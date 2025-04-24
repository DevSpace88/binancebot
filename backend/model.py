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
        Initialisiert das Prädiktionsmodell

        Args:
            config: Konfigurationsparameter für das Modell
        """
        self.config = config or {
            'model_type': 'random_forest',  # 'random_forest', 'gradient_boosting', 'linear'
            'features': ['close', 'volume', 'rsi', 'macd', 'sentiment', 'ema_short', 'ema_medium', 'volatility'],
            'target': 'close',
            'prediction_horizon': 1,  # in Stunden
            'lookback_window': 24,  # wie viele vergangene Zeitschritte betrachten
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
        """Erstellt ein neues Modell basierend auf der Konfiguration"""
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
            raise ValueError(f"Unbekannter Modelltyp: {model_type}")

    def prepare_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Bereitet Daten für Training oder Vorhersage vor

        Args:
            df: DataFrame mit Marktdaten

        Returns:
            X: Features für das Modell
            y: Zielwerte (nur wenn verfügbar)
        """
        # Überprüfen, ob alle erforderlichen Features vorhanden sind
        selected_features = [f for f in self.config['features'] if f in df.columns]

        if not selected_features:
            raise ValueError("Keine der angegebenen Features sind im DataFrame vorhanden")

        # Features und Zielwerte extrahieren
        X = df[selected_features].values

        # Skalieren der Features
        X = self.scaler.fit_transform(X)

        # Zielwerte extrahieren, falls verfügbar
        target = self.config.get('target', 'close')
        y = None
        if target in df.columns:
            # Target-Werte um prediction_horizon verschieben
            horizon = self.config.get('prediction_horizon', 1)
            y = df[target].shift(-horizon).dropna().values
            # X entsprechend kürzen, wenn y kleiner ist
            if len(y) < len(X):
                X = X[:len(y)]

        return X, y

    def train(self, df: pd.DataFrame) -> None:
        """
        Trainiert das Modell mit den bereitgestellten Daten

        Args:
            df: DataFrame mit Marktdaten
        """
        try:
            X, y = self.prepare_data(df)

            if y is None or len(y) == 0:
                raise ValueError("Keine Zielwerte (y) für das Training verfügbar")

            # Modell erstellen
            self.model = self._create_model()

            # Modell trainieren
            self.model.fit(X, y)

            self.logger.info(f"Modell erfolgreich trainiert: {self.config['model_type']}")

            # Modell speichern
            self.save_model()

        except Exception as e:
            self.logger.error(f"Fehler beim Training des Modells: {str(e)}")

    def predict(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Führt eine Vorhersage mit dem trainierten Modell durch

        Args:
            df: DataFrame mit aktuellen Marktdaten

        Returns:
            Dictionary mit Vorhersageergebnissen
        """
        try:
            if self.model is None:
                # Versuche, ein gespeichertes Modell zu laden
                self.load_model()
                if self.model is None:
                    # Wenn kein Modell geladen werden kann, trainiere ein einfaches mit den vorhandenen Daten
                    self.logger.warning("Kein trainiertes Modell verfügbar, trainiere einfaches Modell")
                    self.model = self._create_model()
                    # Minimales Training mit den vorhandenen Daten
                    X, y = self.prepare_data(df)
                    if y is not None and len(y) > 0:
                        self.model.fit(X[:len(y)], y)
                    else:
                        # Wenn keine Zielvariable verfügbar ist, mache ein Dummy-Training
                        self.model.fit(X, np.random.normal(0, 0.01, size=len(X)))

            # Debug-Informationen
            self.logger.info(f"DataFrame für Vorhersage: Spalten: {df.columns.tolist()}, Shape: {df.shape}")

            # Sicherstellen, dass 'close' in den Features ist
            if 'close' not in df.columns and 'Close' in df.columns:
                df['close'] = df['Close']

            # Stellen sicher, dass die Daten keine Fehlwerte enthalten
            df_clean = df.fillna(method='ffill').fillna(method='bfill').fillna(0)

            X, _ = self.prepare_data(df_clean)

            # Vorhersage machen
            pred_value = self.model.predict(X[-1].reshape(1, -1))[0]

            # Aktuellen Wert holen für Vergleich
            current_value = df_clean[self.config.get('target', 'close')].iloc[-1]

            # Ergebnisse zusammenstellen
            result = {
                'prediction': float(pred_value),  # Sicherstellen, dass es ein normaler Python-Float ist
                'current': float(current_value),
                'change': float(pred_value - current_value),
                'change_pct': float((pred_value - current_value) / current_value * 100),
                'direction': 'up' if pred_value > current_value else 'down',
                'timestamp': pd.Timestamp.now().isoformat(),
                'confidence': float(self._get_prediction_confidence(X[-1].reshape(1, -1))),
                'horizon': self.config.get('prediction_horizon', 1)
            }

            self.logger.info(f"Vorhersage: Aktuell={current_value:.2f}, " +
                             f"Prognose={pred_value:.2f}, Änderung={result['change_pct']:.2f}%")

            return result

        except Exception as e:
            self.logger.error(f"Fehler bei der Vorhersage: {str(e)}")
            return {
                'error': str(e),
                'timestamp': pd.Timestamp.now().isoformat()
            }

    def _get_prediction_confidence(self, X: np.ndarray) -> float:
        """
        Berechnet ein Konfidenzmaß für die Vorhersage

        Args:
            X: Features für die Vorhersage

        Returns:
            Konfidenzwert zwischen 0 und 1
        """
        if hasattr(self.model, 'predict_proba'):
            # Für Modelle mit Wahrscheinlichkeitsabschätzung
            try:
                proba = self.model.predict_proba(X)
                return np.max(proba)
            except:
                pass

        # Für RandomForest: Standardabweichung der Baumvorhersagen
        if isinstance(self.model, RandomForestRegressor):
            predictions = [tree.predict(X)[0] for tree in self.model.estimators_]
            return 1.0 - (np.std(predictions) / np.mean(predictions))

        # Fallback
        return 0.8

    def save_model(self) -> None:
        """Speichert das trainierte Modell und den Scaler"""
        if self.model is not None:
            try:
                model_name = f"{self.config['model_type']}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}"
                joblib.dump(self.model, os.path.join(self.models_dir, f"{model_name}.joblib"))
                joblib.dump(self.scaler, os.path.join(self.models_dir, f"{model_name}_scaler.joblib"))

                # Config speichern
                with open(os.path.join(self.models_dir, f"{model_name}_config.json"), 'w') as f:
                    import json
                    json.dump(self.config, f)

                self.logger.info(f"Modell erfolgreich gespeichert als {model_name}")
            except Exception as e:
                self.logger.error(f"Fehler beim Speichern des Modells: {str(e)}")

    def load_model(self, model_name: Optional[str] = None) -> bool:
        """
        Lädt ein gespeichertes Modell

        Args:
            model_name: Name des zu ladenden Modells, wenn None wird das neueste Modell geladen

        Returns:
            True wenn erfolgreich, sonst False
        """
        try:
            if model_name is None:
                # Neuestes Modell finden
                model_files = [f for f in os.listdir(self.models_dir) if
                               f.endswith('.joblib') and not f.endswith('_scaler.joblib')]
                if not model_files:
                    self.logger.warning("Keine gespeicherten Modelle gefunden")
                    return False

                model_files.sort(reverse=True)  # Neueste zuerst
                model_name = model_files[0].replace('.joblib', '')

            # Modell laden
            self.model = joblib.load(os.path.join(self.models_dir, f"{model_name}.joblib"))

            # Scaler laden
            scaler_path = os.path.join(self.models_dir, f"{model_name}_scaler.joblib")
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)

            # Config laden
            config_path = os.path.join(self.models_dir, f"{model_name}_config.json")
            if os.path.exists(config_path):
                import json
                with open(config_path, 'r') as f:
                    self.config = json.load(f)

            self.logger.info(f"Modell {model_name} erfolgreich geladen")
            return True

        except Exception as e:
            self.logger.error(f"Fehler beim Laden des Modells: {str(e)}")
            return False

    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Aktualisiert die Modellkonfiguration

        Args:
            new_config: Neue Konfigurationsparameter
        """
        self.config.update(new_config)
        self.logger.info(f"Modellkonfiguration aktualisiert: {new_config}")


