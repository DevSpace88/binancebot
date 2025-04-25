"""
TradeBot - A configurable trading bot with predictive model and web frontend

Main modules:
- data_collector.py: Collects market data from various APIs
- model.py: Implements the predictive model
- trader.py: Executes trading logic based on predictions
- scheduler.py: Plans and controls hourly jobs
- api.py: RESTful API for frontend communication
- app.py: Main application that combines all components
- frontend/: Directory for the web frontend
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
        """Collects historical market data for a specific symbol"""
        self.logger.info(f"Starting market data retrieval for {symbol} with limit {limit}")

        # ATTEMPT 1: Binance API with Python-Binance library
        try:
            from binance.client import Client

            if 'binance' in self.api_keys and self.api_keys.get('binance', {}).get('api_key'):
                api_key = self.api_keys['binance']['api_key']
                api_secret = self.api_keys['binance'].get('api_secret', '')

                self.logger.info(f"Using Binance API for {symbol}")
                client = Client(api_key, api_secret)

                # Adjust symbol for Binance (remove hyphen)
                binance_symbol = symbol.replace('-', '')

                # Timeframe mapping for Binance
                interval_map = {
                    '1m': Client.KLINE_INTERVAL_1MINUTE,
                    '3m': Client.KLINE_INTERVAL_3MINUTE,
                    '5m': Client.KLINE_INTERVAL_5MINUTE,
                    '15m': Client.KLINE_INTERVAL_15MINUTE,
                    '30m': Client.KLINE_INTERVAL_30MINUTE,
                    '1h': Client.KLINE_INTERVAL_1HOUR,
                    '2h': Client.KLINE_INTERVAL_2HOUR,
                    '4h': Client.KLINE_INTERVAL_4HOUR,
                    '6h': Client.KLINE_INTERVAL_6HOUR,
                    '8h': Client.KLINE_INTERVAL_8HOUR,
                    '12h': Client.KLINE_INTERVAL_12HOUR,
                    '1d': Client.KLINE_INTERVAL_1DAY,
                    '3d': Client.KLINE_INTERVAL_3DAY,
                    '1w': Client.KLINE_INTERVAL_1WEEK,
                    '1M': Client.KLINE_INTERVAL_1MONTH
                }

                binance_interval = interval_map.get(timeframe, Client.KLINE_INTERVAL_1HOUR)

                # use get_klines or get_historical_klines
                try:
                    self.logger.info(
                        f"Binance Klines request for {binance_symbol}, interval {binance_interval}, limit {limit}")
                    klines = client.get_klines(symbol=binance_symbol, interval=binance_interval, limit=limit)

                    if klines and len(klines) > 0:
                        # Convert to DataFrame
                        df = pd.DataFrame(klines, columns=[
                            'timestamp', 'open', 'high', 'low', 'close', 'volume',
                            'close_time', 'quote_asset_volume', 'number_of_trades',
                            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                        ])

                        # Convert columns to numeric values
                        for col in ['open', 'high', 'low', 'close', 'volume']:
                            df[col] = pd.to_numeric(df[col])

                        # Convert timestamp to datetime
                        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

                        self.logger.info(
                            f"Binance data successfully retrieved: {len(df)} data points with columns {df.columns.tolist()}")
                        return df
                except Exception as e:
                    self.logger.warning(f"Error with Binance Klines: {str(e)}, trying historical_klines")

                    # Try get_historical_klines for older data
                    try:
                        # Calculate time for historical data
                        end_str = datetime.now().strftime("%d %b, %Y")
                        if timeframe in ['1h', '2h', '4h']:
                            start_str = f"{limit} hours ago UTC"
                        elif timeframe == '1d':
                            start_str = f"{limit} days ago UTC"
                        else:
                            start_str = f"{int(limit / 24)} days ago UTC"  # For minute intervals

                        self.logger.info(
                            f"Binance Historical Klines request for {binance_symbol}, interval {binance_interval}, Start {start_str}")
                        klines = client.get_historical_klines(symbol=binance_symbol, interval=binance_interval,
                                                              start_str=start_str, end_str=end_str)

                        if klines and len(klines) > 0:
                            # Convert to DataFrame
                            df = pd.DataFrame(klines, columns=[
                                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                                'close_time', 'quote_asset_volume', 'number_of_trades',
                                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                            ])

                            # Convert columns to numeric values
                            for col in ['open', 'high', 'low', 'close', 'volume']:
                                df[col] = pd.to_numeric(df[col])

                            # Convert timestamp to datetime
                            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

                            self.logger.info(f"Binance Historical data successfully retrieved: {len(df)} data points")
                            return df
                        else:
                            self.logger.warning(
                                f"Binance Historical Klines returned empty or invalid data for {binance_symbol}")
                    except Exception as e:
                        self.logger.warning(f"Error with Binance Historical Klines: {str(e)}")
        except ImportError:
            self.logger.warning("Binance Client not installed. Install with 'pip install python-binance'")
        except Exception as e:
            self.logger.warning(f"Unexpected error with Binance API: {str(e)}")

        # ATTEMPT 2: Yahoo Finance (if Binance is not available)
        try:
            self.logger.info(f"Trying Yahoo Finance for {symbol}")
            import yfinance as yf

            # Adjust symbol for Yahoo Finance
            yahoo_symbol = symbol
            if "-USDT" in symbol:
                yahoo_symbol = symbol.replace("-USDT", "-USD")

            self.logger.info(f"Querying Yahoo Finance with symbol: {yahoo_symbol}")
            ticker = yf.Ticker(yahoo_symbol)

            # Adjust timeframe
            interval_map = {'1m': '1m', '5m': '5m', '15m': '15m', '30m': '30m',
                            '1h': '1h', '2h': '2h', '4h': '4h', '1d': '1d', '1w': '1wk'}
            yahoo_interval = interval_map.get(timeframe, '1h')

            # Set period
            period_map = {'1m': '7d', '5m': '7d', '15m': '7d', '30m': '7d',
                          '1h': '60d', '2h': '60d', '4h': '60d', '1d': '730d', '1w': '5y'}
            period = period_map.get(timeframe, '60d')

            self.logger.info(f"Yahoo Finance query: period={period}, interval={yahoo_interval}")
            df = ticker.history(period=period, interval=yahoo_interval)

            if not df.empty:
                self.logger.info(
                    f"Yahoo Finance data successfully retrieved: {len(df)} data points with columns {df.columns.tolist()}")

                # IMPORTANT: Make sure the 'close' column is present
                if 'Close' in df.columns:
                    df['close'] = df['Close']
                if 'Open' in df.columns:
                    df['open'] = df['Open']
                if 'High' in df.columns:
                    df['high'] = df['High']
                if 'Low' in df.columns:
                    df['low'] = df['Low']
                if 'Volume' in df.columns:
                    df['volume'] = df['Volume']

                return df
            else:
                self.logger.warning(f"Yahoo Finance returned empty data for {yahoo_symbol}")
        except Exception as e:
            self.logger.warning(f"Error retrieving Yahoo Finance data: {str(e)}")

        # FALLBACK: Synthetic data (if everything else fails)
        self.logger.warning(f"No real data available for {symbol}, creating synthetic data")

        # Generate timestamps for the last 'limit' hours
        timestamps = [datetime.now() - timedelta(hours=i) for i in range(limit)]
        timestamps.reverse()  # Chronological order

        # Initial price based on symbol
        if 'BTC' in symbol:
            base_price = 30000.0
        elif 'ETH' in symbol:
            base_price = 2000.0
        else:
            base_price = 100.0  # Generic value for other symbols

        # Simulate price movement
        prices = []
        price = base_price
        for i in range(limit):
            # Random price change with slight trend
            change = np.random.normal(0, base_price * 0.01)  # 1% volatility
            if i % 10 < 5:  # Slight upward trend for the first 5 periods of 10
                change += base_price * 0.002
            else:
                change -= base_price * 0.001

            price += change
            prices.append(price)

        # Create dataframe
        df = pd.DataFrame({
            'timestamp': timestamps,
            'open': [p * (1 + np.random.normal(0, 0.002)) for p in prices],
            'high': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
            'low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
            'close': prices,
            'volume': [np.random.uniform(100, 1000) * (base_price / 100) for _ in range(limit)]
        })

        self.logger.info(f"Synthetic data created: {len(df)} data points with columns {df.columns.tolist()}")
        return df

    def get_news_sentiment(self, symbol):
        """Retrieves news sentiment for a symbol"""
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

                self.logger.info(f"Sentiment score for {symbol}: {sentiment_score}")
                return sentiment_score
            except Exception as e:
                self.logger.error(f"Error retrieving news sentiment: {str(e)}")
                # Fallback to dummy value

        # Return dummy value if no API key is available or an error occurred
        import random
        dummy_score = random.uniform(-0.1, 0.1)  # Small random values, close to neutral
        self.logger.info(f"Using dummy sentiment for {symbol}: {dummy_score}")
        return dummy_score

    def prepare_features(self, symbol, prediction_hours=1):
        """Prepares features for the model"""
        # Retrieve market data
        market_data = self.get_market_data(symbol, limit=168)  # 1 week of hourly data

        if market_data.empty:
            return None

        # Debug output of columns
        self.logger.info(f"Original columns in market_data: {market_data.columns.tolist()}")

        # With yfinance the columns are capitalized, with Binance they are lowercase
        # Ensure consistency
        column_mapping = {
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        }

        for old_col, new_col in column_mapping.items():
            if old_col in market_data.columns and new_col not in market_data.columns:
                market_data[new_col] = market_data[old_col]

        # Make sure all required columns are present
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in market_data.columns:
                if col == 'close' and 'Close' in market_data.columns:
                    market_data[col] = market_data['Close']
                else:
                    # Generate synthetic data for missing columns
                    self.logger.warning(f"Column {col} is missing, generating synthetic data")

                    # Set base for values
                    if col in ['open', 'high', 'low', 'close']:
                        if 'close' in market_data.columns:
                            base = market_data['close'].mean()
                        elif 'Close' in market_data.columns:
                            base = market_data['Close'].mean()
                        else:
                            base = 100.0  # Fallback

                        if col == 'high':
                            market_data[col] = base * (1 + np.random.uniform(0.001, 0.01, size=len(market_data)))
                        elif col == 'low':
                            market_data[col] = base * (1 - np.random.uniform(0.001, 0.01, size=len(market_data)))
                        else:  # open or close
                            market_data[col] = base * (1 + np.random.normal(0, 0.005, size=len(market_data)))
                    elif col == 'volume':
                        market_data[col] = np.random.uniform(100, 1000, size=len(market_data))

        # Calculate technical indicators
        try:
            market_data['rsi'] = self._calculate_rsi(market_data['close'])
            market_data['macd'], market_data['macd_signal'] = self._calculate_macd(market_data['close'])
            market_data['ema_short'] = market_data['close'].ewm(span=12).mean()
            market_data['ema_medium'] = market_data['close'].ewm(span=26).mean()
            market_data['ema_long'] = market_data['close'].ewm(span=50).mean()
            market_data['volatility'] = market_data['close'].rolling(window=24).std()
        except Exception as e:
            self.logger.error(f"Error calculating technical indicators: {str(e)}")
            # Simply continue, missing values will be replaced by NaN

        # Add sentiment data
        sentiment = self.get_news_sentiment(symbol)
        market_data['sentiment'] = sentiment

        # Handle NaN values
        market_data = market_data.fillna(method='ffill').fillna(method='bfill').fillna(0)

        # Return only the latest data for prediction
        return market_data.iloc[-48:].copy()  # 48 hours of data, create a copy

    def _calculate_rsi(self, prices, period=14):
        """Calculates the Relative Strength Index"""
        try:
            delta = prices.diff()
            # Prevent division by zero
            gain = (delta.where(delta > 0, 0)).fillna(0).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).fillna(0).rolling(window=period).mean()

            # Prevent division by zero
            loss = loss.replace(0, 0.00001)

            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            self.logger.error(f"Error calculating RSI: {e}")
            # Return a column with 50 (neutral) in case of error
            return pd.Series(50, index=prices.index)

    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculates the MACD (Moving Average Convergence Divergence)"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        return macd, macd_signal

    # Optional: This method can be implemented later when advanced functionality is needed
    def get_economic_indicators(self):
        """
        Retrieves important economic indicators

        This function is a placeholder for future extensions.
        It could be used to retrieve macroeconomic data such as inflation rates,
        GDP growth, unemployment rates, etc. and incorporate them into trading decisions.
        """
        # TODO: Implementation for economic indicators (inflation, GDP, etc.)
        return {}