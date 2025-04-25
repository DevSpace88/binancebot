# app.py
import logging
import argparse
import json
import os
from typing import Dict, Any

# Lokale Module importieren
from model import PredictionModel
from data_collector import DataCollector
from trader import Trader
from scheduler import Scheduler
from api import TradeBotAPI


class TradeBotApp:
    def __init__(self, config_file=None):
        self.logger = self._setup_logging()
        self.config = self._load_config(config_file)


        self.data_collector = DataCollector(api_keys=self.config.get('api_keys', {}))
        self.model = PredictionModel(config=self.config.get('model', {}))
        self.trader = Trader(config=self.config.get('trader', {}))
        self.scheduler = Scheduler()


        self.api = TradeBotAPI(self.model, self.data_collector, self.trader, self.scheduler, parent_app=self)

    def _setup_logging(self):
        """Richtet das Logging ein"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("tradebot.log"),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('TradeBotApp')

    def _load_config(self, config_file):
        """Lädt die Konfiguration aus einer Datei"""
        default_config = {
            'api_keys': {},
            'model': {
                'model_type': 'random_forest',
                'features': ['close', 'volume', 'rsi', 'macd', 'sentiment'],
                'target': 'close',
                'prediction_horizon': 1
            },
            'trader': {
                'trading_enabled': False,
                'exchanges': {
                    'binance': {
                        'test_mode': True
                    }
                },
                'trade_amount': 100,
                'max_trades_per_day': 5
            },
            'api': {
                'host': '0.0.0.0',
                'port': 8000
            }
        }

        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    loaded_config = json.load(f)


                def recursive_update(d, u):
                    for k, v in u.items():
                        if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                            recursive_update(d[k], v)
                        else:
                            d[k] = v

                recursive_update(default_config, loaded_config)
                self.logger.info(f"Konfiguration aus {config_file} geladen")

            except Exception as e:
                self.logger.error(f"Fehler beim Laden der Konfiguration: {str(e)}")
                self.logger.info("Verwende Standard-Konfiguration")
        else:
            self.logger.info("Verwende Standard-Konfiguration")

        return default_config

    def save_config(self, config_file=None):
        """saves current config in a file"""
        config_to_save = {
            'api_keys': self.data_collector.api_keys,
            'model': self.model.config,
            'trader': self.trader.config,
            'api': {
                'host': self.config.get('api', {}).get('host', '0.0.0.0'),
                'port': self.config.get('api', {}).get('port', 8000)
            }
        }

        save_path = config_file or 'config.json'

        try:
            with open(save_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            self.logger.info(f"Konfiguration in {save_path} gespeichert")
            return True
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern der Konfiguration: {str(e)}")
            return False

    def start(self):
        self.logger.info("TradeBot wird gestartet...")

        # Scheduler starten
        self.scheduler.start()
        self.logger.info("Scheduler gestartet")

        # API starten
        api_config = self.config.get('api', {})
        host = api_config.get('host', '0.0.0.0')
        port = api_config.get('port', 8000)

        self.logger.info(f"API wird gestartet auf {host}:{port}")
        self.api.run(host=host, port=port)

    def stop(self):
        self.logger.info("TradeBot wird gestoppt...")
        self.scheduler.stop()
        self.logger.info("TradeBot gestoppt")
