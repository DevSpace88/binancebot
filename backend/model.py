# model.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
import joblib
import os
import logging
from typing import Dict, Any, Optional, Tuple, Union

logging.basicConfig(level=logging.INFO)


class PredictionModel:
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initializes the prediction model

        Args:
            config: Configuration parameters for the model
        """
        self.config = config or {
            'model_type': 'random_forest',  # 'random_forest', 'gradient_boosting', 'linear'
            'features': ['close', 'volume', 'rsi', 'macd', 'sentiment', 'ema_short', 'ema_medium', 'volatility'],
            'target': 'close',
            'prediction_horizon': 1,  # in hours
            'lookback_window': 24,  # how many past time steps to consider
            'train_test_split': 0.8,
            'model_params': {
                'random_forest': {
                    'n_estimators': 100,
                    'max_depth': 10
                },
                'gradient_boosting': {
                    'n_estimators': 100,
                    'learning_rate': 0.1
                }
            }
        }
        self.model = None
        self.scaler = StandardScaler()
        self.logger = logging.getLogger('PredictionModel')
        self.models_dir = 'models'
        os.makedirs(self.models_dir, exist_ok=True)

    def _create_model(self) -> Any:
        """Creates a new model based on the configuration"""
        model_type = self.config.get('model_type', 'random_forest')

        if model_type == 'random_forest':
            params = self.config.get('model_params', {}).get('random_forest', {})
            return RandomForestRegressor(
                n_estimators=params.get('n_estimators', 100),
                max_depth=params.get('max_depth', 10),
                random_state=42
            )
        elif model_type == 'gradient_boosting':
            params = self.config.get('model_params', {}).get('gradient_boosting', {})
            return GradientBoostingRegressor(
                n_estimators=params.get('n_estimators', 100),
                learning_rate=params.get('learning_rate', 0.1),
                random_state=42
            )
        elif model_type == 'linear':
            return LinearRegression()
        else:
            raise ValueError(f"Unknown model type: {model_type}")

    def prepare_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepares data for training or prediction

        Args:
            df: DataFrame with market data

        Returns:
            X: Features for the model
            y: Target values (only if available)
        """
        # Check if all required features are present
        selected_features = [f for f in self.config['features'] if f in df.columns]

        if not selected_features:
            raise ValueError("None of the specified features are present in the DataFrame")

        # Extract features and target values
        X = df[selected_features].values

        # Scale the features
        X = self.scaler.fit_transform(X)

        # Extract target values, if available
        target = self.config.get('target', 'close')
        y = None
        if target in df.columns:
            # Shift target values by prediction_horizon
            horizon = self.config.get('prediction_horizon', 1)
            y = df[target].shift(-horizon).dropna().values
            # Truncate X accordingly if y is smaller
            if len(y) < len(X):
                X = X[:len(y)]

        return X, y

    def train(self, df: pd.DataFrame) -> None:
        """
        Trains the model with the provided data

        Args:
            df: DataFrame with market data
        """
        try:
            X, y = self.prepare_data(df)

            if y is None or len(y) == 0:
                raise ValueError("No target values (y) available for training")

            # Create model
            self.model = self._create_model()

            # Train model
            self.model.fit(X, y)

            self.logger.info(f"Model successfully trained: {self.config['model_type']}")

            # Save model
            self.save_model()

        except Exception as e:
            self.logger.error(f"Error training the model: {str(e)}")

    def predict(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Makes a prediction with the trained model

        Args:
            df: DataFrame with current market data

        Returns:
            Dictionary with prediction results
        """
        try:
            if self.model is None:
                # Try to load a saved model
                self.load_model()
                if self.model is None:
                    # If no model can be loaded, train a simple one with the available data
                    self.logger.warning("No trained model available, training simple model")
                    self.model = self._create_model()
                    # Minimal training with available data
                    X, y = self.prepare_data(df)
                    if y is not None and len(y) > 0:
                        self.model.fit(X[:len(y)], y)
                    else:
                        # If no target variable is available, do a dummy training
                        self.model.fit(X, np.random.normal(0, 0.01, size=len(X)))

            # Debug information
            self.logger.info(f"DataFrame for prediction: Columns: {df.columns.tolist()}, Shape: {df.shape}")

            # Ensure that 'close' is in the features
            if 'close' not in df.columns and 'Close' in df.columns:
                df['close'] = df['Close']

            # Ensure that the data contains no missing values
            df_clean = df.fillna(method='ffill').fillna(method='bfill').fillna(0)

            X, _ = self.prepare_data(df_clean)

            # Make prediction
            pred_value = self.model.predict(X[-1].reshape(1, -1))[0]

            # Get current value for comparison
            current_value = df_clean[self.config.get('target', 'close')].iloc[-1]

            # Compile results
            result = {
                'prediction': float(pred_value),  # Ensure it's a normal Python float
                'current': float(current_value),
                'change': float(pred_value - current_value),
                'change_pct': float((pred_value - current_value) / current_value * 100),
                'direction': 'up' if pred_value > current_value else 'down',
                'timestamp': pd.Timestamp.now().isoformat(),
                'confidence': float(self._get_prediction_confidence(X[-1].reshape(1, -1))),
                'horizon': self.config.get('prediction_horizon', 1)
            }

            self.logger.info(f"Prediction: Current={current_value:.2f}, " +
                             f"Forecast={pred_value:.2f}, Change={result['change_pct']:.2f}%")

            return result

        except Exception as e:
            self.logger.error(f"Error making prediction: {str(e)}")
            return {
                'error': str(e),
                'timestamp': pd.Timestamp.now().isoformat()
            }

    def _get_prediction_confidence(self, X: np.ndarray) -> float:
        """
        Calculates a confidence measure for the prediction

        Args:
            X: Features for the prediction

        Returns:
            Confidence value between 0 and 1
        """
        if hasattr(self.model, 'predict_proba'):
            # For models with probability estimation
            try:
                proba = self.model.predict_proba(X)
                return np.max(proba)
            except:
                pass

        # For RandomForest: Standard deviation of tree predictions
        if isinstance(self.model, RandomForestRegressor):
            predictions = [tree.predict(X)[0] for tree in self.model.estimators_]
            return 1.0 - (np.std(predictions) / np.mean(predictions))

        # Fallback
        return 0.8

    def save_model(self) -> None:
        """Saves the trained model and the scaler"""
        if self.model is not None:
            try:
                model_name = f"{self.config['model_type']}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}"
                joblib.dump(self.model, os.path.join(self.models_dir, f"{model_name}.joblib"))
                joblib.dump(self.scaler, os.path.join(self.models_dir, f"{model_name}_scaler.joblib"))

                # Save config
                with open(os.path.join(self.models_dir, f"{model_name}_config.json"), 'w') as f:
                    import json
                    json.dump(self.config, f)

                self.logger.info(f"Model successfully saved as {model_name}")
            except Exception as e:
                self.logger.error(f"Error saving the model: {str(e)}")

    def load_model(self, model_name: Optional[str] = None) -> bool:
        """
        Loads a saved model

        Args:
            model_name: Name of the model to load, if None the newest model is loaded

        Returns:
            True if successful, otherwise False
        """
        try:
            if model_name is None:
                # Find newest model
                model_files = [f for f in os.listdir(self.models_dir) if
                               f.endswith('.joblib') and not f.endswith('_scaler.joblib')]
                if not model_files:
                    self.logger.warning("No saved models found")
                    return False

                model_files.sort(reverse=True)  # Newest first
                model_name = model_files[0].replace('.joblib', '')

            # Load model
            self.model = joblib.load(os.path.join(self.models_dir, f"{model_name}.joblib"))

            # Load scaler
            scaler_path = os.path.join(self.models_dir, f"{model_name}_scaler.joblib")
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)

            # Load config
            config_path = os.path.join(self.models_dir, f"{model_name}_config.json")
            if os.path.exists(config_path):
                import json
                with open(config_path, 'r') as f:
                    self.config = json.load(f)

            self.logger.info(f"Model {model_name} successfully loaded")
            return True

        except Exception as e:
            self.logger.error(f"Error loading the model: {str(e)}")
            return False

    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Updates the model configuration

        Args:
            new_config: New configuration parameters
        """
        self.config.update(new_config)
        self.logger.info(f"Model configuration updated: {new_config}")