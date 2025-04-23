# trader.py
import pandas as pd
import numpy as np
import logging
import json
import os
import time
from typing import Dict, Any, List, Optional
import requests
from datetime import datetime, timedelta


class Trader:
    def __init__(self, config=None):
        self.config = config or {
            'trading_enabled': False,  # Standardmäßig deaktiviert (Paper-Trading)
            'exchanges': {
                'binance': {
                    'api_key': '',
                    'api_secret': '',
                    'test_mode': True  # Testmodus standardmäßig aktiviert
                }
            },
            'trade_amount': 100,  # Standardbetrag pro Trade in der Basiswährung (z.B. USD)
            'max_trades_per_day': 5,
            'stop_loss_pct': 2.0,
            'take_profit_pct': 3.0,
            'max_open_trades': 3,
            'confidence_threshold': 0.7,  # Mindestvertrauen für Trades
            'min_change_pct': 1.0,  # Mindeständerung für Trades
            'symbols': ['BTC-USDT', 'ETH-USDT'],  # Handelbare Symbole
            'risk_management': {
                'max_risk_per_trade': 2.0,  # Maximales Risiko pro Trade in %
                'daily_drawdown_limit': 5.0  # Maximaler täglicher Drawdown in %
            }
        }

        self.logger = logging.getLogger('Trader')
        self.open_trades = []
        self.trade_history = []
        self.daily_stats = {
            'trades': 0,
            'profit_loss': 0.0,
            'date': datetime.now().strftime('%Y-%m-%d')
        }

        # Handelshistorie laden, falls vorhanden
        self._load_trade_history()

    def _load_trade_history(self):
        """Lädt die Handelshistorie aus einer Datei"""
        try:
            if os.path.exists('trade_history.json'):
                with open('trade_history.json', 'r') as f:
                    data = json.load(f)
                    self.trade_history = data.get('history', [])
                    self.open_trades = data.get('open_trades', [])
                    self.daily_stats = data.get('daily_stats', self.daily_stats)

                # Überprüfen, ob daily_stats für den aktuellen Tag ist
                if self.daily_stats['date'] != datetime.now().strftime('%Y-%m-%d'):
                    self.daily_stats = {
                        'trades': 0,
                        'profit_loss': 0.0,
                        'date': datetime.now().strftime('%Y-%m-%d')
                    }

                self.logger.info(f"Handelshistorie geladen: {len(self.trade_history)} vergangene Trades, " +
                                 f"{len(self.open_trades)} offene Trades")
        except Exception as e:
            self.logger.error(f"Fehler beim Laden der Handelshistorie: {str(e)}")

    def _save_trade_history(self):
        """Speichert die Handelshistorie in einer Datei"""
        try:
            data = {
                'history': self.trade_history,
                'open_trades': self.open_trades,
                'daily_stats': self.daily_stats
            }

            with open('trade_history.json', 'w') as f:
                json.dump(data, f, indent=2)

            self.logger.info("Handelshistorie gespeichert")
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern der Handelshistorie: {str(e)}")

    def process_prediction(self, symbol: str, prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verarbeitet eine Vorhersage und entscheidet über Handelsaktionen

        Args:
            symbol: Handelssymbol (z.B. 'BTC-USDT')
            prediction: Vorhersageergebnis vom Modell

        Returns:
            Dictionary mit Handelsentscheidung und -details
        """
        if not self.config['trading_enabled']:
            return {
                'action': 'none',
                'reason': 'Trading ist deaktiviert (Paper-Trading-Modus)',
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol,
                'prediction': prediction
            }

        # Überprüfen, ob das Symbol in der Liste der handelbaren Symbole ist
        if symbol not in self.config['symbols']:
            return {
                'action': 'none',
                'reason': f"Symbol {symbol} ist nicht in der Liste der handelbaren Symbole",
                'timestamp': datetime.now().isoformat()
            }

        # Tägliches Handelslimit überprüfen
        if self.daily_stats['trades'] >= self.config['max_trades_per_day']:
            return {
                'action': 'none',
                'reason': 'Tägliches Handelslimit erreicht',
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol
            }

        # Offene Trades für das Symbol überprüfen
        symbol_open_trades = [t for t in self.open_trades if t['symbol'] == symbol]
        if len(symbol_open_trades) > 0:
            # Es gibt bereits offene Trades für dieses Symbol
            return {
                'action': 'none',
                'reason': f"Es gibt bereits {len(symbol_open_trades)} offene Trades für {symbol}",
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol
            }

        # Mindestvertrauen und -änderung überprüfen
        if prediction.get('confidence', 0) < self.config['confidence_threshold']:
            return {
                'action': 'none',
                'reason': f"Vertrauen {prediction.get('confidence', 0):.2f} unter Schwellenwert {self.config['confidence_threshold']}",
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol
            }

        if abs(prediction.get('change_pct', 0)) < self.config['min_change_pct']:
            return {
                'action': 'none',
                'reason': f"Vorhergesagte Änderung {abs(prediction.get('change_pct', 0)):.2f}% unter Schwellenwert {self.config['min_change_pct']}%",
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol
            }

        # Handelsentscheidung treffen
        action = 'buy' if prediction.get('direction') == 'up' else 'sell'

        # Trade ausführen
        trade_result = self._execute_trade(symbol, action, prediction)

        # Trade zur Handelshistorie hinzufügen
        if trade_result.get('success', False):
            trade_info = {
                'id': f"trade_{int(time.time())}",
                'symbol': symbol,
                'action': action,
                'price': prediction.get('current'),
                'amount': self.config['trade_amount'],
                'timestamp': datetime.now().isoformat(),
                'prediction': prediction,
                'status': 'open',
                'stop_loss': self._calculate_stop_loss(action, prediction.get('current')),
                'take_profit': self._calculate_take_profit(action, prediction.get('current'))
            }

            self.open_trades.append(trade_info)
            self.daily_stats['trades'] += 1
            self._save_trade_history()

            self.logger.info(f"Neuer Trade eröffnet: {action.upper()} {symbol} bei {prediction.get('current')}")

            return {
                'action': action,
                'success': True,
                'trade_info': trade_info,
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol
            }
        else:
            return {
                'action': 'error',
                'reason': trade_result.get('message', 'Unbekannter Fehler'),
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol
            }

    def _execute_trade(self, symbol: str, action: str, prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Führt einen Trade aus (oder simuliert ihn im Paper-Trading-Modus)

        Args:
            symbol: Handelssymbol
            action: 'buy' oder 'sell'
            prediction: Vorhersageergebnis

        Returns:
            Trade-Ergebnis
        """
        try:
            if not self.config['trading_enabled'] or self.config['exchanges']['binance'].get('test_mode', True):
                # Paper-Trading-Modus
                self.logger.info(f"Paper-Trading: {action.upper()} {symbol} bei {prediction.get('current')}")
                return {
                    'success': True,
                    'message': 'Paper-Trading-Modus'
                }
            else:
                # Live-Trading (Binance als Beispiel)
                if 'binance' in self.config['exchanges'] and self.config['exchanges']['binance']['api_key']:
                    # Hier würde die Integration mit der Binance-API erfolgen
                    api_key = self.config['exchanges']['binance']['api_key']
                    api_secret = self.config['exchanges']['binance']['api_secret']

                    # Platzhalter für Binance-API-Integration
                    self.logger.info(f"Echter Trade: {action.upper()} {symbol} bei {prediction.get('current')}")

                    # In einer echten Implementierung würde hier die Binance-API aufgerufen werden
                    # Beispiel:
                    # from binance.client import Client
                    # client = Client(api_key, api_secret)
                    # if action == 'buy':
                    #     order = client.order_market_buy(symbol=symbol.replace('-', ''), quantity=quantity)
                    # else:
                    #     order = client.order_market_sell(symbol=symbol.replace('-', ''), quantity=quantity)

                    return {
                        'success': True,
                        'message': 'Trade erfolgreich ausgeführt'
                    }
                else:
                    return {
                        'success': False,
                        'message': 'Keine gültigen API-Zugangsdaten für die Börse'
                    }
        except Exception as e:
            self.logger.error(f"Fehler beim Ausführen des Trades: {str(e)}")
            return {
                'success': False,
                'message': f"Fehler: {str(e)}"
            }

    def update_open_trades(self, current_prices: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Aktualisiert offene Trades und prüft auf Stop-Loss/Take-Profit

        Args:
            current_prices: Dictionary mit aktuellen Preisen für Symbole

        Returns:
            Liste der geschlossenen Trades
        """
        closed_trades = []

        for trade in list(self.open_trades):  # Liste kopieren, um sicher zu iterieren
            symbol = trade['symbol']

            if symbol not in current_prices:
                self.logger.warning(f"Kein aktueller Preis für {symbol} verfügbar, Trade bleibt offen")
                continue

            current_price = current_prices[symbol]
            action = trade['action']
            entry_price = trade['price']
            stop_loss = trade['stop_loss']
            take_profit = trade['take_profit']

            # Gewinn/Verlust berechnen
            if action == 'buy':
                profit_loss_pct = (current_price - entry_price) / entry_price * 100
                close_condition = (current_price <= stop_loss) or (current_price >= take_profit)
            else:  # sell/short
                profit_loss_pct = (entry_price - current_price) / entry_price * 100
                close_condition = (current_price >= stop_loss) or (current_price <= take_profit)

            # Trade schließen, wenn Stop-Loss oder Take-Profit erreicht wurde
            if close_condition:
                reason = 'stop_loss' if (
                        (action == 'buy' and current_price <= stop_loss) or
                        (action == 'sell' and current_price >= stop_loss)
                ) else 'take_profit'

                # Trade als geschlossen markieren
                trade['status'] = 'closed'
                trade['close_price'] = current_price
                trade['close_time'] = datetime.now().isoformat()
                trade['profit_loss'] = profit_loss_pct
                trade['close_reason'] = reason

                # In die Historie verschieben
                self.trade_history.append(trade)
                self.open_trades.remove(trade)
                closed_trades.append(trade)

                # Tagesstatistik aktualisieren
                self.daily_stats['profit_loss'] += profit_loss_pct

                self.logger.info(f"Trade geschlossen: {action.upper()} {symbol}, " +
                                 f"Grund: {reason}, P/L: {profit_loss_pct:.2f}%")

        # Handelshistorie speichern
        if closed_trades:
            self._save_trade_history()

        return closed_trades

    def _calculate_stop_loss(self, action: str, current_price: float) -> float:
        """Berechnet den Stop-Loss-Preis"""
        stop_loss_pct = self.config['stop_loss_pct']

        if action == 'buy':
            return current_price * (1 - stop_loss_pct / 100)
        else:  # sell/short
            return current_price * (1 + stop_loss_pct / 100)

    def _calculate_take_profit(self, action: str, current_price: float) -> float:
        """Berechnet den Take-Profit-Preis"""
        take_profit_pct = self.config['take_profit_pct']

        if action == 'buy':
            return current_price * (1 + take_profit_pct / 100)
        else:  # sell/short
            return current_price * (1 - take_profit_pct / 100)

    def get_trading_stats(self) -> Dict[str, Any]:
        """
        Gibt Handelsstatistiken zurück

        Returns:
            Dictionary mit Handelsstatistiken
        """
        stats = {
            'open_trades': len(self.open_trades),
            'total_trades': len(self.trade_history),
            'daily_trades': self.daily_stats['trades'],
            'daily_profit_loss': self.daily_stats['profit_loss'],
            'win_rate': 0.0
        }

        if self.trade_history:
            profitable_trades = sum(1 for trade in self.trade_history if trade.get('profit_loss', 0) > 0)
            stats['win_rate'] = profitable_trades / len(self.trade_history) * 100

            # Gesamtperformance berechnen
            total_profit_loss = sum(trade.get('profit_loss', 0) for trade in self.trade_history)
            stats['total_profit_loss'] = total_profit_loss

            # Durchschnittlicher Gewinn/Verlust
            stats['avg_profit_loss'] = total_profit_loss / len(self.trade_history)

            # Beste und schlechteste Trades
            best_trade = max(self.trade_history, key=lambda x: x.get('profit_loss', 0))
            worst_trade = min(self.trade_history, key=lambda x: x.get('profit_loss', 0))

            stats['best_trade'] = {
                'symbol': best_trade['symbol'],
                'profit_loss': best_trade.get('profit_loss', 0),
                'date': best_trade['timestamp']
            }

            stats['worst_trade'] = {
                'symbol': worst_trade['symbol'],
                'profit_loss': worst_trade.get('profit_loss', 0),
                'date': worst_trade['timestamp']
            }

        return stats

    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Aktualisiert die Trader-Konfiguration

        Args:
            new_config: Neue Konfigurationsparameter
        """

        # Rekursive Update-Funktion für verschachtelte Dictionaries
        def recursive_update(d, u):
            for k, v in u.items():
                if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                    recursive_update(d[k], v)
                else:
                    d[k] = v

        recursive_update(self.config, new_config)
        self.logger.info(f"Trader-Konfiguration aktualisiert")

