<template>
  <div class="container">
    <header>
      <h1>TradeBot - Prädiktiver Handelsbot</h1>
      <div class="status-indicator" :class="{ active: isActive }">
        {{ isActive ? 'Aktiv' : 'Inaktiv' }}
      </div>
    </header>

    <div class="main-content">
      <div class="sidebar">
        <nav>
          <button @click="activeTab = 'dashboard'" :class="{ active: activeTab === 'dashboard' }">Dashboard</button>
          <button @click="activeTab = 'predictions'" :class="{ active: activeTab === 'predictions' }">Prognosen</button>
          <button @click="activeTab = 'trades'" :class="{ active: activeTab === 'trades' }">Trades</button>
          <button @click="activeTab = 'jobs'" :class="{ active: activeTab === 'jobs' }">Jobs</button>
          <button @click="activeTab = 'settings'" :class="{ active: activeTab === 'settings' }">Einstellungen</button>
        </nav>
      </div>

      <div class="content">
        <!-- Dashboard -->
        <div v-if="activeTab === 'dashboard'" class="tab-content">
          <h2>Dashboard</h2>

          <div class="stats-grid">
            <div class="stat-card">
              <h3>Offene Trades</h3>
              <div class="stat-value">{{ stats.open_trades || 0 }}</div>
            </div>

            <div class="stat-card">
              <h3>Trades Heute</h3>
              <div class="stat-value">{{ stats.daily_trades || 0 }}</div>
            </div>

            <div class="stat-card">
              <h3>Gewinn/Verlust Heute</h3>
              <div class="stat-value" :class="{ positive: stats.daily_profit_loss > 0, negative: stats.daily_profit_loss < 0 }">
                {{ stats.daily_profit_loss ? stats.daily_profit_loss.toFixed(2) + '%' : '0.00%' }}
              </div>
            </div>

            <div class="stat-card">
              <h3>Gewinnrate</h3>
              <div class="stat-value">{{ stats.win_rate ? stats.win_rate.toFixed(2) + '%' : '0.00%' }}</div>
            </div>
          </div>

          <div class="chart-container">
            <h3>Performance Übersicht</h3>
            <canvas ref="performanceChart" width="400" height="200"></canvas>
          </div>

          <div class="active-symbols">
            <h3>Aktive Symbole</h3>
            <div class="symbols-list">
              <div v-for="job in jobs" :key="job.id" class="symbol-item">
                <div class="symbol-name">{{ extractSymbol(job.id) }}</div>
                <div class="symbol-next-run">Nächste Prognose: {{ job.next_run }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Prognosen -->
        <div v-if="activeTab === 'predictions'" class="tab-content">
          <h2>Prognosen</h2>

          <div class="prediction-form">
            <h3>Neue Prognose</h3>
            <div class="form-group">
              <label for="prediction-symbol">Symbol</label>
              <input type="text" id="prediction-symbol" v-model="predictionForm.symbol" placeholder="z.B. BTC-USDT">
            </div>

            <div class="form-group">
              <label for="prediction-timeframe">Zeitrahmen</label>
              <select id="prediction-timeframe" v-model="predictionForm.timeframe">
                <option value="1h">1 Stunde</option>
                <option value="4h">4 Stunden</option>
                <option value="1d">1 Tag</option>
              </select>
            </div>

            <button @click="makePrediction" class="primary-button">Prognose erstellen</button>
          </div>

          <div v-if="latestPrediction" class="prediction-result">
            <h3>Letzte Prognose</h3>
            <div class="prediction-card">
              <div class="prediction-header">
                <div class="prediction-symbol">{{ latestPrediction.symbol }}</div>
                <div class="prediction-time">{{ formatTime(latestPrediction.timestamp) }}</div>
              </div>

              <div class="prediction-details">
                <div class="prediction-row">
                  <div class="prediction-label">Aktueller Preis:</div>
                  <div class="prediction-value">{{ latestPrediction.current.toFixed(2) }}</div>
                </div>

                <div class="prediction-row">
                  <div class="prediction-label">Prognostizierter Preis:</div>
                  <div class="prediction-value">{{ latestPrediction.prediction.toFixed(2) }}</div>
                </div>

                <div class="prediction-row">
                  <div class="prediction-label">Richtung:</div>
                  <div class="prediction-value" :class="{
                    positive: latestPrediction.direction === 'up',
                    negative: latestPrediction.direction === 'down'
                  }">
                    {{ latestPrediction.direction === 'up' ? '↑ Aufwärts' : '↓ Abwärts' }}
                  </div>
                </div>

                <div class="prediction-row">
                  <div class="prediction-label">Änderung:</div>
                  <div class="prediction-value" :class="{
                    positive: latestPrediction.change_pct > 0,
                    negative: latestPrediction.change_pct < 0
                  }">
                    {{ latestPrediction.change_pct.toFixed(2) }}%
                  </div>
                </div>

                <div class="prediction-row">
                  <div class="prediction-label">Vertrauen:</div>
                  <div class="prediction-value">{{ (latestPrediction.confidence * 100).toFixed(2) }}%</div>
                </div>
              </div>

              <div class="prediction-actions">
                <button @click="executeTrade(latestPrediction.symbol, latestPrediction.direction === 'up' ? 'buy' : 'sell')"
                        class="action-button"
                        :class="{ 'buy-button': latestPrediction.direction === 'up', 'sell-button': latestPrediction.direction === 'down' }">
                  {{ latestPrediction.direction === 'up' ? 'Kaufen' : 'Verkaufen' }}
                </button>
              </div>
            </div>
          </div>

          <div class="prediction-history">
            <h3>Prognosehistorie</h3>
            <div class="prediction-history-placeholder">Noch keine Prognosehistorie verfügbar</div>
          </div>
        </div>

        <!-- Trades -->
        <div v-if="activeTab === 'trades'" class="tab-content">
          <h2>Trades</h2>

          <div class="tabs">
            <button @click="tradeTabActive = 'open'" :class="{ active: tradeTabActive === 'open' }">Offene Trades</button>
            <button @click="tradeTabActive = 'closed'" :class="{ active: tradeTabActive === 'closed' }">Geschlossene Trades</button>
          </div>

          <div v-if="tradeTabActive === 'open'" class="trade-list">
            <div v-if="openTrades.length === 0" class="empty-state">
              Keine offenen Trades
            </div>

            <div v-else class="trades-table">
              <div class="trades-header">
                <div class="trade-cell">Symbol</div>
                <div class="trade-cell">Aktion</div>
                <div class="trade-cell">Preis</div>
                <div class="trade-cell">Betrag</div>
                <div class="trade-cell">Zeit</div>
                <div class="trade-cell">Stop-Loss</div>
                <div class="trade-cell">Take-Profit</div>
              </div>

              <div v-for="trade in openTrades" :key="trade.id" class="trade-row">
                <div class="trade-cell">{{ trade.symbol }}</div>
                <div class="trade-cell" :class="{ 'buy': trade.action === 'buy', 'sell': trade.action === 'sell' }">
                  {{ trade.action.toUpperCase() }}
                </div>
                <div class="trade-cell">{{ trade.price.toFixed(2) }}</div>
                <div class="trade-cell">{{ trade.amount.toFixed(2) }}</div>
                <div class="trade-cell">{{ formatTime(trade.timestamp) }}</div>
                <div class="trade-cell">{{ trade.stop_loss.toFixed(2) }}</div>
                <div class="trade-cell">{{ trade.take_profit.toFixed(2) }}</div>
              </div>
            </div>
          </div>

          <div v-if="tradeTabActive === 'closed'" class="trade-list">
            <div v-if="closedTrades.length === 0" class="empty-state">
              Keine geschlossenen Trades
            </div>

            <div v-else class="trades-table">
              <div class="trades-header">
                <div class="trade-cell">Symbol</div>
                <div class="trade-cell">Aktion</div>
                <div class="trade-cell">Eröffnungspreis</div>
                <div class="trade-cell">Schlusspreis</div>
                <div class="trade-cell">P/L %</div>
                <div class="trade-cell">Grund</div>
                <div class="trade-cell">Geschlossen</div>
              </div>

              <div v-for="trade in closedTrades" :key="trade.id" class="trade-row">
                <div class="trade-cell">{{ trade.symbol }}</div>
                <div class="trade-cell" :class="{ 'buy': trade.action === 'buy', 'sell': trade.action === 'sell' }">
                  {{ trade.action.toUpperCase() }}
                </div>
                <div class="trade-cell">{{ trade.price.toFixed(2) }}</div>
                <div class="trade-cell">{{ trade.close_price.toFixed(2) }}</div>
                <div class="trade-cell" :class="{ 'positive': trade.profit_loss > 0, 'negative': trade.profit_loss < 0 }">
                  {{ trade.profit_loss.toFixed(2) }}%
                </div>
                <div class="trade-cell">{{ formatCloseReason(trade.close_reason) }}</div>
                <div class="trade-cell">{{ formatTime(trade.close_time) }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Jobs -->
        <div v-if="activeTab === 'jobs'" class="tab-content">
          <h2>Automatisierte Jobs</h2>

          <div class="job-form">
            <h3>Neuen Job hinzufügen</h3>
            <div class="form-group">
              <label for="job-symbol">Symbol</label>
              <input type="text" id="job-symbol" v-model="jobForm.symbol" placeholder="z.B. BTC-USDT">
            </div>

            <div class="form-group">
              <label for="job-interval">Intervall</label>
              <select id="job-interval" v-model="jobForm.interval">
                <option value="15m">15 Minuten</option>
                <option value="30m">30 Minuten</option>
                <option value="1h">1 Stunde</option>
                <option value="4h">4 Stunden</option>
                <option value="1d">1 Tag</option>
              </select>
            </div>

            <button @click="addJob" class="primary-button">Job hinzufügen</button>
          </div>

          <div class="job-list">
            <h3>Aktive Jobs</h3>

            <div v-if="jobs.length === 0" class="empty-state">
              Keine aktiven Jobs
            </div>

            <div v-else class="jobs-table">
              <div class="jobs-header">
                <div class="job-cell">Job ID</div>
                <div class="job-cell">Symbol</div>
                <div class="job-cell">Intervall</div>
                <div class="job-cell">Nächste Ausführung</div>
                <div class="job-cell">Aktionen</div>
              </div>

              <div v-for="job in jobs" :key="job.id" class="job-row">
                <div class="job-cell">{{ job.id }}</div>
                <div class="job-cell">{{ extractSymbol(job.id) }}</div>
                <div class="job-cell">{{ job.interval }} {{ job.unit }}</div>
                <div class="job-cell">{{ job.next_run }}</div>
                <div class="job-cell">
                  <button @click="removeJob(job.id)" class="delete-button">Löschen</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Einstellungen -->
        <div v-if="activeTab === 'settings'" class="tab-content">
          <h2>Einstellungen</h2>

          <div class="settings-section">
            <h3>Allgemeine Einstellungen</h3>

            <div class="form-group">
              <label for="trading-enabled">Trading aktivieren</label>
              <div class="toggle-switch">
                <input type="checkbox" id="trading-enabled" v-model="settings.trader.trading_enabled">
                <label for="trading-enabled"></label>
              </div>
            </div>

            <div class="form-group">
              <label for="max-trades-day">Maximale Trades pro Tag</label>
              <input type="number" id="max-trades-day" v-model="settings.trader.max_trades_per_day" min="1" max="50">
            </div>

            <div class="form-group">
              <label for="trade-amount">Betrag pro Trade</label>
              <input type="number" id="trade-amount" v-model="settings.trader.trade_amount" min="1">
            </div>
          </div>

          <div class="settings-section">
            <h3>Risikomanagement</h3>

            <div class="form-group">
              <label for="stop-loss">Stop-Loss (%)</label>
              <input type="number" id="stop-loss" v-model="settings.trader.stop_loss_pct" min="0.1" max="10" step="0.1">
            </div>

            <div class="form-group">
              <label for="take-profit">Take-Profit (%)</label>
              <input type="number" id="take-profit" v-model="settings.trader.take_profit_pct" min="0.1" max="20" step="0.1">
            </div>

            <div class="form-group">
              <label for="max-risk">Maximales Risiko pro Trade (%)</label>
              <input type="number" id="max-risk" v-model="settings.trader.risk_management.max_risk_per_trade" min="0.1" max="10" step="0.1">
            </div>
          </div>

          <div class="settings-section">
            <h3>Modelleinstellungen</h3>

            <div class="form-group">
              <label for="model-type">Modelltyp</label>
              <select id="model-type" v-model="settings.model.model_type">
                <option value="random_forest">Random Forest</option>
                <option value="gradient_boosting">Gradient Boosting</option>
                <option value="linear">Linear</option>
              </select>
            </div>

            <div class="form-group">
              <label for="prediction-horizon">Prognosehorizont (Stunden)</label>
              <input type="number" id="prediction-horizon" v-model="settings.model.prediction_horizon" min="1" max="24">
            </div>

            <div class="form-group">
              <label for="confidence-threshold">Vertrauensschwelle</label>
              <input type="number" id="confidence-threshold" v-model="settings.trader.confidence_threshold" min="0.1" max="1" step="0.05">
            </div>

            <div class="form-group">
              <label for="min-change">Minimale Änderung für Trade (%)</label>
              <input type="number" id="min-change" v-model="settings.trader.min_change_pct" min="0.1" max="5" step="0.1">
            </div>
          </div>

          <div class="settings-section">
            <h3>API-Schlüssel</h3>

            <div class="form-group">
              <label for="binance-api-key">Binance API-Schlüssel</label>
              <input type="password" id="binance-api-key" v-model="settings.trader.exchanges.binance.api_key">
            </div>

            <div class="form-group">
              <label for="binance-api-secret">Binance API-Secret</label>
              <input type="password" id="binance-api-secret" v-model="settings.trader.exchanges.binance.api_secret">
            </div>

            <div class="form-group">
              <label for="binance-test-mode">Testmodus</label>
              <div class="toggle-switch">
                <input type="checkbox" id="binance-test-mode" v-model="settings.trader.exchanges.binance.test_mode">
                <label for="binance-test-mode"></label>
              </div>
            </div>
          </div>

          <div class="settings-actions">
            <button @click="saveSettings" class="primary-button">Einstellungen speichern</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  data() {
    return {
      activeTab: 'dashboard',
      tradeTabActive: 'open',
      isActive: false,
      stats: {},
      jobs: [],
      openTrades: [],
      closedTrades: [],
      latestPrediction: null,
      performanceChart: null,

      predictionForm: {
        symbol: 'BTC-USDT',
        timeframe: '1h'
      },

      jobForm: {
        symbol: 'BTC-USDT',
        interval: '1h'
      },

      settings: {
        trader: {
          trading_enabled: false,
          max_trades_per_day: 5,
          trade_amount: 100,
          stop_loss_pct: 2.0,
          take_profit_pct: 3.0,
          confidence_threshold: 0.7,
          min_change_pct: 1.0,
          exchanges: {
            binance: {
              api_key: '',
              api_secret: '',
              test_mode: true
            }
          },
          risk_management: {
            max_risk_per_trade: 2.0,
            daily_drawdown_limit: 5.0
          }
        },
        model: {
          model_type: 'random_forest',
          prediction_horizon: 1
        }
      }
    }
  },

  created() {
    this.loadData();

    // Daten periodisch aktualisieren
    setInterval(this.loadData, 30000);
  },

  mounted() {
    // Performance-Chart initialisieren
    this.$nextTick(() => {
      this.initPerformanceChart();
    });
  },

  methods: {
    loadData() {
      this.loadStatus();
      this.loadStats();
      this.loadJobs();
      this.loadTrades();
      this.loadSettings();
    },

    async loadStatus() {
      try {
        const response = await fetch('/api/status');
        const data = await response.json();
        this.isActive = data.status === 'running';
      } catch (error) {
        console.error('Fehler beim Laden des Status:', error);
      }
    },

    async loadStats() {
      try {
        const response = await fetch('/api/stats');
        this.stats = await response.json();
      } catch (error) {
        console.error('Fehler beim Laden der Statistiken:', error);
      }
    },

    async loadJobs() {
      try {
        const response = await fetch('/api/jobs');
        const data = await response.json();
        this.jobs = data.jobs;
      } catch (error) {
        console.error('Fehler beim Laden der Jobs:', error);
      }
    },

    async loadTrades() {
      try {
        // Offene Trades laden
        const openResponse = await fetch('/api/trades?status=open');
        const openData = await openResponse.json();
        this.openTrades = openData.trades;

        // Geschlossene Trades laden
        const closedResponse = await fetch('/api/trades?status=closed');
        const closedData = await closedResponse.json();
        this.closedTrades = closedData.trades;
      } catch (error) {
        console.error('Fehler beim Laden der Trades:', error);
      }
    },

    async loadSettings() {
      try {
        const response = await fetch('/api/config');
        const data = await response.json();

        if (data.model_config) {
          this.settings.model = data.model_config;
        }

        if (data.trader_config) {
          this.settings.trader = data.trader_config;
        }
      } catch (error) {
        console.error('Fehler beim Laden der Einstellungen:', error);
      }
    },

    async makePrediction() {
      try {
        const response = await fetch('/api/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.predictionForm)
        });

        const data = await response.json();
        this.latestPrediction = data;
      } catch (error) {
        console.error('Fehler bei der Prognose:', error);
        alert('Fehler bei der Prognose: ' + error.message);
      }
    },

    async executeTrade(symbol, action) {
      try {
        const response = await fetch('/api/trade', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            symbol: symbol,
            action: action
          })
        });

        const data = await response.json();

        if (data.success) {
          alert(`Trade erfolgreich ausgeführt: ${action.toUpperCase()} ${symbol}`);
          this.loadTrades();
        } else {
          alert(`Fehler beim Ausführen des Trades: ${data.reason}`);
        }
      } catch (error) {
        console.error('Fehler beim Ausführen des Trades:', error);
        alert('Fehler beim Ausführen des Trades: ' + error.message);
      }
    },

    async addJob() {
      try {
        const response = await fetch('/api/jobs', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.jobForm)
        });

        const data = await response.json();

        if (data.job_id) {
          alert(`Job erfolgreich hinzugefügt: ${data.job_id}`);
          this.loadJobs();
        } else {
          alert('Fehler beim Hinzufügen des Jobs');
        }
      } catch (error) {
        console.error('Fehler beim Hinzufügen des Jobs:', error);
        alert('Fehler beim Hinzufügen des Jobs: ' + error.message);
      }
    },

    async removeJob(jobId) {
      if (confirm(`Sind Sie sicher, dass Sie den Job ${jobId} löschen möchten?`)) {
        try {
          const response = await fetch(`/api/jobs/${jobId}`, {
            method: 'DELETE'
          });

          const data = await response.json();

          if (data.message) {
            alert(data.message);
            this.loadJobs();
          } else {
            alert('Fehler beim Löschen des Jobs');
          }
        } catch (error) {
          console.error('Fehler beim Löschen des Jobs:', error);
          alert('Fehler beim Löschen des Jobs: ' + error.message);
        }
      }
    },

    async saveSettings() {
      try {
        // Trader-Einstellungen speichern
        await fetch('/api/config', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            section: 'trader',
            config: this.settings.trader
          })
        });

        // Modell-Einstellungen speichern
        await fetch('/api/config', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            section: 'model',
            config: this.settings.model
          })
        });

        alert('Einstellungen erfolgreich gespeichert');
      } catch (error) {
        console.error('Fehler beim Speichern der Einstellungen:', error);
        alert('Fehler beim Speichern der Einstellungen: ' + error.message);
      }
    },

    formatTime(timestamp) {
      if (!timestamp) return '';

      const date = new Date(timestamp);
      return date.toLocaleString();
    },

    formatCloseReason(reason) {
      if (reason === 'stop_loss') return 'Stop-Loss';
      if (reason === 'take_profit') return 'Take-Profit';
      return reason;
    },

    extractSymbol(jobId) {
      if (!jobId) return '';

      // Format: predict_BTC-USDT_1h
      const parts = jobId.split('_');
      if (parts.length >= 2) {
        return parts[1];
      }

      return jobId;
    },

    initPerformanceChart() {
      // Beispielhafte Performance-Daten
      const ctx = this.$refs.performanceChart.getContext('2d');
      
      // Chart-Daten erstellen
      const labels = [];
      const profitLossData = [];
      
      // Letzten 30 Tage generieren
      const today = new Date();
      for (let i = 30; i >= 0; i--) {
        const date = new Date();
        date.setDate(today.getDate() - i);
        labels.push(date.toLocaleDateString());
        
        // Dummy-Daten für die Demonstration
        const randomValue = Math.random() * 4 - 1; // Zwischen -1% und 3%
        profitLossData.push(randomValue);
      }
      
      // Chart erstellen
      this.performanceChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Tägliche P/L (%)',
              data: profitLossData,
              borderColor: '#2a3f54',
              backgroundColor: 'rgba(42, 63, 84, 0.1)',
              tension: 0.4,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `${context.dataset.label}: ${context.raw.toFixed(2)}%`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              grid: {
                drawBorder: false
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          }
        }
      });
    },

    updatePerformanceChart(performanceData) {
      if (!this.performanceChart) return;
      
      this.performanceChart.data.labels = performanceData.dates;
      this.performanceChart.data.datasets[0].data = performanceData.values;
      this.performanceChart.update();
    }
  }
}
</script>

<style>
/* Grundstile */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f5f7fa;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* Header */
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

header h1 {
  font-size: 28px;
  color: #2a3f54;
}

.status-indicator {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  background-color: #f0f0f0;
  color: #888;
}

.status-indicator.active {
  background-color: #d4edda;
  color: #155724;
}

/* Layout */
.main-content {
  display: flex;
  gap: 30px;
}

.sidebar {
  width: 200px;
  flex-shrink: 0;
}

.content {
  flex-grow: 1;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 30px;
}

/* Navigation */
.sidebar nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sidebar button {
  padding: 12px 15px;
  text-align: left;
  background-color: #f5f7fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.sidebar button.active {
  background-color: #2a3f54;
  color: white;
  border-color: #2a3f54;
}

.sidebar button:hover:not(.active) {
  background-color: #e9ecef;
}

/* Tabs */
.tab-content {
  min-height: 500px;
}

.tab-content h2 {
  font-size: 24px;
  margin-bottom: 25px;
  color: #2a3f54;
}

.tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.tabs button {
  padding: 10px 20px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-weight: 500;
  color: #666;
}

.tabs button.active {
  color: #2a3f54;
  border-bottom-color: #2a3f54;
}

/* Statistik-Karten */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
  border: 1px solid #e0e0e0;
}

.stat-card h3 {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #2a3f54;
}

.positive {
  color: #28a745;
}

.negative {
  color: #dc3545;
}

/* Charts */
.chart-container {
  margin-bottom: 30px;
}

.chart-placeholder {
  height: 300px;
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: 1px dashed #ccc;
  color: #888;
}

/* Symbole */
.active-symbols {
  margin-bottom: 30px;
}

.symbols-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.symbol-item {
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  background-color: #f9f9f9;
}

.symbol-name {
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 5px;
}

.symbol-next-run {
  color: #666;
  font-size: 14px;
}

/* Formulare */
.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

input[type="text"],
input[type="number"],
input[type="password"],
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.primary-button {
  background-color: #2a3f54;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  font-size: 16px;
}

.primary-button:hover {
  background-color: #1f2f3d;
}

.delete-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.delete-button:hover {
  background-color: #c82333;
}

.action-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.buy-button {
  background-color: #28a745;
  color: white;
}

.buy-button:hover {
  background-color: #218838;
}

.sell-button {
  background-color: #dc3545;
  color: white;
}

.sell-button:hover {
  background-color: #c82333;
}

/* Prognosen */
.prediction-form {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.prediction-result {
  margin-bottom: 30px;
}

.prediction-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background-color: white;
}

.prediction-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.prediction-symbol {
  font-size: 20px;
  font-weight: bold;
}

.prediction-time {
  color: #666;
}

.prediction-details {
  margin-bottom: 20px;
}

.prediction-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.prediction-label {
  font-weight: 500;
}

.prediction-actions {
  display: flex;
  justify-content: flex-end;
}

/* Trades und Jobs Tabellen */
.trades-table, .jobs-table {
  width: 100%;
  border-collapse: collapse;
}

.trades-header, .jobs-header {
  background-color: #f5f7fa;
  font-weight: bold;
}

.trade-row, .job-row {
  border-bottom: 1px solid #eee;
}

.trade-cell, .job-cell {
  padding: 12px 15px;
  text-align: left;
}

.trade-row:last-child, .job-row:last-child {
  border-bottom: none;
}

.buy {
  color: #28a745;
}

.sell {
  color: #dc3545;
}

.empty-state {
  padding: 30px;
  text-align: center;
  color: #888;
  background-color: #f9f9f9;
  border-radius: 8px;
}

/* Einstellungen */
.settings-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.settings-section h3 {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.settings-actions {
  margin-top: 30px;
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-switch label {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}

.toggle-switch label:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

.toggle-switch input:checked + label {
  background-color: #2a3f54;
}

.toggle-switch input:checked + label:before {
  transform: translateX(26px);
}

</style>