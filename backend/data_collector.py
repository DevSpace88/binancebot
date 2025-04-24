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

    # def get_market_data(self, symbol, timeframe='1h', limit=100):
    #     """Sammelt historische Marktdaten für ein bestimmtes Symbol"""
    #     # Beispiel für Binance API
    #     if 'binance' in self.api_keys:
    #         try:
    #             endpoint = f"https://api.binance.com/api/v3/klines"
    #             params = {
    #                 'symbol': symbol.replace('-', ''),
    #                 'interval': timeframe,
    #                 'limit': limit
    #             }
    #             response = requests.get(endpoint, params=params)
    #             data = response.json()
    #
    #             # Konvertiere Daten in DataFrame
    #             df = pd.DataFrame(data, columns=[
    #                 'timestamp', 'open', 'high', 'low', 'close', 'volume',
    #                 'close_time', 'quote_volume', 'trades', 'taker_buy_base',
    #                 'taker_buy_quote', 'ignore'
    #             ])
    #             # Konvertiere Spalten zu numerischen Werten
    #             for col in ['open', 'high', 'low', 'close', 'volume']:
    #                 df[col] = pd.to_numeric(df[col])
    #             # Konvertiere Timestamp zu datetime
    #             df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    #
    #             self.logger.info(f"Erfolgreich Daten für {symbol} abgerufen: {len(df)} Einträge")
    #             return df
    #         except Exception as e:
    #             self.logger.warning(f"Fehler bei Binance API: {str(e)}, versuche Yahoo Finance")
    #             # Kein return hier, damit wir zum Yahoo Finance Fallback gelangen
    #
    #     # Alternative: Yahoo Finance (keine API-Keys erforderlich)
    #     try:
    #         import yfinance as yf
    #         ticker = yf.Ticker(symbol)
    #         interval_map = {'1h': '1h', '1d': '1d', '15m': '15m'}
    #         df = ticker.history(period=f"{limit}{timeframe[-1]}", interval=interval_map.get(timeframe, '1h'))
    #
    #         self.logger.info(f"Erfolgreich Daten für {symbol} über Yahoo Finance abgerufen: {len(df)} Einträge")
    #         return df
    #     except Exception as e:
    #         self.logger.error(f"Fehler beim Abrufen von Marktdaten mit Yahoo Finance: {str(e)}")
    #         return pd.DataFrame()  # Leeres DataFrame zurückgeben

    # def get_market_data(self, symbol, timeframe='1h', limit=100):
    #     """Sammelt historische Marktdaten für ein bestimmtes Symbol"""
    #     self.logger.info(f"Versuche Daten für {symbol} mit Limit {limit} zu sammeln")
    #
    #     # Erste Option: Versuche mit API, wenn API Keys vorhanden
    #     api_data = self._try_api_data_collection(symbol, timeframe, limit)
    #     if not api_data.empty:
    #         return api_data
    #
    #     # Zweite Option: Versuche Yahoo Finance
    #     yahoo_data = self._try_yahoo_finance(symbol, timeframe, limit)
    #     if not yahoo_data.empty:
    #         return yahoo_data
    #
    #     # Fallback: Generiere synthetische Daten mit Warnhinweis
    #     self.logger.warning(f"Konnte keine echten Daten für {symbol} abrufen. Generiere synthetische Daten.")
    #     return self._generate_synthetic_data(symbol, limit)

    def get_market_data(self, symbol, timeframe='1h', limit=100):
        """Sammelt historische Marktdaten für ein bestimmtes Symbol"""
        self.logger.info(f"Starte Marktdatenabruf für {symbol} mit Limit {limit}")

        # VERSUCH 1: Binance API mit Python-Binance Bibliothek
        try:
            from binance.client import Client

            if 'binance' in self.api_keys and self.api_keys.get('binance', {}).get('api_key'):
                api_key = self.api_keys['binance']['api_key']
                api_secret = self.api_keys['binance'].get('api_secret', '')

                self.logger.info(f"Verwende Binance API für {symbol}")
                client = Client(api_key, api_secret)

                # Symbol für Binance anpassen (entferne Bindestrich)
                binance_symbol = symbol.replace('-', '')

                # Timeframe-Mapping für Binance
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

                # get_klines oder get_historical_klines verwenden
                try:
                    self.logger.info(
                        f"Binance Klines Anfrage für {binance_symbol}, Intervall {binance_interval}, Limit {limit}")
                    klines = client.get_klines(symbol=binance_symbol, interval=binance_interval, limit=limit)

                    if klines and len(klines) > 0:
                        # Konvertiere zu DataFrame
                        df = pd.DataFrame(klines, columns=[
                            'timestamp', 'open', 'high', 'low', 'close', 'volume',
                            'close_time', 'quote_asset_volume', 'number_of_trades',
                            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                        ])

                        # Konvertiere Spalten zu numerischen Werten
                        for col in ['open', 'high', 'low', 'close', 'volume']:
                            df[col] = pd.to_numeric(df[col])

                        # Konvertiere Timestamp zu datetime
                        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

                        self.logger.info(
                            f"Binance Daten erfolgreich abgerufen: {len(df)} Datenpunkte mit Spalten {df.columns.tolist()}")
                        return df
                except Exception as e:
                    self.logger.warning(f"Fehler bei Binance Klines: {str(e)}, versuche historical_klines")

                    # Versuche get_historical_klines für ältere Daten
                    try:
                        # Für historische Daten Zeit berechnen
                        end_str = datetime.now().strftime("%d %b, %Y")
                        if timeframe in ['1h', '2h', '4h']:
                            start_str = f"{limit} hours ago UTC"
                        elif timeframe == '1d':
                            start_str = f"{limit} days ago UTC"
                        else:
                            start_str = f"{int(limit / 24)} days ago UTC"  # Für Minuten-Intervalle

                        self.logger.info(
                            f"Binance Historical Klines Anfrage für {binance_symbol}, Intervall {binance_interval}, Start {start_str}")
                        klines = client.get_historical_klines(symbol=binance_symbol, interval=binance_interval,
                                                              start_str=start_str, end_str=end_str)

                        if klines and len(klines) > 0:
                            # Konvertiere zu DataFrame
                            df = pd.DataFrame(klines, columns=[
                                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                                'close_time', 'quote_asset_volume', 'number_of_trades',
                                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                            ])

                            # Konvertiere Spalten zu numerischen Werten
                            for col in ['open', 'high', 'low', 'close', 'volume']:
                                df[col] = pd.to_numeric(df[col])

                            # Konvertiere Timestamp zu datetime
                            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

                            self.logger.info(f"Binance Historical Daten erfolgreich abgerufen: {len(df)} Datenpunkte")
                            return df
                        else:
                            self.logger.warning(
                                f"Binance Historical Klines lieferte leere oder ungültige Daten für {binance_symbol}")
                    except Exception as e:
                        self.logger.warning(f"Fehler bei Binance Historical Klines: {str(e)}")
        except ImportError:
            self.logger.warning("Binance Client nicht installiert. Installiere mit 'pip install python-binance'")
        except Exception as e:
            self.logger.warning(f"Unerwarteter Fehler bei Binance API: {str(e)}")

        # VERSUCH 2: Yahoo Finance (wenn Binance nicht verfügbar ist)
        try:
            self.logger.info(f"Versuche Yahoo Finance für {symbol}")
            import yfinance as yf

            # Symbol anpassen für Yahoo Finance
            yahoo_symbol = symbol
            if "-USDT" in symbol:
                yahoo_symbol = symbol.replace("-USDT", "-USD")

            self.logger.info(f"Abfrage Yahoo Finance mit Symbol: {yahoo_symbol}")
            ticker = yf.Ticker(yahoo_symbol)

            # Timeframe anpassen
            interval_map = {'1m': '1m', '5m': '5m', '15m': '15m', '30m': '30m',
                            '1h': '1h', '2h': '2h', '4h': '4h', '1d': '1d', '1w': '1wk'}
            yahoo_interval = interval_map.get(timeframe, '1h')

            # Periode festlegen
            period_map = {'1m': '7d', '5m': '7d', '15m': '7d', '30m': '7d',
                          '1h': '60d', '2h': '60d', '4h': '60d', '1d': '730d', '1w': '5y'}
            period = period_map.get(timeframe, '60d')

            self.logger.info(f"Yahoo Finance Abfrage: period={period}, interval={yahoo_interval}")
            df = ticker.history(period=period, interval=yahoo_interval)

            if not df.empty:
                self.logger.info(
                    f"Yahoo Finance Daten erfolgreich abgerufen: {len(df)} Datenpunkte mit Spalten {df.columns.tolist()}")

                # WICHTIG: Stelle sicher, dass die 'close' Spalte vorhanden ist
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
                self.logger.warning(f"Yahoo Finance lieferte leere Daten für {yahoo_symbol}")
        except Exception as e:
            self.logger.warning(f"Fehler beim Abrufen von Yahoo Finance Daten: {str(e)}")

        # FALLBACK: Synthetische Daten (wenn alles andere fehlschlägt)
        self.logger.warning(f"Keine echten Daten für {symbol} verfügbar, erstelle synthetische Daten")

        # Erzeuge Zeitstempel für die letzten 'limit' Stunden
        timestamps = [datetime.now() - timedelta(hours=i) for i in range(limit)]
        timestamps.reverse()  # Chronologische Reihenfolge

        # Anfangspreis basierend auf Symbol
        if 'BTC' in symbol:
            base_price = 30000.0
        elif 'ETH' in symbol:
            base_price = 2000.0
        else:
            base_price = 100.0  # Generischer Wert für andere Symbole

        # Preisbewegung simulieren
        prices = []
        price = base_price
        for i in range(limit):
            # Zufällige Preisänderung mit leichtem Trend
            change = np.random.normal(0, base_price * 0.01)  # 1% Volatilität
            if i % 10 < 5:  # Leichter Aufwärtstrend für die ersten 5 Perioden von 10
                change += base_price * 0.002
            else:
                change -= base_price * 0.001

            price += change
            prices.append(price)

        # Dataframe erstellen
        df = pd.DataFrame({
            'timestamp': timestamps,
            'open': [p * (1 + np.random.normal(0, 0.002)) for p in prices],
            'high': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
            'low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
            'close': prices,
            'volume': [np.random.uniform(100, 1000) * (base_price / 100) for _ in range(limit)]
        })

        self.logger.info(f"Synthetische Daten erstellt: {len(df)} Datenpunkte mit Spalten {df.columns.tolist()}")
        return df


    def _try_api_data_collection(self, symbol, timeframe, limit):
        """Versucht Daten von einer API zu sammeln"""
        if 'binance' in self.api_keys:
            try:
                self.logger.info(f"Versuche Binance API für {symbol}")
                endpoint = f"https://api.binance.com/api/v3/klines"
                params = {
                    'symbol': symbol.replace('-', ''),
                    'interval': timeframe,
                    'limit': limit
                }
                self.logger.info(f"API Request: {endpoint} mit Params: {params}")
                response = requests.get(endpoint, params=params)
                if response.status_code != 200:
                    self.logger.warning(f"Binance API Fehler: Status {response.status_code}, Antwort: {response.text}")
                    return pd.DataFrame()

                data = response.json()
                if not data or len(data) == 0:
                    self.logger.warning(f"Binance API lieferte leere Daten für {symbol}")
                    return pd.DataFrame()

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

                self.logger.info(f"Erfolgreich Daten für {symbol} über Binance abgerufen: {len(df)} Einträge")
                return df
            except Exception as e:
                self.logger.warning(f"Fehler bei Binance API: {str(e)}")
                return pd.DataFrame()

        return pd.DataFrame()  # Keine API Keys vorhanden

    def _try_yahoo_finance(self, symbol, timeframe, limit):
        """Versucht Daten von Yahoo Finance zu sammeln"""
        try:
            self.logger.info(f"Versuche Yahoo Finance für {symbol}")
            import yfinance as yf
            # Bei Yahoo Finance müssen wir das Symbol anpassen (BTC-USDT -> BTC-USD)
            yahoo_symbol = symbol
            if "USDT" in symbol:
                yahoo_symbol = symbol.replace("USDT", "USD")

            self.logger.info(f"Yahoo Finance Symbol: {yahoo_symbol}")
            ticker = yf.Ticker(yahoo_symbol)

            interval_map = {'1h': '1h', '1d': '1d', '15m': '15m'}
            period_value = f"{min(limit, 10000)}d"  # Yahoo Finance hat ein Limit

            self.logger.info(
                f"Yahoo Finance Anfrage mit period={period_value}, interval={interval_map.get(timeframe, '1h')}")
            df = ticker.history(period=period_value, interval=interval_map.get(timeframe, '1h'))

            if df.empty:
                self.logger.warning(f"Yahoo Finance lieferte leere Daten für {yahoo_symbol}")
                return pd.DataFrame()

            self.logger.info(f"Erfolgreich Daten für {symbol} über Yahoo Finance abgerufen: {len(df)} Einträge")
            return df
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen von Marktdaten mit Yahoo Finance: {str(e)}")
            return pd.DataFrame()

    def _generate_synthetic_data(self, symbol, limit):
        """Generiert synthetische Marktdaten für Demo-Zwecke"""
        self.logger.info(f"Generiere Dummy-Daten für {symbol} mit Limit {limit}")

        try:
            # Erzeuge Zeitstempel für die letzen 'limit' Stunden
            timestamps = [datetime.now() - timedelta(hours=i) for i in range(limit)]
            timestamps.reverse()  # Chronologische Reihenfolge

            # Anfangspreis basierend auf Symbol
            if 'BTC' in symbol:
                base_price = 30000.0
            elif 'ETH' in symbol:
                base_price = 2000.0
            else:
                base_price = 100.0  # Generischer Wert für andere Symbole

            # Preisbewegung simulieren
            prices = []
            price = base_price
            for i in range(limit):
                # Zufällige Preisänderung mit leichtem Trend
                change = np.random.normal(0, base_price * 0.01)  # 1% Volatilität
                if i % 10 < 5:  # Leichter Aufwärtstrend für die ersten 5 Perioden von 10
                    change += base_price * 0.002
                else:
                    change -= base_price * 0.001

                price += change
                prices.append(price)

            # Dataframe erstellen
            df = pd.DataFrame({
                'timestamp': timestamps,
                'open': [p * (1 + np.random.normal(0, 0.002)) for p in prices],
                'high': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
                'low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
                'close': prices,
                'volume': [np.random.uniform(100, 1000) * (base_price / 100) for _ in range(limit)]
            })

            self.logger.info(f"Erfolgreich Dummy-Daten für {symbol} generiert: {len(df)} Einträge")
            return df

        except Exception as e:
            self.logger.error(f"Fehler beim Generieren von Dummy-Daten: {str(e)}")
            # Hier leeres DataFrame zurückgeben, damit die Fehlerbehandlung im API-Code greift
            return pd.DataFrame()

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

        # Debug-Ausgabe der Spalten
        self.logger.info(f"Original columns in market_data: {market_data.columns.tolist()}")

        # Bei yfinance sind die Spalten großgeschrieben, bei Binance kleingeschrieben
        # Stellen wir Konsistenz sicher
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

        # Stellen wir sicher, dass alle erforderlichen Spalten da sind
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in market_data.columns:
                if col == 'close' and 'Close' in market_data.columns:
                    market_data[col] = market_data['Close']
                else:
                    # Generiere synthetische Daten für fehlende Spalten
                    self.logger.warning(f"Spalte {col} fehlt, generiere synthetische Daten")

                    # Basis für Werte festlegen
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
                        else:  # open oder close
                            market_data[col] = base * (1 + np.random.normal(0, 0.005, size=len(market_data)))
                    elif col == 'volume':
                        market_data[col] = np.random.uniform(100, 1000, size=len(market_data))

        # Technische Indikatoren berechnen
        try:
            market_data['rsi'] = self._calculate_rsi(market_data['close'])
            market_data['macd'], market_data['macd_signal'] = self._calculate_macd(market_data['close'])
            market_data['ema_short'] = market_data['close'].ewm(span=12).mean()
            market_data['ema_medium'] = market_data['close'].ewm(span=26).mean()
            market_data['ema_long'] = market_data['close'].ewm(span=50).mean()
            market_data['volatility'] = market_data['close'].rolling(window=24).std()
        except Exception as e:
            self.logger.error(f"Fehler beim Berechnen der technischen Indikatoren: {str(e)}")
            # Einfach weitermachen, fehlende Werte werden durch NaN ersetzt

        # Sentiment-Daten hinzufügen
        sentiment = self.get_news_sentiment(symbol)
        market_data['sentiment'] = sentiment

        # NaN-Werte behandeln
        market_data = market_data.fillna(method='ffill').fillna(method='bfill').fillna(0)

        # Nur die neuesten Daten für Prognose zurückgeben
        return market_data.iloc[-48:].copy()  # 48 Stunden Daten, Kopie erstellen

    def _calculate_rsi(self, prices, period=14):
        """Berechnet den Relative Strength Index"""
        try:
            delta = prices.diff()
            # Verhindere Division durch Null
            gain = (delta.where(delta > 0, 0)).fillna(0).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).fillna(0).rolling(window=period).mean()

            # Verhindere Division durch Null
            loss = loss.replace(0, 0.00001)

            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            self.logger.error(f"Fehler bei RSI-Berechnung: {e}")
            # Rückgabe einer Spalte mit 50 (neutral) im Fehlerfall
            return pd.Series(50, index=prices.index)

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