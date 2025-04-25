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
            'trading_enabled': False,  # Disabled by default (Paper-Trading)
            'exchanges': {
                'binance': {
                    'api_key': '',
                    'api_secret': '',
                    'test_mode': True  # Test mode enabled by default
                }
            },
            'trade_amount': 100,  # Default amount per trade in base currency (e.g. USD)
            'max_trades_per_day': 5,
            'stop_loss_pct': 2.0,
            'take_profit_pct': 3.0,
            'max_open_trades': 3,
            'confidence_threshold': 0.7,  # Minimum confidence for trades
            'min_change_pct': 1.0,  # Minimum change for trades
            'symbols': ['BTC-USDT', 'ETH-USDT'],  # Tradable symbols
            'risk_management': {
                'max_risk_per_trade': 2.0,  # Maximum risk per trade in %
                'daily_drawdown_limit': 5.0  # Maximum daily drawdown in %
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

        # Load trade history if available
        self._load_trade_history()

    def _load_trade_history(self):
        """Loads the trading history from a file"""
        try:
            if os.path.exists('trade_history.json'):
                with open('trade_history.json', 'r') as f:
                    data = json.load(f)
                    self.trade_history = data.get('history', [])
                    self.open_trades = data.get('open_trades', [])
                    self.daily_stats = data.get('daily_stats', self.daily_stats)

                # Check if daily_stats is for the current day
                if self.daily_stats['date'] != datetime.now().strftime('%Y-%m-%d'):
                    self.daily_stats = {
                        'trades': 0,
                        'profit_loss': 0.0,
                        'date': datetime.now().strftime('%Y-%m-%d')
                    }

                self.logger.info(f"Trading history loaded: {len(self.trade_history)} past trades, " +
                                 f"{len(self.open_trades)} open trades")
        except Exception as e:
            self.logger.error(f"Error loading trading history: {str(e)}")

    def _save_trade_history(self):
        """Saves the trading history to a file"""
        try:
            data = {
                'history': self.trade_history,
                'open_trades': self.open_trades,
                'daily_stats': self.daily_stats
            }

            with open('trade_history.json', 'w') as f:
                json.dump(data, f, indent=2)

            self.logger.info("Trading history saved")
        except Exception as e:
            self.logger.error(f"Error saving trading history: {str(e)}")

    def process_prediction(self, symbol: str, prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a prediction and decides on trading actions

        Args:
            symbol: Trading symbol (e.g. 'BTC-USDT')
            prediction: Prediction result from the model

        Returns:
            Dictionary with trading decision and details
        """
        if not self.config['trading_enabled']:
            return {
                'action': 'none',
                'reason': 'Trading is disabled (Paper-Trading mode)',
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol,
                'prediction': prediction
            }

        # Check if the symbol is in the list of tradable symbols
        if symbol not in self.config['symbols']:
            return {
                'action': 'none',
                'reason': f"Symbol {symbol} is not in the list of tradable symbols",
                'timestamp': datetime.now().isoformat()
            }

        # Check daily trading limit
        if self.daily_stats['trades'] >= self.config['max_trades_per_day']:
            return {
                'action': 'none',
                'reason': 'Daily trading limit reached',
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol
            }

        # Check open trades for the symbol
        symbol_open_trades = [t for t in self.open_trades if t['symbol'] == symbol]
        if len(symbol_open_trades) > 0:
            # There are already open trades for this symbol
            return {
                'action': 'none',
                'reason': f"There are already {len(symbol_open_trades)} open trades for {symbol}",
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol
            }

        # Check minimum confidence and change
        if prediction.get('confidence', 0) < self.config['confidence_threshold']:
            return {
                'action': 'none',
                'reason': f"Confidence {prediction.get('confidence', 0):.2f} below threshold {self.config['confidence_threshold']}",
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol
            }

        if abs(prediction.get('change_pct', 0)) < self.config['min_change_pct']:
            return {
                'action': 'none',
                'reason': f"Predicted change {abs(prediction.get('change_pct', 0)):.2f}% below threshold {self.config['min_change_pct']}%",
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol
            }

        # Make trading decision
        action = 'buy' if prediction.get('direction') == 'up' else 'sell'

        # Execute trade
        trade_result = self._execute_trade(symbol, action, prediction)

        # Add trade to trading history
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

            self.logger.info(f"New trade opened: {action.upper()} {symbol} at {prediction.get('current')}")

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
                'reason': trade_result.get('message', 'Unknown error'),
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol
            }

    def _execute_trade(self, symbol: str, action: str, prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a trade (or simulates it in Paper-Trading mode)

        Args:
            symbol: Trading symbol
            action: 'buy' or 'sell'
            prediction: Prediction result

        Returns:
            Trade result
        """
        try:
            if not self.config['trading_enabled'] or self.config['exchanges']['binance'].get('test_mode', True):
                # Paper-Trading mode
                self.logger.info(f"Paper-Trading: {action.upper()} {symbol} at {prediction.get('current')}")
                return {
                    'success': True,
                    'message': 'Paper-Trading mode'
                }
            else:
                # Live-Trading (Binance as example)
                if 'binance' in self.config['exchanges'] and self.config['exchanges']['binance']['api_key']:
                    # Here would be the integration with the Binance API
                    api_key = self.config['exchanges']['binance']['api_key']
                    api_secret = self.config['exchanges']['binance']['api_secret']

                    # Placeholder for Binance API integration
                    self.logger.info(f"Real trade: {action.upper()} {symbol} at {prediction.get('current')}")

                    # In a real implementation, the Binance API would be called here
                    # Example:
                    # from binance.client import Client
                    # client = Client(api_key, api_secret)
                    # if action == 'buy':
                    #     order = client.order_market_buy(symbol=symbol.replace('-', ''), quantity=quantity)
                    # else:
                    #     order = client.order_market_sell(symbol=symbol.replace('-', ''), quantity=quantity)

                    return {
                        'success': True,
                        'message': 'Trade successfully executed'
                    }
                else:
                    return {
                        'success': False,
                        'message': 'No valid API credentials for the exchange'
                    }
        except Exception as e:
            self.logger.error(f"Error executing the trade: {str(e)}")
            return {
                'success': False,
                'message': f"Error: {str(e)}"
            }

    def update_open_trades(self, current_prices: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Updates open trades and checks for Stop-Loss/Take-Profit

        Args:
            current_prices: Dictionary with current prices for symbols

        Returns:
            List of closed trades
        """
        closed_trades = []

        for trade in list(self.open_trades):  # Copy list to iterate safely
            symbol = trade['symbol']

            if symbol not in current_prices:
                self.logger.warning(f"No current price available for {symbol}, trade remains open")
                continue

            current_price = current_prices[symbol]
            action = trade['action']
            entry_price = trade['price']
            stop_loss = trade['stop_loss']
            take_profit = trade['take_profit']

            # Calculate profit/loss
            if action == 'buy':
                profit_loss_pct = (current_price - entry_price) / entry_price * 100
                close_condition = (current_price <= stop_loss) or (current_price >= take_profit)
            else:  # sell/short
                profit_loss_pct = (entry_price - current_price) / entry_price * 100
                close_condition = (current_price >= stop_loss) or (current_price <= take_profit)

            # Close trade if Stop-Loss or Take-Profit has been reached
            if close_condition:
                reason = 'stop_loss' if (
                        (action == 'buy' and current_price <= stop_loss) or
                        (action == 'sell' and current_price >= stop_loss)
                ) else 'take_profit'

                # Mark trade as closed
                trade['status'] = 'closed'
                trade['close_price'] = current_price
                trade['close_time'] = datetime.now().isoformat()
                trade['profit_loss'] = profit_loss_pct
                trade['close_reason'] = reason

                # Move to history
                self.trade_history.append(trade)
                self.open_trades.remove(trade)
                closed_trades.append(trade)

                # Update daily statistics
                self.daily_stats['profit_loss'] += profit_loss_pct

                self.logger.info(f"Trade closed: {action.upper()} {symbol}, " +
                                 f"Reason: {reason}, P/L: {profit_loss_pct:.2f}%")

        # Save trading history
        if closed_trades:
            self._save_trade_history()

        return closed_trades

    def _calculate_stop_loss(self, action: str, current_price: float) -> float:
        """Calculates the Stop-Loss price"""
        stop_loss_pct = self.config['stop_loss_pct']

        if action == 'buy':
            return current_price * (1 - stop_loss_pct / 100)
        else:  # sell/short
            return current_price * (1 + stop_loss_pct / 100)

    def _calculate_take_profit(self, action: str, current_price: float) -> float:
        """Calculates the Take-Profit price"""
        take_profit_pct = self.config['take_profit_pct']

        if action == 'buy':
            return current_price * (1 + take_profit_pct / 100)
        else:  # sell/short
            return current_price * (1 - take_profit_pct / 100)

    def get_trading_stats(self) -> Dict[str, Any]:
        """
        Returns trading statistics

        Returns:
            Dictionary with trading statistics
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

            # Calculate total performance
            total_profit_loss = sum(trade.get('profit_loss', 0) for trade in self.trade_history)
            stats['total_profit_loss'] = total_profit_loss

            # Average profit/loss
            stats['avg_profit_loss'] = total_profit_loss / len(self.trade_history)

            # Best and worst trades
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
        Updates the trader configuration

        Args:
            new_config: New configuration parameters
        """

        # Recursive update function for nested dictionaries
        def recursive_update(d, u):
            for k, v in u.items():
                if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                    recursive_update(d[k], v)
                else:
                    d[k] = v

        recursive_update(self.config, new_config)
        self.logger.info(f"Trader Einstellungen aktualisiert {new_config}")