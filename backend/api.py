# api.py
from fastapi import FastAPI, HTTPException, Body, Query, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, List, Optional
import uvicorn
import logging
import os
import json
from datetime import datetime, timedelta
import time

# Lokale Module importieren
from model import PredictionModel
from data_collector import DataCollector
from trader import Trader
from scheduler import Scheduler


# Pydantic-Modelle für API-Requests/Responses
class PredictionRequest(BaseModel):
    symbol: str
    timeframe: str = Field(default="1h", description="Timeframe for prediction (e.g. '1h', '4h', '1d')")

    @validator('symbol')
    def validate_symbol(cls, v):
        if not v or len(v) < 3:
            raise ValueError("Symbol muss mindestens 3 Zeichen lang sein")
        return v

    @validator('timeframe')
    def validate_timeframe(cls, v):
        valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d', '3d', '1w']
        if v not in valid_timeframes:
            raise ValueError(f"Timeframe muss einer der folgenden sein: {', '.join(valid_timeframes)}")
        return v


class PredictionResponse(BaseModel):
    symbol: str
    prediction: float
    current: float
    change: float
    change_pct: float
    direction: str
    confidence: float
    timestamp: str


class TradeRequest(BaseModel):
    symbol: str
    action: str = Field(description="Trade action: 'buy' or 'sell'")
    amount: Optional[float] = None

    @validator('action')
    def validate_action(cls, v):
        if v not in ['buy', 'sell']:
            raise ValueError("Action muss entweder 'buy' oder 'sell' sein")
        return v


class ConfigUpdateRequest(BaseModel):
    section: str = Field(description="Configuration section to update ('model', 'trader', or 'global')")
    config: Dict[str, Any] = Field(description="Configuration parameters to update")

    @validator('section')
    def validate_section(cls, v):
        if v not in ['model', 'trader', 'global']:
            raise ValueError("Section muss 'model', 'trader' oder 'global' sein")
        return v


class JobRequest(BaseModel):
    symbol: str
    interval: str = Field(default="1h", description="Job interval (e.g. '1h', '30m', '1d')")

    @validator('interval')
    def validate_interval(cls, v):
        valid_intervals = ['15m', '30m', '1h', '2h', '4h', '12h', '1d']
        if v not in valid_intervals:
            raise ValueError(f"Interval muss einer der folgenden sein: {', '.join(valid_intervals)}")
        return v


# Neues Modell für das Modelltraining
class TrainModelRequest(BaseModel):
    symbol: str
    data_points: int = Field(default=2000, ge=100, le=10000, description="Anzahl der Datenpunkte (Stunden) für Training")


# API-Klasse
class TradeBotAPI:
    def __init__(self, model, data_collector, trader, scheduler):
        self.app = FastAPI(title="TradeBot API",
                           description="API für den prädiktiven Handelsbot",
                           version="1.0.0")

        # Komponenten speichern
        self.model = model
        self.data_collector = data_collector
        self.trader = trader
        self.scheduler = scheduler
        self.logger = logging.getLogger('API')

        # CORS konfigurieren - in Produktion einschränken!
        origins = [
            "http://localhost:8080",
            "http://127.0.0.1:8080",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            # Weitere erlaubte Origins hier hinzufügen
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Exception Handler für generelle Fehlerbehandlung
        @self.app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception):
            self.logger.error(f"Unbehandelte Ausnahme: {str(exc)}")
            return JSONResponse(
                status_code=500,
                content={"detail": f"Interner Serverfehler: {str(exc)}"}
            )

        # Routen registrieren
        self._setup_routes()

        # Statische Dateien einbinden
        if os.path.exists('frontend/dist'):
            self.app.mount("/static", StaticFiles(directory="frontend/dist/static"), name="static")
            self.app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")

    def _setup_routes(self):
        """Richtet die API-Routen ein"""

        @self.app.get("/api/status")
        async def get_status():
            """Gibt den aktuellen Status des Bots zurück"""
            try:
                return {
                    "status": "running",
                    "time": datetime.now().isoformat(),
                    "trading_enabled": self.trader.config['trading_enabled'],
                    "scheduler_running": self.scheduler.running,
                    "active_jobs": len(self.scheduler.jobs),
                    "model_type": self.model.config.get('model_type', 'unknown')
                }
            except Exception as e:
                self.logger.error(f"Fehler beim Abrufen des Status: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Fehler beim Abrufen des Status: {str(e)}")

        @self.app.post("/api/predict", response_model=PredictionResponse)
        async def predict(request: PredictionRequest):
            """Führt eine Prognose für ein Symbol durch"""
            try:
                # Daten sammeln
                features = self.data_collector.prepare_features(request.symbol)
                if features is None or features.empty:
                    raise HTTPException(status_code=400, detail=f"Keine Daten für {request.symbol} verfügbar")

                # Vorhersage machen
                prediction = self.model.predict(features)

                if 'error' in prediction:
                    raise HTTPException(status_code=500, detail=prediction['error'])

                # Response erweitern
                prediction['symbol'] = request.symbol

                return prediction

            except HTTPException as he:
                raise he
            except Exception as e:
                self.logger.error(f"Fehler bei Vorhersage: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/trade")
        async def execute_trade(request: TradeRequest):
            """Führt einen Trade manuell aus"""
            try:
                # Aktuelle Daten holen
                features = self.data_collector.prepare_features(request.symbol)
                if features is None or features.empty:
                    raise HTTPException(status_code=400, detail=f"Keine Daten für {request.symbol} verfügbar")

                # Dummy-Vorhersage erstellen für manuellen Trade
                current_price = features['close'].iloc[-1]
                prediction = {
                    'current': current_price,
                    'prediction': current_price * (1.02 if request.action == 'buy' else 0.98),
                    'direction': 'up' if request.action == 'buy' else 'down',
                    'confidence': 1.0,  # Maximales Vertrauen für manuellen Trade
                    'change': 0.0,
                    'change_pct': 2.0 if request.action == 'buy' else -2.0,
                    'timestamp': datetime.now().isoformat()
                }

                # Trade ausführen
                result = self.trader.process_prediction(request.symbol, prediction)

                return result

            except HTTPException as he:
                raise he
            except Exception as e:
                self.logger.error(f"Fehler bei manuellem Trade: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/trades")
        async def get_trades(status: str = Query(None, description="Filter nach Status ('open', 'closed', 'all')")):
            """Gibt die Trades zurück"""
            try:
                if status == 'open' or status is None:
                    return {'trades': self.trader.open_trades}
                elif status == 'closed':
                    return {'trades': self.trader.trade_history}
                else:  # 'all'
                    return {
                        'open_trades': self.trader.open_trades,
                        'closed_trades': self.trader.trade_history
                    }
            except Exception as e:
                self.logger.error(f"Fehler beim Abrufen der Trades: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/stats")
        async def get_stats():
            """Gibt Handelsstatistiken zurück"""
            try:
                return self.trader.get_trading_stats()
            except Exception as e:
                self.logger.error(f"Fehler beim Abrufen der Statistiken: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        # In der _setup_routes-Methode von api.py, aktualisiere die update_config-Funktion wie folgt:

        @self.app.post("/api/config")
        async def update_config(request: ConfigUpdateRequest):
            """Aktualisiert die Konfiguration"""
            try:
                if request.section == 'model':
                    self.model.update_config(request.config)
                elif request.section == 'trader':
                    self.trader.update_config(request.config)
                elif request.section == 'global':
                    # Globale Konfiguration betrifft alle Komponenten
                    if 'trading_enabled' in request.config:
                        self.trader.config['trading_enabled'] = request.config['trading_enabled']

                    # API-Keys aktualisieren
                    if 'api_keys' in request.config:
                        if 'news_api' in request.config['api_keys']:
                            # News API-Key in data_collector aktualisieren
                            if not hasattr(self.data_collector, 'api_keys'):
                                self.data_collector.api_keys = {}

                            self.data_collector.api_keys['news_api'] = request.config['api_keys']['news_api']
                            self.logger.info("News API-Key aktualisiert")

                    # Weitere globale Konfigurationen hier...
                else:
                    raise HTTPException(status_code=400, detail=f"Unbekannte Konfigurationssektion: {request.section}")

                return {"message": f"Konfiguration für {request.section} aktualisiert"}

            except HTTPException as he:
                raise he
            except Exception as e:
                self.logger.error(f"Fehler bei Konfigurationsaktualisierung: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/config")
        async def get_config(section: str = Query(None)):
            """Gibt die aktuelle Konfiguration zurück"""
            try:
                if section == 'model':
                    return {'config': self.model.config}
                elif section == 'trader':
                    return {'config': self.trader.config}
                else:
                    # Zusätzliche API-Keys in der Antwort einschließen
                    api_keys = {}
                    if hasattr(self.data_collector, 'api_keys'):
                        # Keine Secrets in der Antwort senden
                        if 'news_api' in self.data_collector.api_keys:
                            api_keys['news_api'] = self.data_collector.api_keys['news_api']

                    return {
                        'model_config': self.model.config,
                        'trader_config': self.trader.config,
                        'api_keys': api_keys
                    }
            except Exception as e:
                self.logger.error(f"Fehler beim Abrufen der Konfiguration: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/jobs")
        async def add_job(request: JobRequest):
            """Fügt einen Prognose- und Handelsjob hinzu"""
            try:
                job_id = f"predict_{request.symbol}_{request.interval}"

                # Job-Funktion
                def prediction_job(symbol=request.symbol):
                    try:
                        self.logger.info(f"Führe Vorhersagejob für {symbol} aus")
                        # Daten sammeln
                        features = self.data_collector.prepare_features(symbol)
                        if features is None or features.empty:
                            self.logger.error(f"Keine Daten für {symbol} verfügbar")
                            return

                        # Vorhersage machen
                        prediction = self.model.predict(features)

                        if 'error' in prediction:
                            self.logger.error(f"Fehler bei Vorhersage: {prediction['error']}")
                            return

                        # Handelsentscheidung treffen
                        trade_result = self.trader.process_prediction(symbol, prediction)

                        self.logger.info(f"Vorhersagejob für {symbol} abgeschlossen: {trade_result['action']}")

                    except Exception as e:
                        self.logger.error(f"Fehler im Vorhersagejob: {str(e)}")

                # Job hinzufügen
                self.scheduler.add_job(job_id, request.interval, prediction_job)

                return {
                    "message": f"Job für {request.symbol} mit Intervall {request.interval} hinzugefügt",
                    "job_id": job_id
                }

            except Exception as e:
                self.logger.error(f"Fehler beim Hinzufügen des Jobs: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.delete("/api/jobs/{job_id}")
        async def remove_job(job_id: str):
            """Entfernt einen Job"""
            try:
                if self.scheduler.remove_job(job_id):
                    return {"message": f"Job {job_id} entfernt"}
                else:
                    raise HTTPException(status_code=404, detail=f"Job {job_id} nicht gefunden")
            except HTTPException as he:
                raise he
            except Exception as e:
                self.logger.error(f"Fehler beim Entfernen des Jobs: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/jobs")
        async def get_jobs():
            """Gibt alle aktiven Jobs zurück"""
            try:
                return {"jobs": self.scheduler.get_jobs()}
            except Exception as e:
                self.logger.error(f"Fehler beim Abrufen der Jobs: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/train")
        async def train_model(request: TrainModelRequest):
            """Trainiert das Modell mit historischen Daten für ein Symbol"""
            try:
                # Mehr historische Daten für das Training sammeln
                features = self.data_collector.get_market_data(request.symbol, limit=request.data_points)

                if features.empty:
                    raise HTTPException(status_code=400, detail=f"Keine Trainingsdaten für {request.symbol} verfügbar")

                # Technische Indikatoren hinzufügen
                features['rsi'] = self.data_collector._calculate_rsi(features['close'])
                features['macd'], features['macd_signal'] = self.data_collector._calculate_macd(features['close'])
                features['ema_short'] = features['close'].ewm(span=12).mean()
                features['ema_medium'] = features['close'].ewm(span=26).mean()
                features['ema_long'] = features['close'].ewm(span=50).mean()
                features['volatility'] = features['close'].rolling(window=24).std()

                # Sentiment-Daten hinzufügen (Dummy-Werte für historische Daten)
                import numpy as np
                features['sentiment'] = np.random.uniform(-0.5, 0.5, size=len(features))

                # Modell trainieren
                self.model.train(features.dropna())

                return {
                    "message": f"Modell erfolgreich mit {len(features.dropna())} Datenpunkten für {request.symbol} trainiert",
                    "data_points": len(features.dropna()),
                    "symbol": request.symbol,
                    "model_type": self.model.config.get('model_type', 'unknown')
                }

            except HTTPException as he:
                raise he
            except Exception as e:
                self.logger.error(f"Fehler beim Training des Modells: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

    def run(self, host="0.0.0.0", port=8000):
        """Startet den API-Server"""
        # Konfiguriere uvicorn für bessere Fehlerbehandlung
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr"
                }
            },
            "loggers": {
                "uvicorn": {"handlers": ["default"], "level": "INFO"}
            }
        }

        try:
            uvicorn.run(
                self.app,
                host=host,
                port=port,
                log_config=log_config,
                log_level="info"
            )
        except Exception as e:
            self.logger.error(f"Fehler beim Starten des API-Servers: {str(e)}")
            raise