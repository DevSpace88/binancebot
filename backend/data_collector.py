"""
TradeBot - Ein konfigurierbarer Handelsbot mit prädiktivem Modell und Web-Frontend

Hauptmodule:
- data_collector.py: Sammelt Marktdaten von verschiedenen APIs
- model.py: Implementiert das prädiktive Modell
- trader.py: Führt Handelslogik basierend auf Vorhersagen aus
- scheduler.py: Plant und steuert stündliche Jobs
- api.py: RESTful API für Frontend-Kommunikation
- app.py: Hauptanwendung, die alle Komponenten zusammenführt
- frontend/: Verzeichnis für das Web-Frontend
"""

# data_collector.py
import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tradebot.log"),
        logging.StreamHandler()
    ]
)


class DataCollector:
    def __init__(self, api_keys=None):
        self.api_keys = api_keys or {}
        self.logger = logging.getLogger('DataCollector')

    def get_market_data(self, symbol, timeframe='1h', limit=100):
        """Sammelt historische Marktdaten für ein bestimmtes Symbol"""
        # Beispiel für Binance API
        if 'binance' in self.api_keys:
            try:
                endpoint = f"https://api.binance.com/api/v3/klines"
                params = {
                    'symbol': symbol.replace('-', ''),
                    'interval': timeframe,
                    'limit': limit
                }
                response = requests.get(endpoint, params=params)
                data = response.json()

                # Konvertiere Daten in DataFrame
                df = pd.DataFrame(data, columns=[
                    'timestamp', 'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                    'taker_buy_quote', 'ignore'
                ])
                # Konvertiere Spalten zu numerischen Werten
                for col in ['open', 'high', 'low', 'close', 'volume']:
                    df[col] = pd.to_numeric(df[col])
                # Konvertiere Timestamp zu datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

                self.logger.info(f"Erfolgreich Daten für {symbol} abgerufen: {len(df)} Einträge")
                return df
            except Exception as e:
                self.logger.warning(f"Fehler bei Binance API: {str(e)}, versuche Yahoo Finance")
                # Kein return hier, damit wir zum Yahoo Finance Fallback gelangen

        # Alternative: Yahoo Finance (keine API-Keys erforderlich)
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            interval_map = {'1h': '1h', '1d': '1d', '15m': '15m'}
            df = ticker.history(period=f"{limit}{timeframe[-1]}", interval=interval_map.get(timeframe, '1h'))

            self.logger.info(f"Erfolgreich Daten für {symbol} über Yahoo Finance abgerufen: {len(df)} Einträge")
            return df
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen von Marktdaten mit Yahoo Finance: {str(e)}")
            return pd.DataFrame()  # Leeres DataFrame zurückgeben

    def get_news_sentiment(self, symbol):
        """Ruft Nachrichtensentiment für ein Symbol ab"""
        if 'news_api' in self.api_keys and self.api_keys['news_api']:
            try:
                # Alpha Vantage News API
                endpoint = f"https://www.alphavantage.co/query"
                params = {
                    'function': 'NEWS_SENTIMENT',
                    'tickers': symbol,
                    'apikey': self.api_keys['news_api']
                }
                response = requests.get(endpoint, params=params)
                data = response.json()

                sentiment_score = 0
                if 'feed' in data:
                    sentiments = [item.get('overall_sentiment_score', 0) for item in data['feed']]
                    if sentiments:
                        sentiment_score = sum(sentiments) / len(sentiments)

                self.logger.info(f"Sentiment-Score für {symbol}: {sentiment_score}")
                return sentiment_score
            except Exception as e:
                self.logger.error(f"Fehler beim Abrufen des Nachrichtensentiments: {str(e)}")
                # Fallback auf Dummy-Wert

        # Dummy-Wert zurückgeben, wenn kein API-Key vorhanden oder ein Fehler aufgetreten ist
        import random
        dummy_score = random.uniform(-0.1, 0.1)  # Kleine zufällige Werte, nahe neutral
        self.logger.info(f"Verwende Dummy-Sentiment für {symbol}: {dummy_score}")
        return dummy_score

    def prepare_features(self, symbol, prediction_hours=1):
        """Bereitet Features für das Modell vor"""
        # Marktdaten abrufen
        market_data = self.get_market_data(symbol, limit=168)  # 1 Woche stündliche Daten

        if market_data.empty:
            return None

        # Technische Indikatoren berechnen
        market_data['rsi'] = self._calculate_rsi(market_data['close'])
        market_data['macd'], market_data['macd_signal'] = self._calculate_macd(market_data['close'])
        market_data['ema_short'] = market_data['close'].ewm(span=12).mean()
        market_data['ema_medium'] = market_data['close'].ewm(span=26).mean()
        market_data['ema_long'] = market_data['close'].ewm(span=50).mean()
        market_data['volatility'] = market_data['close'].rolling(window=24).std()

        # Sentiment-Daten hinzufügen
        sentiment = self.get_news_sentiment(symbol)
        market_data['sentiment'] = sentiment

        # Nur die neuesten Daten für Prognose zurückgeben
        return market_data.iloc[-48:].dropna()  # 48 Stunden Daten

    def _calculate_rsi(self, prices, period=14):
        """Berechnet den Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Berechnet den MACD (Moving Average Convergence Divergence)"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        return macd, macd_signal

    # Optional: Diese Methode kann später implementiert werden, wenn erweiterte Funktionalität benötigt wird
    def get_economic_indicators(self):
        """
        Ruft wichtige Wirtschaftsindikatoren ab

        Diese Funktion ist ein Platzhalter für zukünftige Erweiterungen.
        Sie könnte verwendet werden, um makroökonomische Daten wie Inflationsraten,
        BIP-Wachstum, Arbeitslosenquoten usw. abzurufen und in die Handelsentscheidungen einzubeziehen.
        """
        # TODO: Implementierung für Wirtschaftsindikatoren (Inflation, BIP usw.)
        return {}