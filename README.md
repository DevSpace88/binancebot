# TradeBot

TradeBot is a configurable trading bot with a predictive model and web frontend for automated analysis and trading of cryptocurrencies and other financial instruments.

## Features

- 🤖 **Predictive Model**: Uses machine learning to predict future price movements
- 📊 **Data Analysis**: Collects and analyzes market data from various APIs
- 🚀 **Automated Trading**: Automatically executes trades based on predictions
- 📱 **Modern Web Frontend**: User-friendly interface for monitoring and controlling the bot
- ⏱️ **Job Scheduler**: Plans and controls regular prediction and trading jobs
- 🔧 **Extensive Configuration**: Customizable parameters for model, trading, and risk management
- 📝 **Trading History**: Stores and displays past trades and performance

## System Requirements

- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher
- Optional: Docker for container deployment

## Installation

### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

   If there is no `requirements.txt`, install the following packages:
   ```
   pip install fastapi uvicorn pandas numpy scikit-learn joblib schedule requests yfinance
   ```

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install Node dependencies:
   ```
   npm install
   ```

3. Build frontend for production:
   ```
   npm run build
   ```

## Starting TradeBot

### All in one step (Development)

```bash
cd backend
python start.py --config config.json --port 8000
```

Optional: Start the frontend separately in development mode:
```bash
cd frontend
npm run serve
```

## Using Docker

It's recommended to use Docker since it's easier:

```
docker-compose up
```

## Configuration

The configuration file is in JSON format and contains the following sections:

### Example Configuration `config.json`:

```json
{
  "api_keys": {
    "binance": {
      "api_key": "YOUR_API_KEY",
      "api_secret": "YOUR_API_SECRET"
    },
    "news_api": "YOUR_NEWS_API_KEY"
  },
  "model": {
    "model_type": "random_forest",
    "features": ["close", "volume", "rsi", "macd", "sentiment", "ema_short", "ema_medium", "volatility"],
    "target": "close",
    "prediction_horizon": 1
  },
  "trader": {
    "trading_enabled": false,
    "exchanges": {
      "binance": {
        "api_key": "YOUR_API_KEY",
        "api_secret": "YOUR_API_SECRET",
        "test_mode": true
      }
    },
    "trade_amount": 100,
    "max_trades_per_day": 5,
    "stop_loss_pct": 2.0,
    "take_profit_pct": 3.0,
    "confidence_threshold": 0.7,
    "min_change_pct": 1.0,
    "risk_management": {
      "max_risk_per_trade": 2.0,
      "daily_drawdown_limit": 5.0
    }
  },
  "api": {
    "host": "0.0.0.0",
    "port": 8000
  }
}
```

### Configuration Parameters

#### Model Configuration
- `model_type`: Type of predictive model ("random_forest", "gradient_boosting", "linear")
- `features`: List of features to use for the model
- `target`: Target value for prediction (typically "close")
- `prediction_horizon`: Time horizon for prediction in hours

#### Trader Configuration
- `trading_enabled`: Enables or disables actual trading (false for paper-trading)
- `exchanges`: Configuration for different exchanges (such as Binance)
- `trade_amount`: Default amount per trade in the base currency
- `max_trades_per_day`: Maximum number of trades per day
- `stop_loss_pct`: Stop loss in percentage from entry price
- `take_profit_pct`: Take profit in percentage from entry price
- `confidence_threshold`: Minimum confidence for trades (0-1)
- `min_change_pct`: Minimum price change for trades in percentage
- `risk_management`: Parameters for risk management

#### API Configuration
- `host`: Hostname for the API server
- `port`: Port for the API server

## Using the Web Frontend

After starting TradeBot, the web frontend can be accessed via a browser:

```
http://localhost:8000
```

The user interface consists of five main areas:

### Dashboard
Shows an overview of the key metrics:
- Number of open trades
- Number of trades today
- Profit/loss today
- Win rate
- Performance chart
- Active symbols

### Predictions
Here you can create manual predictions for any symbol (Model is always only trained on one symbol!):
1. Enter a symbol (e.g., "BTC-USDT")
2. Select a timeframe
3. Click "Create prediction"
4. The results will be displayed and can optionally be implemented as a trade

### Trades
Shows all open and closed trades:
- Open trades: Current trades with stop-loss and take-profit
- Closed trades: Past trades with profit/loss and closing reason

### Jobs
Allows creating and managing automated prediction and trading jobs:
1. Enter a symbol
2. Select an interval (15m, 30m, 1h, 4h, 1d)
3. Click "Add job"
4. The job will run regularly and automatically execute trades when signals are appropriate

### Settings
Allows adjustment of all configuration parameters:
- General settings: Enable/disable trading, maximum number of trades, amount per trade
- Risk management: Stop-loss, take-profit, maximum risk per trade
- Model settings: Model type, prediction horizon, confidence threshold
- API keys: Access data for exchanges

## API Endpoints

TradeBot offers a RESTful API that can be used to program your own clients or integrate into other systems:

| Endpoint | Method | Description |
|----------|---------|--------------|
| `/api/status` | GET | Returns the current status of the bot |
| `/api/predict` | POST | Performs a prediction for a symbol |
| `/api/trade` | POST | Executes a manual trade |
| `/api/trades` | GET | Returns trades (open, closed, or all) |
| `/api/stats` | GET | Returns trading statistics |
| `/api/config` | POST | Updates the configuration |
| `/api/config` | GET | Returns the current configuration |
| `/api/jobs` | POST | Adds a prediction and trading job |
| `/api/jobs/{job_id}` | DELETE | Removes a job |
| `/api/jobs` | GET | Returns all active jobs |
| `/api/train` | POST | Trains the model with historical data for a symbol |

## Training the Model

Before using TradeBot for real trades, it is recommended to train the predictive model:

1. Via the API (recommended):
   ```
   curl -X POST -H "Content-Type: application/json" -d '{"symbol":"BTC-USDT"}' http://localhost:8000/api/train
   ```

2. Alternatively, the model can be trained manually:
   ```python
   from model import PredictionModel
   from data_collector import DataCollector

   # Collect market data
   collector = DataCollector()
   data = collector.get_market_data("BTC-USDT", limit=2000)

   # Calculate technical indicators
   data['rsi'] = collector._calculate_rsi(data['close'])
   data['macd'], data['macd_signal'] = collector._calculate_macd(data['close'])
   data['ema_short'] = data['close'].ewm(span=12).mean()
   data['ema_medium'] = data['close'].ewm(span=26).mean()
   data['volatility'] = data['close'].rolling(window=24).std()

   # Initialize and train model
   model = PredictionModel()
   model.train(data.dropna())
   ```

## Paper-Trading vs. Live-Trading

TradeBot supports two trading modes:

1. **Paper-Trading (Simulation Mode)**:
   - Default setting (`trading_enabled: false`)
   - All features are available, but no real trades are executed
   - Ideal for testing strategies without financial risk

2. **Live-Trading**:
   - Can be activated in settings (`trading_enabled: true`)
   - Executes real trades on the configured exchange
   - Requires valid API keys
   - WARNING: Uses real money!

## Risk Management

TradeBot has several features to minimize risk:

- **Stop-Loss**: Automatic selling when the price falls below a certain value
- **Take-Profit**: Automatic selling when the price reaches a certain value
- **Maximum Risk per Trade**: Limits the loss per trade
- **Daily Drawdown Limit**: Stops trading when daily losses exceed a certain value
- **Confidence Threshold**: Minimum confidence for trades
- **Minimum Price Change**: Minimum predicted price change for trades

## Architecture

TradeBot consists of several main modules:

1. **data_collector.py**: Collects market data from various APIs
2. **model.py**: Implements the predictive model
3. **trader.py**: Executes trading logic based on predictions
4. **scheduler.py**: Plans and controls hourly jobs
5. **api.py**: RESTful API for frontend communication
6. **app.py**: Main application that combines all components
7. **frontend/**: Web frontend for control and monitoring

## Security and Risks

**WARNING**: Trading bots can lead to financial losses. Use them with caution and make sure you understand the risks.

- This bot is just a demo, it shouldn't be used for trading at all
- Do not deploy this, this isn't safe!
- Store API keys securely and do not share them with anyone
- Start with paper-trading to understand the bot functions
- When transitioning to live-trading, start with small amounts, if you really have to and know what you're doing
- Monitor bot activities regularly
- Always set stop-loss limits to limit potential losses



### Log Files

TradeBot writes detailed logs to the file `tradebot.log`. These logs can provide valuable information when problems occur.