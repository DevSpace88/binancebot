# TradeBot

TradeBot ist ein konfigurierbarer Handelsbot mit prädiktivem Modell und Web-Frontend für die automatisierte Analyse und den Handel von Kryptowährungen und anderen Finanzinstrumenten.

## Funktionen

- 🤖 **Prädiktives Modell**: Verwendet maschinelles Lernen, um zukünftige Preisbewegungen vorherzusagen
- 📊 **Datenanalyse**: Sammelt und analysiert Marktdaten von verschiedenen APIs
- 🚀 **Automatisierter Handel**: Führt automatisch Trades basierend auf Vorhersagen durch
- 📱 **Modernes Web-Frontend**: Benutzerfreundliche Oberfläche zur Überwachung und Steuerung des Bots
- ⏱️ **Job-Scheduler**: Plant und steuert regelmäßige Prognose- und Handelsjobs
- 🔧 **Umfangreiche Konfiguration**: Anpassbare Parameter für Modell, Handel und Risikomanagement
- 📝 **Handelshistorie**: Speichert und zeigt vergangene Trades und Performance

## Systemanforderungen

- Python 3.8 oder höher
- Node.js 14 oder höher
- npm 6 oder höher
- Optional: Docker für Container-Deployment

## Installation

### Backend

1. Ins Backend-Verzeichnis wechseln:
   ```
   cd backend
   ```

2. Python-Abhängigkeiten installieren:
   ```
   pip install -r requirements.txt
   ```

   Wenn keine `requirements.txt` vorhanden ist, installiere die folgenden Pakete:
   ```
   pip install fastapi uvicorn pandas numpy scikit-learn joblib schedule requests yfinance
   ```

### Frontend

1. Ins Frontend-Verzeichnis wechseln:
   ```
   cd frontend
   ```

2. Node-Abhängigkeiten installieren:
   ```
   npm install
   ```

3. Frontend für Produktion bauen:
   ```
   npm run build
   ```



## Starten des TradeBot

### Alles in einem Schritt (Entwicklung)

```bash
cd backend
python start.py --config config.json --port 8000
```

Optional: Starte das Frontend separat im Entwicklungsmodus:
```bash
cd frontend
npm run serve
```

### Produktionsumgebung

1. Frontend bauen:
   ```bash
   cd frontend
   npm run build
   ```

2. Backend mit der Konfigurationsdatei starten:
   ```bash
   cd backend
   python start.py --config config.json
   ```

## Docker verwenden

Es empfiehlt sich auch lokal einfach Docker zu verwenden:

```
docker-compose up
```

## Konfiguration

Die Konfigurationsdatei ist im JSON-Format und enthält folgende Abschnitte:

### Beispiel-Konfiguration `config.json`:

```json
{
  "api_keys": {
    "binance": {
      "api_key": "DEIN_API_KEY",
      "api_secret": "DEIN_API_SECRET"
    },
    "news_api": "DEIN_NEWS_API_KEY"
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
        "api_key": "DEIN_API_KEY",
        "api_secret": "DEIN_API_SECRET",
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

### Konfigurationsparameter

#### Modell-Konfiguration
- `model_type`: Typ des prädiktiven Modells ("random_forest", "gradient_boosting", "linear")
- `features`: Liste der zu verwendenden Features für das Modell
- `target`: Zielwert für die Vorhersage (in der Regel "close")
- `prediction_horizon`: Zeithorizont für die Vorhersage in Stunden

#### Trader-Konfiguration
- `trading_enabled`: Aktiviert oder deaktiviert den tatsächlichen Handel (false für Paper-Trading)
- `exchanges`: Konfiguration für verschiedene Börsen (wie Binance)
- `trade_amount`: Standardbetrag pro Trade in der Basiswährung
- `max_trades_per_day`: Maximale Anzahl von Trades pro Tag
- `stop_loss_pct`: Stop-Loss in Prozent vom Einstiegspreis
- `take_profit_pct`: Take-Profit in Prozent vom Einstiegspreis
- `confidence_threshold`: Mindestvertrauen für Trades (0-1)
- `min_change_pct`: Mindestpreisänderung für Trades in Prozent
- `risk_management`: Parameter für das Risikomanagement

#### API-Konfiguration
- `host`: Hostname für den API-Server
- `port`: Port für den API-Server

## Verwendung des Web-Frontends

Nach dem Start des TradeBot kann auf das Web-Frontend über einen Browser zugegriffen werden:

```
http://localhost:8000
```

Die Benutzeroberfläche besteht aus fünf Hauptbereichen:

### Dashboard
Zeigt eine Übersicht der wichtigsten Kennzahlen:
- Anzahl der offenen Trades
- Anzahl der Trades heute
- Gewinn/Verlust heute
- Gewinnrate
- Performance-Diagramm
- Aktive Symbole

### Prognosen
Hier können manuelle Prognosen für beliebige Symbole erstellt werden:
1. Symbol eingeben (z.B. "BTC-USDT")
2. Zeitrahmen auswählen
3. "Prognose erstellen" klicken
4. Die Ergebnisse werden angezeigt und können optional in einen Trade umgesetzt werden

### Trades
Zeigt alle offenen und geschlossenen Trades an:
- Offene Trades: Aktuelle Trades mit Stop-Loss und Take-Profit
- Geschlossene Trades: Vergangene Trades mit Gewinn/Verlust und Schließungsgrund

### Jobs
Ermöglicht das Erstellen und Verwalten von automatisierten Prognose- und Handelsjobs:
1. Symbol eingeben
2. Intervall auswählen (15m, 30m, 1h, 4h, 1d)
3. "Job hinzufügen" klicken
4. Der Job wird regelmäßig ausgeführt und führt bei entsprechenden Signalen automatisch Trades durch

### Einstellungen
Erlaubt die Anpassung aller Konfigurationsparameter:
- Allgemeine Einstellungen: Trading aktivieren/deaktivieren, maximale Anzahl von Trades, Betrag pro Trade
- Risikomanagement: Stop-Loss, Take-Profit, maximales Risiko pro Trade
- Modelleinstellungen: Modelltyp, Prognosehorizont, Vertrauensschwelle
- API-Schlüssel: Zugangsdaten für Börsen

## API-Endpunkte

TradeBot bietet eine RESTful API, die zur Programmierung eigener Clients oder zur Integration in andere Systeme genutzt werden kann:

| Endpunkt | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/status` | GET | Gibt den aktuellen Status des Bots zurück |
| `/api/predict` | POST | Führt eine Prognose für ein Symbol durch |
| `/api/trade` | POST | Führt einen manuellen Trade aus |
| `/api/trades` | GET | Gibt die Trades zurück (offene, geschlossene oder alle) |
| `/api/stats` | GET | Gibt Handelsstatistiken zurück |
| `/api/config` | POST | Aktualisiert die Konfiguration |
| `/api/config` | GET | Gibt die aktuelle Konfiguration zurück |
| `/api/jobs` | POST | Fügt einen Prognose- und Handelsjob hinzu |
| `/api/jobs/{job_id}` | DELETE | Entfernt einen Job |
| `/api/jobs` | GET | Gibt alle aktiven Jobs zurück |
| `/api/train` | POST | Trainiert das Modell mit historischen Daten für ein Symbol |

## Trainieren des Modells

Vor der Verwendung des TradeBot für reale Trades wird empfohlen, das prädiktive Modell zu trainieren:

1. Über die API (empfohlen):
   ```
   curl -X POST -H "Content-Type: application/json" -d '{"symbol":"BTC-USDT"}' http://localhost:8000/api/train
   ```

2. Alternativ kann das Modell auch manuell trainiert werden:
   ```python
   from model import PredictionModel
   from data_collector import DataCollector

   # Marktdaten sammeln
   collector = DataCollector()
   data = collector.get_market_data("BTC-USDT", limit=2000)

   # Technische Indikatoren berechnen
   data['rsi'] = collector._calculate_rsi(data['close'])
   data['macd'], data['macd_signal'] = collector._calculate_macd(data['close'])
   data['ema_short'] = data['close'].ewm(span=12).mean()
   data['ema_medium'] = data['close'].ewm(span=26).mean()
   data['volatility'] = data['close'].rolling(window=24).std()

   # Modell initialisieren und trainieren
   model = PredictionModel()
   model.train(data.dropna())
   ```

## Paper-Trading vs. Live-Trading

TradeBot unterstützt zwei Trading-Modi:

1. **Paper-Trading (Simulationsmodus)**:
   - Standard-Einstellung (`trading_enabled: false`)
   - Alle Funktionen sind verfügbar, aber keine echten Trades werden ausgeführt
   - Ideal zum Testen von Strategien ohne finanzielles Risiko

2. **Live-Trading**:
   - Aktivierbar über Einstellungen (`trading_enabled: true`)
   - Führt echte Trades auf der konfigurierten Börse durch
   - Erfordert gültige API-Schlüssel
   - ACHTUNG: Verwendet echtes Geld!

## Risikomanagement

TradeBot verfügt über mehrere Funktionen zur Risikominimierung:

- **Stop-Loss**: Automatischer Verkauf, wenn der Preis unter einen bestimmten Wert fällt
- **Take-Profit**: Automatischer Verkauf, wenn der Preis einen bestimmten Wert erreicht
- **Maximales Risiko pro Trade**: Begrenzt den Verlust pro Trade
- **Tägliches Drawdown-Limit**: Stoppt den Handel, wenn die täglichen Verluste einen bestimmten Wert überschreiten
- **Vertrauensschwelle**: Minimale Konfidenz für Trades
- **Mindestpreisänderung**: Minimale prognostizierte Preisänderung für Trades

## Architektur

TradeBot besteht aus mehreren Hauptmodulen:

1. **data_collector.py**: Sammelt Marktdaten von verschiedenen APIs
2. **model.py**: Implementiert das prädiktive Modell
3. **trader.py**: Führt Handelslogik basierend auf Vorhersagen aus
4. **scheduler.py**: Plant und steuert stündliche Jobs
5. **api.py**: RESTful API für Frontend-Kommunikation
6. **app.py**: Hauptanwendung, die alle Komponenten zusammenführt
7. **frontend/**: Web-Frontend zur Steuerung und Überwachung

## Sicherheit und Risiken

**WARNUNG**: Trading-Bots können zu finanziellen Verlusten führen. Verwende sie mit Vorsicht und stelle sicher, dass du die Risiken verstehst.

- Speichere API-Schlüssel sicher und teile sie niemandem mit
- Beginne mit Paper-Trading, um die Bot-Funktionen zu verstehen
- Verwende beim Übergang zum Live-Trading zunächst kleine Beträge
- Überwache die Bot-Aktivitäten regelmäßig
- Setze immer Stop-Loss-Limits, um potenzielle Verluste zu begrenzen

## Fehlersuche

### Bekannte Probleme und Lösungen

1. **Problem**: Bot kann keine Verbindung zur Börsen-API herstellen
   **Lösung**: Überprüfe deine API-Schlüssel und Internetverbindung

2. **Problem**: Prognosen werden nicht erstellt
   **Lösung**: Stelle sicher, dass die Datenquellen verfügbar sind und das Modell trainiert wurde

3. **Problem**: Rekursionsfehler in den Einstellungs-Komponenten
   **Lösung**: Dies ist ein bekanntes Problem in den Vue-Komponenten. Die Lösung besteht darin, die Watchers und Event-Emitter zu überarbeiten, um Endlosschleifen zu vermeiden.

4. **Problem**: Fehlermeldung "Maximum recursive updates exceeded in component <SettingsPage>"
   **Lösung**: Verwende die korrigierten Komponenten für die Einstellungsseite, die die bidirektionale Bindung richtig handhaben.

5. **Problem**: Frontend lädt nicht
   **Lösung**: Stelle sicher, dass das Frontend gebaut wurde und die Dateien im richtigen Verzeichnis liegen

### Logdateien

TradeBot schreibt detaillierte Logs in die Datei `tradebot.log`. Bei Problemen können diese Logs wertvolle Hinweise liefern.

## Beitragen

Beiträge zum Projekt sind willkommen! Um beizutragen:

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/amazing-feature`)
3. Committe deine Änderungen (`git commit -m 'Add amazing feature'`)
4. Push zum Branch (`git push origin feature/amazing-feature`)
5. Öffne einen Pull Request

## Lizenz

Dieses Projekt steht unter einer offenen Lizenz - siehe die LICENSE-Datei für Details.

## Anpassungen und Erweiterungen

TradeBot kann an deine spezifischen Bedürfnisse angepasst werden:

- **Unterstützung für weitere Börsen**: Implementiere Adapter für andere Handelsplattformen
- **Zusätzliche technische Indikatoren**: Erweitere die Sammlung von Features für das prädiktive Modell
- **Alternative ML-Modelle**: Implementiere weitere Algorithmen wie neuronale Netze
- **Erweiterte Benachrichtigungen**: Füge E-Mail- oder SMS-Benachrichtigungen hinzu
- **Backtesting-Funktionalität**: Teste Strategien mit historischen Daten
- **Portfolio-Management**: Optimiere die Allokation über mehrere Vermögenswerte hinweg