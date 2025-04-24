<!--<template>-->
<!--  <div class="container">-->
<!--    <header>-->
<!--      <h1>TradeBot - Prädiktiver Handelsbot</h1>-->
<!--      <div class="status-indicator" :class="{ active: isActive }">-->
<!--        {{ isActive ? 'Aktiv' : 'Inaktiv' }}-->
<!--      </div>-->
<!--    </header>-->

<!--    <div v-if="isLoading" class="loading-overlay">-->
<!--      <div class="loading-spinner"></div>-->
<!--      <div class="loading-text">Daten werden geladen...</div>-->
<!--    </div>-->

<!--    <div v-if="globalError" class="error-message">-->
<!--      {{ globalError }}-->
<!--      <button @click="dismissError" class="dismiss-button">×</button>-->
<!--    </div>-->

<!--    <div class="main-content">-->
<!--      <div class="sidebar">-->
<!--        <nav>-->
<!--          <button @click="activeTab = 'dashboard'" :class="{ active: activeTab === 'dashboard' }">Dashboard</button>-->
<!--          <button @click="activeTab = 'predictions'" :class="{ active: activeTab === 'predictions' }">Prognosen</button>-->
<!--          <button @click="activeTab = 'trades'" :class="{ active: activeTab === 'trades' }">Trades</button>-->
<!--          <button @click="activeTab = 'jobs'" :class="{ active: activeTab === 'jobs' }">Jobs</button>-->
<!--          <button @click="activeTab = 'settings'" :class="{ active: activeTab === 'settings' }">Einstellungen</button>-->
<!--        </nav>-->
<!--      </div>-->

<!--      <div class="content">-->
<!--        &lt;!&ndash; Dashboard &ndash;&gt;-->
<!--        <div v-if="activeTab === 'dashboard'" class="tab-content">-->
<!--          <h2>Dashboard</h2>-->

<!--          <div class="stats-grid">-->
<!--            <div class="stat-card">-->
<!--              <h3>Offene Trades</h3>-->
<!--              <div class="stat-value">{{ stats.open_trades || 0 }}</div>-->
<!--            </div>-->

<!--            <div class="stat-card">-->
<!--              <h3>Trades Heute</h3>-->
<!--              <div class="stat-value">{{ stats.daily_trades || 0 }}</div>-->
<!--            </div>-->

<!--            <div class="stat-card">-->
<!--              <h3>Gewinn/Verlust Heute</h3>-->
<!--              <div class="stat-value" :class="{ positive: (stats.daily_profit_loss || 0) > 0, negative: (stats.daily_profit_loss || 0) < 0 }">-->
<!--                {{ stats.daily_profit_loss ? stats.daily_profit_loss.toFixed(2) + '%' : '0.00%' }}-->
<!--              </div>-->
<!--            </div>-->

<!--            <div class="stat-card">-->
<!--              <h3>Gewinnrate</h3>-->
<!--              <div class="stat-value">{{ stats.win_rate ? stats.win_rate.toFixed(2) + '%' : '0.00%' }}</div>-->
<!--            </div>-->
<!--          </div>-->

<!--          <div class="chart-container">-->
<!--            <h3>Performance Übersicht</h3>-->
<!--            <canvas ref="performanceChart" width="400" height="200"></canvas>-->
<!--          </div>-->

<!--          <div class="active-symbols">-->
<!--            <h3>Aktive Symbole</h3>-->
<!--            <div class="symbols-list">-->
<!--              <div v-for="job in jobs" :key="job.id" class="symbol-item">-->
<!--                <div class="symbol-name">{{ extractSymbol(job.id) }}</div>-->
<!--                <div class="symbol-next-run">Nächste Prognose: {{ job.next_run }}</div>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Prognosen &ndash;&gt;-->
<!--        <div v-if="activeTab === 'predictions'" class="tab-content">-->
<!--          <h2>Prognosen</h2>-->

<!--          <div class="prediction-form">-->
<!--            <h3>Neue Prognose</h3>-->
<!--            <div class="form-group">-->
<!--              <label for="prediction-symbol">Symbol</label>-->
<!--              <input type="text" id="prediction-symbol" v-model="predictionForm.symbol" placeholder="z.B. BTC-USDT">-->
<!--              <div v-if="errors.predictionSymbol" class="error-hint">{{ errors.predictionSymbol }}</div>-->
<!--            </div>-->

<!--            <div class="form-group">-->
<!--              <label for="prediction-timeframe">Zeitrahmen</label>-->
<!--              <select id="prediction-timeframe" v-model="predictionForm.timeframe">-->
<!--                <option value="1h">1 Stunde</option>-->
<!--                <option value="4h">4 Stunden</option>-->
<!--                <option value="1d">1 Tag</option>-->
<!--              </select>-->
<!--            </div>-->

<!--            <button @click="makePrediction" class="primary-button" :disabled="loading.prediction">-->
<!--              {{ loading.prediction ? 'Wird berechnet...' : 'Prognose erstellen' }}-->
<!--            </button>-->
<!--          </div>-->

<!--          <div v-if="errors.prediction" class="error-box">-->
<!--            {{ errors.prediction }}-->
<!--          </div>-->

<!--          <div v-if="latestPrediction" class="prediction-result">-->
<!--            <h3>Letzte Prognose</h3>-->
<!--            <div class="prediction-card">-->
<!--              <div class="prediction-header">-->
<!--                <div class="prediction-symbol">{{ latestPrediction.symbol }}</div>-->
<!--                <div class="prediction-time">{{ formatTime(latestPrediction.timestamp) }}</div>-->
<!--              </div>-->

<!--              <div class="prediction-details">-->
<!--                <div class="prediction-row">-->
<!--                  <div class="prediction-label">Aktueller Preis:</div>-->
<!--                  <div class="prediction-value">{{ latestPrediction.current.toFixed(2) }}</div>-->
<!--                </div>-->

<!--                <div class="prediction-row">-->
<!--                  <div class="prediction-label">Prognostizierter Preis:</div>-->
<!--                  <div class="prediction-value">{{ latestPrediction.prediction.toFixed(2) }}</div>-->
<!--                </div>-->

<!--                <div class="prediction-row">-->
<!--                  <div class="prediction-label">Richtung:</div>-->
<!--                  <div class="prediction-value" :class="{-->
<!--                    positive: latestPrediction.direction === 'up',-->
<!--                    negative: latestPrediction.direction === 'down'-->
<!--                  }">-->
<!--                    {{ latestPrediction.direction === 'up' ? '↑ Aufwärts' : '↓ Abwärts' }}-->
<!--                  </div>-->
<!--                </div>-->

<!--                <div class="prediction-row">-->
<!--                  <div class="prediction-label">Änderung:</div>-->
<!--                  <div class="prediction-value" :class="{-->
<!--                    positive: latestPrediction.change_pct > 0,-->
<!--                    negative: latestPrediction.change_pct < 0-->
<!--                  }">-->
<!--                    {{ latestPrediction.change_pct.toFixed(2) }}%-->
<!--                  </div>-->
<!--                </div>-->

<!--                <div class="prediction-row">-->
<!--                  <div class="prediction-label">Vertrauen:</div>-->
<!--                  <div class="prediction-value">{{ (latestPrediction.confidence * 100).toFixed(2) }}%</div>-->
<!--                </div>-->
<!--              </div>-->

<!--              <div class="prediction-actions">-->
<!--                <button @click="executeTrade(latestPrediction.symbol, latestPrediction.direction === 'up' ? 'buy' : 'sell')"-->
<!--                        class="action-button"-->
<!--                        :class="{ 'buy-button': latestPrediction.direction === 'up', 'sell-button': latestPrediction.direction === 'down' }"-->
<!--                        :disabled="loading.trade">-->
<!--                  {{ loading.trade ? 'Wird ausgeführt...' : (latestPrediction.direction === 'up' ? 'Kaufen' : 'Verkaufen') }}-->
<!--                </button>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->

<!--          <div class="prediction-history">-->
<!--            <h3>Prognosehistorie</h3>-->
<!--            <div class="prediction-history-placeholder">Noch keine Prognosehistorie verfügbar</div>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Trades &ndash;&gt;-->
<!--        <div v-if="activeTab === 'trades'" class="tab-content">-->
<!--          <h2>Trades</h2>-->

<!--          <div class="tabs">-->
<!--            <button @click="tradeTabActive = 'open'" :class="{ active: tradeTabActive === 'open' }">Offene Trades</button>-->
<!--            <button @click="tradeTabActive = 'closed'" :class="{ active: tradeTabActive === 'closed' }">Geschlossene Trades</button>-->
<!--          </div>-->

<!--          <div v-if="tradeTabActive === 'open'" class="trade-list">-->
<!--            <div v-if="openTrades.length === 0" class="empty-state">-->
<!--              Keine offenen Trades-->
<!--            </div>-->

<!--            <div v-else class="trades-table">-->
<!--              <div class="trades-header">-->
<!--                <div class="trade-cell">Symbol</div>-->
<!--                <div class="trade-cell">Aktion</div>-->
<!--                <div class="trade-cell">Preis</div>-->
<!--                <div class="trade-cell">Betrag</div>-->
<!--                <div class="trade-cell">Zeit</div>-->
<!--                <div class="trade-cell">Stop-Loss</div>-->
<!--                <div class="trade-cell">Take-Profit</div>-->
<!--              </div>-->

<!--              <div v-for="trade in openTrades" :key="trade.id" class="trade-row">-->
<!--                <div class="trade-cell">{{ trade.symbol }}</div>-->
<!--                <div class="trade-cell" :class="{ 'buy': trade.action === 'buy', 'sell': trade.action === 'sell' }">-->
<!--                  {{ trade.action.toUpperCase() }}-->
<!--                </div>-->
<!--                <div class="trade-cell">{{ trade.price ? trade.price.toFixed(2) : '0.00' }}</div>-->
<!--                <div class="trade-cell">{{ trade.amount ? trade.amount.toFixed(2) : '0.00' }}</div>-->
<!--                <div class="trade-cell">{{ formatTime(trade.timestamp) }}</div>-->
<!--                <div class="trade-cell">{{ trade.stop_loss ? trade.stop_loss.toFixed(2) : '0.00' }}</div>-->
<!--                <div class="trade-cell">{{ trade.take_profit ? trade.take_profit.toFixed(2) : '0.00' }}</div>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->

<!--          <div v-if="tradeTabActive === 'closed'" class="trade-list">-->
<!--            <div v-if="closedTrades.length === 0" class="empty-state">-->
<!--              Keine geschlossenen Trades-->
<!--            </div>-->

<!--            <div v-else class="trades-table">-->
<!--              <div class="trades-header">-->
<!--                <div class="trade-cell">Symbol</div>-->
<!--                <div class="trade-cell">Aktion</div>-->
<!--                <div class="trade-cell">Eröffnungspreis</div>-->
<!--                <div class="trade-cell">Schlusspreis</div>-->
<!--                <div class="trade-cell">P/L %</div>-->
<!--                <div class="trade-cell">Grund</div>-->
<!--                <div class="trade-cell">Geschlossen</div>-->
<!--              </div>-->

<!--              <div v-for="trade in closedTrades" :key="trade.id" class="trade-row">-->
<!--                <div class="trade-cell">{{ trade.symbol }}</div>-->
<!--                <div class="trade-cell" :class="{ 'buy': trade.action === 'buy', 'sell': trade.action === 'sell' }">-->
<!--                  {{ trade.action.toUpperCase() }}-->
<!--                </div>-->
<!--                <div class="trade-cell">{{ trade.price ? trade.price.toFixed(2) : '0.00' }}</div>-->
<!--                <div class="trade-cell">{{ trade.close_price ? trade.close_price.toFixed(2) : '0.00' }}</div>-->
<!--                <div class="trade-cell" :class="{ 'positive': trade.profit_loss > 0, 'negative': trade.profit_loss < 0 }">-->
<!--                  {{ trade.profit_loss ? trade.profit_loss.toFixed(2) : '0.00' }}%-->
<!--                </div>-->
<!--                <div class="trade-cell">{{ formatCloseReason(trade.close_reason) }}</div>-->
<!--                <div class="trade-cell">{{ formatTime(trade.close_time) }}</div>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Jobs &ndash;&gt;-->
<!--        <div v-if="activeTab === 'jobs'" class="tab-content">-->
<!--          <h2>Automatisierte Jobs</h2>-->

<!--          <div class="job-form">-->
<!--            <h3>Neuen Job hinzufügen</h3>-->
<!--            <div class="form-group">-->
<!--              <label for="job-symbol">Symbol</label>-->
<!--              <input type="text" id="job-symbol" v-model="jobForm.symbol" placeholder="z.B. BTC-USDT">-->
<!--              <div v-if="errors.jobSymbol" class="error-hint">{{ errors.jobSymbol }}</div>-->
<!--            </div>-->

<!--            <div class="form-group">-->
<!--              <label for="job-interval">Intervall</label>-->
<!--              <select id="job-interval" v-model="jobForm.interval">-->
<!--                <option value="15m">15 Minuten</option>-->
<!--                <option value="30m">30 Minuten</option>-->
<!--                <option value="1h">1 Stunde</option>-->
<!--                <option value="4h">4 Stunden</option>-->
<!--                <option value="1d">1 Tag</option>-->
<!--              </select>-->
<!--            </div>-->

<!--            <button @click="addJob" class="primary-button" :disabled="loading.addJob">-->
<!--              {{ loading.addJob ? 'Wird hinzugefügt...' : 'Job hinzufügen' }}-->
<!--            </button>-->
<!--          </div>-->

<!--          <div v-if="errors.jobs" class="error-box">-->
<!--            {{ errors.jobs }}-->
<!--          </div>-->

<!--          <div class="job-list">-->
<!--            <h3>Aktive Jobs</h3>-->

<!--            <div v-if="jobs.length === 0" class="empty-state">-->
<!--              Keine aktiven Jobs-->
<!--            </div>-->

<!--            <div v-else class="jobs-table">-->
<!--              <div class="jobs-header">-->
<!--                <div class="job-cell">Job ID</div>-->
<!--                <div class="job-cell">Symbol</div>-->
<!--                <div class="job-cell">Intervall</div>-->
<!--                <div class="job-cell">Nächste Ausführung</div>-->
<!--                <div class="job-cell">Aktionen</div>-->
<!--              </div>-->

<!--              <div v-for="job in jobs" :key="job.id" class="job-row">-->
<!--                <div class="job-cell">{{ job.id }}</div>-->
<!--                <div class="job-cell">{{ extractSymbol(job.id) }}</div>-->
<!--                <div class="job-cell">{{ job.interval }} {{ job.unit }}</div>-->
<!--                <div class="job-cell">{{ job.next_run }}</div>-->
<!--                <div class="job-cell">-->
<!--                  <button @click="removeJob(job.id)" class="delete-button" :disabled="loading.removeJob === job.id">-->
<!--                    {{ loading.removeJob === job.id ? 'Wird gelöscht...' : 'Löschen' }}-->
<!--                  </button>-->
<!--                </div>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; Einstellungen &ndash;&gt;-->
<!--        <div v-if="activeTab === 'settings'" class="tab-content">-->
<!--          <h2>Einstellungen</h2>-->

<!--          <div class="settings-section">-->
<!--            <h3>Allgemeine Einstellungen</h3>-->

<!--            <div class="form-group">-->
<!--              <label for="trading-enabled">Trading aktivieren</label>-->
<!--              <div class="toggle-switch">-->
<!--                <input type="checkbox" id="trading-enabled" v-model="settings.trader.trading_enabled">-->
<!--                <label for="trading-enabled"></label>-->
<!--              </div>-->
<!--            </div>-->

<!--            <div class="form-group">-->
<!--              <label for="max-trades-day">Maximale Trades pro Tag</label>-->
<!--              <input type="number" id="max-trades-day" v-model.number="settings.trader.max_trades_per_day" min="1" max="50">-->
<!--            </div>-->

<!--            <div class="form-group">-->
<!--              <label for="trade-amount">Betrag pro Trade</label>-->
<!--              <input type="number" id="trade-amount" v-model.number="settings.trader.trade_amount" min="1">-->
<!--            </div>-->
<!--          </div>-->

<!--          <div class="settings-section">-->
<!--            <h3>Risikomanagement</h3>-->

<!--            <div class="form-group">-->
<!--              <label for="stop-loss">Stop-Loss (%)</label>-->
<!--              <input type="number" id="stop-loss" v-model.number="settings.trader.stop_loss_pct" min="0.1" max="10" step="0.1">-->
<!--            </div>-->

<!--            <div class="form-group">-->
<!--              <label for="take-profit">Take-Profit (%)</label>-->
<!--              <input type="number" id="take-profit" v-model.number="settings.trader.take_profit_pct" min="0.1" max="20" step="0.1">-->
<!--            </div>-->

<!--            <div class="form-group">-->
<!--              <label for="max-risk">Maximales Risiko pro Trade (%)</label>-->
<!--              <input type="number" id="max-risk" v-model.number="settings.trader.risk_management.max_risk_per_trade" min="0.1" max="10" step="0.1">-->
<!--            </div>-->
<!--          </div>-->

<!--          <div class="settings-section">-->
<!--            <h3>Modelleinstellungen</h3>-->

<!--            <div class="form-group">-->
<!--              <label for="model-type">Modelltyp</label>-->
<!--              <select id="model-type" v-model="settings.model.model_type">-->
<!--                <option value="random_forest">Random Forest</option>-->
<!--                <option value="gradient_boosting">Gradient Boosting</option>-->
<!--                <option value="linear">Linear</option>-->
<!--              </select>-->
<!--            </div>-->

<!--            <div class="form-group">-->
<!--              <label for="prediction-horizon">Prognosehorizont (Stunden)</label>-->
<!--              <input type="number" id="prediction-horizon" v-model.number="settings.model.prediction_horizon" min="1" max="24">-->
<!--            </div>-->

<!--            <div class="form-group">-->
<!--              <label for="confidence-threshold">Vertrauensschwelle</label>-->
<!--              <input type="number" id="confidence-threshold" v-model.number="settings.trader.confidence_threshold" min="0.1" max="1" step="0.05">-->
<!--            </div>-->

<!--            <div class="form-group">-->
<!--              <label for="min-change">Minimale Änderung für Trade (%)</label>-->
<!--              <input type="number" id="min-change" v-model.number="settings.trader.min_change_pct" min="0.1" max="5" step="0.1">-->
<!--            </div>-->
<!--          </div>-->

<!--          <div class="settings-section">-->
<!--            <h3>API-Schlüssel</h3>-->

<!--            <div class="form-group">-->
<!--              <label for="binance-api-key">Binance API-Schlüssel</label>-->
<!--              <input type="password" id="binance-api-key" v-model="settings.trader.exchanges.binance.api_key">-->
<!--            </div>-->

<!--            <div class="form-group">-->
<!--              <label for="binance-api-secret">Binance API-Secret</label>-->
<!--              <input type="password" id="binance-api-secret" v-model="settings.trader.exchanges.binance.api_secret">-->
<!--            </div>-->

<!--            <div class="form-group">-->
<!--              <label for="binance-test-mode">Testmodus</label>-->
<!--              <div class="toggle-switch">-->
<!--                <input type="checkbox" id="binance-test-mode" v-model="settings.trader.exchanges.binance.test_mode">-->
<!--                <label for="binance-test-mode"></label>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->

<!--          <div v-if="errors.settings" class="error-box">-->
<!--            {{ errors.settings }}-->
<!--          </div>-->

<!--          <div class="settings-actions">-->
<!--            <button @click="saveSettings" class="primary-button" :disabled="loading.settings">-->
<!--              {{ loading.settings ? 'Wird gespeichert...' : 'Einstellungen speichern' }}-->
<!--            </button>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import axios from 'axios';-->
<!--import Chart from 'chart.js/auto';-->

<!--export default {-->
<!--  data() {-->
<!--    return {-->
<!--      activeTab: 'dashboard',-->
<!--      tradeTabActive: 'open',-->
<!--      isActive: false,-->
<!--      stats: {},-->
<!--      jobs: [],-->
<!--      openTrades: [],-->
<!--      closedTrades: [],-->
<!--      latestPrediction: null,-->
<!--      performanceChart: null,-->

<!--      predictionForm: {-->
<!--        symbol: 'BTC-USDT',-->
<!--        timeframe: '1h'-->
<!--      },-->

<!--      jobForm: {-->
<!--        symbol: 'BTC-USDT',-->
<!--        interval: '1h'-->
<!--      },-->

<!--      settings: {-->
<!--        trader: {-->
<!--          trading_enabled: false,-->
<!--          max_trades_per_day: 5,-->
<!--          trade_amount: 100,-->
<!--          stop_loss_pct: 2.0,-->
<!--          take_profit_pct: 3.0,-->
<!--          confidence_threshold: 0.7,-->
<!--          min_change_pct: 1.0,-->
<!--          exchanges: {-->
<!--            binance: {-->
<!--              api_key: '',-->
<!--              api_secret: '',-->
<!--              test_mode: true-->
<!--            }-->
<!--          },-->
<!--          risk_management: {-->
<!--            max_risk_per_trade: 2.0,-->
<!--            daily_drawdown_limit: 5.0-->
<!--          }-->
<!--        },-->
<!--        model: {-->
<!--          model_type: 'random_forest',-->
<!--          prediction_horizon: 1-->
<!--        }-->
<!--      },-->

<!--      // API-Request-Status-->
<!--      loading: {-->
<!--        status: false,-->
<!--        stats: false,-->
<!--        jobs: false,-->
<!--        trades: false,-->
<!--        prediction: false,-->
<!--        settings: false,-->
<!--        trade: false,-->
<!--        addJob: false,-->
<!--        removeJob: null-->
<!--      },-->

<!--      // Fehlermeldungen-->
<!--      errors: {-->
<!--        status: null,-->
<!--        stats: null,-->
<!--        jobs: null,-->
<!--        trades: null,-->
<!--        prediction: null,-->
<!--        settings: null,-->
<!--        predictionSymbol: null,-->
<!--        jobSymbol: null-->
<!--      },-->

<!--      // Globaler Fehler-->
<!--      globalError: null,-->

<!--      // Timer für automatische Aktualisierung-->
<!--      updateTimer: null-->
<!--    };-->
<!--  },-->

<!--  created() {-->
<!--    this.loadData();-->

<!--    // Daten periodisch aktualisieren-->
<!--    this.updateTimer = setInterval(this.loadData, 30000);-->
<!--  },-->

<!--  beforeUnmount() {-->
<!--    // Timer stoppen, wenn die Komponente zerstört wird-->
<!--    if (this.updateTimer) {-->
<!--      clearInterval(this.updateTimer);-->
<!--    }-->
<!--  },-->

<!--  mounted() {-->
<!--    // Performance-Chart initialisieren-->
<!--    this.$nextTick(() => {-->
<!--      this.initPerformanceChart();-->
<!--    });-->
<!--  },-->

<!--  computed: {-->
<!--    isLoading() {-->
<!--      // Prüfen, ob irgendein Ladevorgang aktiv ist-->
<!--      return Object.values(this.loading).some(status => status === true);-->
<!--    }-->
<!--  },-->

<!--  methods: {-->
<!--    loadData() {-->
<!--      this.loadStatus();-->
<!--      this.loadStats();-->
<!--      this.loadJobs();-->
<!--      this.loadTrades();-->
<!--      this.loadSettings();-->
<!--    },-->

<!--    async loadStatus() {-->
<!--      this.loading.status = true;-->
<!--      this.errors.status = null;-->

<!--      try {-->
<!--        const response = await axios.get('/status');-->
<!--        this.isActive = response.data.status === 'running';-->
<!--      } catch (error) {-->
<!--        this.errors.status = `Fehler beim Laden des Status: ${this.getErrorMessage(error)}`;-->
<!--        console.error('Fehler beim Laden des Status:', error);-->
<!--      } finally {-->
<!--        this.loading.status = false;-->
<!--      }-->
<!--    },-->

<!--    async loadStats() {-->
<!--      this.loading.stats = true;-->
<!--      this.errors.stats = null;-->

<!--      try {-->
<!--        const response = await axios.get('/stats');-->
<!--        this.stats = response.data;-->
<!--      } catch (error) {-->
<!--        this.errors.stats = `Fehler beim Laden der Statistiken: ${this.getErrorMessage(error)}`;-->
<!--        console.error('Fehler beim Laden der Statistiken:', error);-->
<!--      } finally {-->
<!--        this.loading.stats = false;-->
<!--      }-->
<!--    },-->

<!--    async loadJobs() {-->
<!--      this.loading.jobs = true;-->
<!--      this.errors.jobs = null;-->

<!--      try {-->
<!--        const response = await axios.get('/jobs');-->
<!--        this.jobs = response.data.jobs || [];-->
<!--      } catch (error) {-->
<!--        this.errors.jobs = `Fehler beim Laden der Jobs: ${this.getErrorMessage(error)}`;-->
<!--        console.error('Fehler beim Laden der Jobs:', error);-->
<!--      } finally {-->
<!--        this.loading.jobs = false;-->
<!--      }-->
<!--    },-->

<!--    async loadTrades() {-->
<!--      this.loading.trades = true;-->
<!--      this.errors.trades = null;-->

<!--      try {-->
<!--        // Offene Trades laden-->
<!--        const openResponse = await axios.get('/trades?status=open');-->
<!--        this.openTrades = openResponse.data.trades || [];-->

<!--        // Geschlossene Trades laden-->
<!--        const closedResponse = await axios.get('/trades?status=closed');-->
<!--        this.closedTrades = closedResponse.data.trades || [];-->
<!--      } catch (error) {-->
<!--        this.errors.trades = `Fehler beim Laden der Trades: ${this.getErrorMessage(error)}`;-->
<!--        console.error('Fehler beim Laden der Trades:', error);-->
<!--      } finally {-->
<!--        this.loading.trades = false;-->
<!--      }-->
<!--    },-->

<!--    async loadSettings() {-->
<!--      this.loading.settings = true;-->
<!--      this.errors.settings = null;-->

<!--      try {-->
<!--        const response = await axios.get('/config');-->

<!--        if (response.data.model_config) {-->
<!--          this.settings.model = response.data.model_config;-->
<!--        }-->

<!--        if (response.data.trader_config) {-->
<!--          this.settings.trader = response.data.trader_config;-->
<!--        }-->
<!--      } catch (error) {-->
<!--        this.errors.settings = `Fehler beim Laden der Einstellungen: ${this.getErrorMessage(error)}`;-->
<!--        console.error('Fehler beim Laden der Einstellungen:', error);-->
<!--      } finally {-->
<!--        this.loading.settings = false;-->
<!--      }-->
<!--    },-->

<!--    async makePrediction() {-->
<!--      // Formularvalidierung-->
<!--      this.errors.predictionSymbol = null;-->
<!--      this.errors.prediction = null;-->

<!--      if (!this.predictionForm.symbol || this.predictionForm.symbol.trim() === '') {-->
<!--        this.errors.predictionSymbol = 'Bitte geben Sie ein Symbol ein';-->
<!--        return;-->
<!--      }-->

<!--      this.loading.prediction = true;-->

<!--      try {-->
<!--        const response = await axios.post('/predict', this.predictionForm);-->
<!--        this.latestPrediction = response.data;-->
<!--      } catch (error) {-->
<!--        this.errors.prediction = `Fehler bei der Prognose: ${this.getErrorMessage(error)}`;-->
<!--        console.error('Fehler bei der Prognose:', error);-->
<!--      } finally {-->
<!--        this.loading.prediction = false;-->
<!--      }-->
<!--    },-->

<!--    async executeTrade(symbol, action) {-->
<!--      this.loading.trade = true;-->
<!--      this.globalError = null;-->

<!--      try {-->
<!--        const response = await axios.post('/trade', {-->
<!--          symbol: symbol,-->
<!--          action: action-->
<!--        });-->

<!--        if (response.data.success) {-->
<!--          // Erfolgsmeldung-->
<!--          this.globalError = `Trade erfolgreich ausgeführt: ${action.toUpperCase()} ${symbol}`;-->
<!--          // Trades neu laden-->
<!--          this.loadTrades();-->
<!--        } else {-->
<!--          this.globalError = `Fehler beim Ausführen des Trades: ${response.data.reason || 'Unbekannter Fehler'}`;-->
<!--        }-->
<!--      } catch (error) {-->
<!--        this.globalError = `Fehler beim Ausführen des Trades: ${this.getErrorMessage(error)}`;-->
<!--        console.error('Fehler beim Ausführen des Trades:', error);-->
<!--      } finally {-->
<!--        this.loading.trade = false;-->
<!--      }-->
<!--    },-->

<!--    async addJob() {-->
<!--      // Formularvalidierung-->
<!--      this.errors.jobSymbol = null;-->
<!--      this.errors.jobs = null;-->

<!--      if (!this.jobForm.symbol || this.jobForm.symbol.trim() === '') {-->
<!--        this.errors.jobSymbol = 'Bitte geben Sie ein Symbol ein';-->
<!--        return;-->
<!--      }-->

<!--      this.loading.addJob = true;-->

<!--      try {-->
<!--        const response = await axios.post('/jobs', this.jobForm);-->

<!--        if (response.data.job_id) {-->
<!--          this.globalError = `Job erfolgreich hinzugefügt: ${response.data.job_id}`;-->
<!--          // Jobs neu laden-->
<!--          this.loadJobs();-->
<!--        } else {-->
<!--          this.errors.jobs = 'Fehler beim Hinzufügen des Jobs';-->
<!--        }-->
<!--      } catch (error) {-->
<!--        this.errors.jobs = `Fehler beim Hinzufügen des Jobs: ${this.getErrorMessage(error)}`;-->
<!--        console.error('Fehler beim Hinzufügen des Jobs:', error);-->
<!--      } finally {-->
<!--        this.loading.addJob = false;-->
<!--      }-->
<!--    },-->

<!--    async removeJob(jobId) {-->
<!--      if (confirm(`Sind Sie sicher, dass Sie den Job ${jobId} löschen möchten?`)) {-->
<!--        this.loading.removeJob = jobId;-->
<!--        this.errors.jobs = null;-->

<!--        try {-->
<!--          const response = await axios.delete(`/jobs/${jobId}`);-->

<!--          if (response.data.message) {-->
<!--            this.globalError = response.data.message;-->
<!--            // Jobs neu laden-->
<!--            this.loadJobs();-->
<!--          } else {-->
<!--            this.errors.jobs = 'Fehler beim Löschen des Jobs';-->
<!--          }-->
<!--        } catch (error) {-->
<!--          this.errors.jobs = `Fehler beim Löschen des Jobs: ${this.getErrorMessage(error)}`;-->
<!--          console.error('Fehler beim Löschen des Jobs:', error);-->
<!--        } finally {-->
<!--          this.loading.removeJob = null;-->
<!--        }-->
<!--      }-->
<!--    },-->

<!--    async saveSettings() {-->
<!--      this.loading.settings = true;-->
<!--      this.errors.settings = null;-->

<!--      try {-->
<!--        // Trader-Einstellungen speichern-->
<!--        await axios.post('/api/config', {-->
<!--          section: 'trader',-->
<!--          config: this.settings.trader-->
<!--        });-->

<!--        // Modell-Einstellungen speichern-->
<!--        await axios.post('/api/config', {-->
<!--          section: 'model',-->
<!--          config: this.settings.model-->
<!--        });-->

<!--        this.globalError = 'Einstellungen erfolgreich gespeichert';-->
<!--      } catch (error) {-->
<!--        this.errors.settings = `Fehler beim Speichern der Einstellungen: ${this.getErrorMessage(error)}`;-->
<!--        console.error('Fehler beim Speichern der Einstellungen:', error);-->
<!--      } finally {-->
<!--        this.loading.settings = false;-->
<!--      }-->
<!--    },-->

<!--    formatTime(timestamp) {-->
<!--      if (!timestamp) return '';-->

<!--      const date = new Date(timestamp);-->
<!--      return date.toLocaleString();-->
<!--    },-->

<!--    formatCloseReason(reason) {-->
<!--      if (reason === 'stop_loss') return 'Stop-Loss';-->
<!--      if (reason === 'take_profit') return 'Take-Profit';-->
<!--      return reason || '';-->
<!--    },-->

<!--    extractSymbol(jobId) {-->
<!--      if (!jobId) return '';-->

<!--      // Format: predict_BTC-USDT_1h-->
<!--      const parts = jobId.split('_');-->
<!--      if (parts.length >= 2) {-->
<!--        return parts[1];-->
<!--      }-->

<!--      return jobId;-->
<!--    },-->

<!--    initPerformanceChart() {-->
<!--      if (!this.$refs.performanceChart) return;-->

<!--      const ctx = this.$refs.performanceChart.getContext('2d');-->

<!--      // Chart-Daten erstellen-->
<!--      const labels = [];-->
<!--      const profitLossData = [];-->

<!--      // Letzten 30 Tage generieren-->
<!--      const today = new Date();-->
<!--      for (let i = 30; i >= 0; i&#45;&#45;) {-->
<!--        const date = new Date();-->
<!--        date.setDate(today.getDate() - i);-->
<!--        labels.push(date.toLocaleDateString());-->

<!--        // Dummy-Daten für die Demonstration-->
<!--        const randomValue = Math.random() * 4 - 1; // Zwischen -1% und 3%-->
<!--        profitLossData.push(randomValue);-->
<!--      }-->

<!--      if (this.performanceChart) {-->
<!--        this.performanceChart.destroy();-->
<!--      }-->

<!--      // Chart erstellen-->
<!--      this.performanceChart = new Chart(ctx, {-->
<!--        type: 'line',-->
<!--        data: {-->
<!--          labels: labels,-->
<!--          datasets: [-->
<!--            {-->
<!--              label: 'Tägliche P/L (%)',-->
<!--              data: profitLossData,-->
<!--              borderColor: '#2a3f54',-->
<!--              backgroundColor: 'rgba(42, 63, 84, 0.1)',-->
<!--              tension: 0.4,-->
<!--              fill: true-->
<!--            }-->
<!--          ]-->
<!--        },-->
<!--        options: {-->
<!--          responsive: true,-->
<!--          maintainAspectRatio: false,-->
<!--          plugins: {-->
<!--            legend: {-->
<!--              position: 'top',-->
<!--            },-->
<!--            tooltip: {-->
<!--              callbacks: {-->
<!--                label: function(context) {-->
<!--                  return `${context.dataset.label}: ${context.raw.toFixed(2)}%`;-->
<!--                }-->
<!--              }-->
<!--            }-->
<!--          },-->
<!--          scales: {-->
<!--            y: {-->
<!--              beginAtZero: false,-->
<!--              grid: {-->
<!--                drawBorder: false-->
<!--              }-->
<!--            },-->
<!--            x: {-->
<!--              grid: {-->
<!--                display: false-->
<!--              }-->
<!--            }-->
<!--          }-->
<!--        }-->
<!--      });-->
<!--    },-->

<!--    updatePerformanceChart() {-->
<!--      if (!this.performanceChart) return;-->

<!--      // Nur die letzten 30 Datenpunkte behalten-->
<!--      const labels = [];-->
<!--      const profitLossData = [];-->

<!--      // Letzten 30 Tage generieren-->
<!--      const today = new Date();-->
<!--      for (let i = 30; i >= 0; i&#45;&#45;) {-->
<!--        const date = new Date();-->
<!--        date.setDate(today.getDate() - i);-->
<!--        labels.push(date.toLocaleDateString());-->

<!--        // Dummy-Daten für die Demonstration-->
<!--        const randomValue = Math.random() * 4 - 1; // Zwischen -1% und 3%-->
<!--        profitLossData.push(randomValue);-->
<!--      }-->

<!--      this.performanceChart.data.labels = labels;-->
<!--      this.performanceChart.data.datasets[0].data = profitLossData;-->
<!--      this.performanceChart.update();-->
<!--    },-->

<!--    dismissError() {-->
<!--      this.globalError = null;-->
<!--    },-->

<!--    getErrorMessage(error) {-->
<!--      if (error.response) {-->
<!--        // Der Server hat mit einem Statuscode außerhalb des 2xx-Bereichs geantwortet-->
<!--        if (error.response.data && error.response.data.detail) {-->
<!--          return error.response.data.detail;-->
<!--        }-->
<!--        return `${error.response.status} ${error.response.statusText}`;-->
<!--      } else if (error.request) {-->
<!--        // Die Anfrage wurde gesendet, aber keine Antwort erhalten-->
<!--        return 'Keine Antwort vom Server erhalten. Bitte überprüfen Sie Ihre Internetverbindung.';-->
<!--      } else {-->
<!--        // Etwas ist bei der Einrichtung der Anfrage schiefgegangen-->
<!--        return error.message || 'Unbekannter Fehler';-->
<!--      }-->
<!--    }-->
<!--  }-->
<!--}-->
<!--</script>-->

<!--<style>-->
<!--/* Grundstile */-->
<!--* {-->
<!--  box-sizing: border-box;-->
<!--  margin: 0;-->
<!--  padding: 0;-->
<!--}-->

<!--body {-->
<!--  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;-->
<!--  line-height: 1.6;-->
<!--  color: #333;-->
<!--  background-color: #f5f7fa;-->
<!--}-->

<!--.container {-->
<!--  max-width: 1400px;-->
<!--  margin: 0 auto;-->
<!--  padding: 20px;-->
<!--}-->

<!--/* Header */-->
<!--header {-->
<!--  display: flex;-->
<!--  justify-content: space-between;-->
<!--  align-items: center;-->
<!--  margin-bottom: 30px;-->
<!--  padding-bottom: 20px;-->
<!--  border-bottom: 1px solid #e0e0e0;-->
<!--}-->

<!--header h1 {-->
<!--  font-size: 28px;-->
<!--  color: #2a3f54;-->
<!--}-->

<!--.status-indicator {-->
<!--  display: inline-block;-->
<!--  padding: 8px 16px;-->
<!--  border-radius: 20px;-->
<!--  font-weight: bold;-->
<!--  background-color: #f0f0f0;-->
<!--  color: #888;-->
<!--}-->

<!--.status-indicator.active {-->
<!--  background-color: #d4edda;-->
<!--  color: #155724;-->
<!--}-->

<!--/* Layout */-->
<!--.main-content {-->
<!--  display: flex;-->
<!--  gap: 30px;-->
<!--}-->

<!--.sidebar {-->
<!--  width: 200px;-->
<!--  flex-shrink: 0;-->
<!--}-->

<!--.content {-->
<!--  flex-grow: 1;-->
<!--  background-color: white;-->
<!--  border-radius: 8px;-->
<!--  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);-->
<!--  padding: 30px;-->
<!--}-->

<!--/* Navigation */-->
<!--.sidebar nav {-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--  gap: 10px;-->
<!--}-->

<!--.sidebar button {-->
<!--  padding: 12px 15px;-->
<!--  text-align: left;-->
<!--  background-color: #f5f7fa;-->
<!--  border: 1px solid #e0e0e0;-->
<!--  border-radius: 8px;-->
<!--  cursor: pointer;-->
<!--  font-weight: 500;-->
<!--  transition: all 0.2s;-->
<!--}-->

<!--.sidebar button.active {-->
<!--  background-color: #2a3f54;-->
<!--  color: white;-->
<!--  border-color: #2a3f54;-->
<!--}-->

<!--.sidebar button:hover:not(.active) {-->
<!--  background-color: #e9ecef;-->
<!--}-->

<!--/* Tabs */-->
<!--.tab-content {-->
<!--  min-height: 500px;-->
<!--}-->

<!--.tab-content h2 {-->
<!--  font-size: 24px;-->
<!--  margin-bottom: 25px;-->
<!--  color: #2a3f54;-->
<!--}-->

<!--.tabs {-->
<!--  display: flex;-->
<!--  margin-bottom: 20px;-->
<!--  border-bottom: 1px solid #e0e0e0;-->
<!--}-->

<!--.tabs button {-->
<!--  padding: 10px 20px;-->
<!--  background: none;-->
<!--  border: none;-->
<!--  border-bottom: 3px solid transparent;-->
<!--  cursor: pointer;-->
<!--  font-weight: 500;-->
<!--  color: #666;-->
<!--}-->

<!--.tabs button.active {-->
<!--  color: #2a3f54;-->
<!--  border-bottom-color: #2a3f54;-->
<!--}-->

<!--/* Statistik-Karten */-->
<!--.stats-grid {-->
<!--  display: grid;-->
<!--  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));-->
<!--  gap: 20px;-->
<!--  margin-bottom: 30px;-->
<!--}-->

<!--.stat-card {-->
<!--  background-color: white;-->
<!--  border-radius: 8px;-->
<!--  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);-->
<!--  padding: 20px;-->
<!--  border: 1px solid #e0e0e0;-->
<!--}-->

<!--.stat-card h3 {-->
<!--  font-size: 14px;-->
<!--  color: #666;-->
<!--  margin-bottom: 10px;-->
<!--}-->

<!--.stat-value {-->
<!--  font-size: 24px;-->
<!--  font-weight: bold;-->
<!--  color: #2a3f54;-->
<!--}-->

<!--.positive {-->
<!--  color: #28a745;-->
<!--}-->

<!--.negative {-->
<!--  color: #dc3545;-->
<!--}-->

<!--/* Charts */-->
<!--.chart-container {-->
<!--  margin-bottom: 30px;-->
<!--}-->

<!--.chart-placeholder {-->
<!--  height: 300px;-->
<!--  background-color: #f5f7fa;-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--  justify-content: center;-->
<!--  border-radius: 8px;-->
<!--  border: 1px dashed #ccc;-->
<!--  color: #888;-->
<!--}-->

<!--/* Symbole */-->
<!--.active-symbols {-->
<!--  margin-bottom: 30px;-->
<!--}-->

<!--.symbols-list {-->
<!--  display: grid;-->
<!--  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));-->
<!--  gap: 15px;-->
<!--}-->

<!--.symbol-item {-->
<!--  padding: 15px;-->
<!--  border-radius: 8px;-->
<!--  border: 1px solid #e0e0e0;-->
<!--  background-color: #f9f9f9;-->
<!--}-->

<!--.symbol-name {-->
<!--  font-weight: bold;-->
<!--  font-size: 18px;-->
<!--  margin-bottom: 5px;-->
<!--}-->

<!--.symbol-next-run {-->
<!--  color: #666;-->
<!--  font-size: 14px;-->
<!--}-->

<!--/* Formulare */-->
<!--.form-group {-->
<!--  margin-bottom: 15px;-->
<!--}-->

<!--.form-group label {-->
<!--  display: block;-->
<!--  margin-bottom: 8px;-->
<!--  font-weight: 500;-->
<!--}-->

<!--input[type="text"],-->
<!--input[type="number"],-->
<!--input[type="password"],-->
<!--select {-->
<!--  width: 100%;-->
<!--  padding: 10px;-->
<!--  border: 1px solid #ddd;-->
<!--  border-radius: 4px;-->
<!--  font-size: 16px;-->
<!--}-->

<!--.primary-button {-->
<!--  background-color: #2a3f54;-->
<!--  color: white;-->
<!--  border: none;-->
<!--  padding: 10px 20px;-->
<!--  border-radius: 4px;-->
<!--  cursor: pointer;-->
<!--  font-weight: 500;-->
<!--  font-size: 16px;-->
<!--}-->

<!--.primary-button:hover {-->
<!--  background-color: #1f2f3d;-->
<!--}-->

<!--.primary-button:disabled {-->
<!--  background-color: #97a4b3;-->
<!--  cursor: not-allowed;-->
<!--}-->

<!--.delete-button {-->
<!--  background-color: #dc3545;-->
<!--  color: white;-->
<!--  border: none;-->
<!--  padding: 6px 12px;-->
<!--  border-radius: 4px;-->
<!--  cursor: pointer;-->
<!--}-->

<!--.delete-button:hover {-->
<!--  background-color: #c82333;-->
<!--}-->

<!--.delete-button:disabled {-->
<!--  background-color: #e48690;-->
<!--  cursor: not-allowed;-->
<!--}-->

<!--.action-button {-->
<!--  padding: 8px 16px;-->
<!--  border: none;-->
<!--  border-radius: 4px;-->
<!--  cursor: pointer;-->
<!--  font-weight: 500;-->
<!--}-->

<!--.action-button:disabled {-->
<!--  opacity: 0.7;-->
<!--  cursor: not-allowed;-->
<!--}-->

<!--.buy-button {-->
<!--  background-color: #28a745;-->
<!--  color: white;-->
<!--}-->

<!--.buy-button:hover:not(:disabled) {-->
<!--  background-color: #218838;-->
<!--}-->

<!--.sell-button {-->
<!--  background-color: #dc3545;-->
<!--  color: white;-->
<!--}-->

<!--.sell-button:hover:not(:disabled) {-->
<!--  background-color: #c82333;-->
<!--}-->

<!--/* Prognosen */-->
<!--.prediction-form {-->
<!--  background-color: #f9f9f9;-->
<!--  padding: 20px;-->
<!--  border-radius: 8px;-->
<!--  margin-bottom: 30px;-->
<!--}-->

<!--.prediction-result {-->
<!--  margin-bottom: 30px;-->
<!--}-->

<!--.prediction-card {-->
<!--  border: 1px solid #e0e0e0;-->
<!--  border-radius: 8px;-->
<!--  padding: 20px;-->
<!--  background-color: white;-->
<!--}-->

<!--.prediction-header {-->
<!--  display: flex;-->
<!--  justify-content: space-between;-->
<!--  margin-bottom: 15px;-->
<!--  padding-bottom: 10px;-->
<!--  border-bottom: 1px solid #eee;-->
<!--}-->

<!--.prediction-symbol {-->
<!--  font-size: 20px;-->
<!--  font-weight: bold;-->
<!--}-->

<!--.prediction-time {-->
<!--  color: #666;-->
<!--}-->

<!--.prediction-details {-->
<!--  margin-bottom: 20px;-->
<!--}-->

<!--.prediction-row {-->
<!--  display: flex;-->
<!--  justify-content: space-between;-->
<!--  margin-bottom: 10px;-->
<!--}-->

<!--.prediction-label {-->
<!--  font-weight: 500;-->
<!--}-->

<!--.prediction-actions {-->
<!--  display: flex;-->
<!--  justify-content: flex-end;-->
<!--}-->

<!--/* Trades und Jobs Tabellen */-->
<!--.trades-table, .jobs-table {-->
<!--  width: 100%;-->
<!--  border-collapse: collapse;-->
<!--}-->

<!--.trades-header, .jobs-header {-->
<!--  background-color: #f5f7fa;-->
<!--  font-weight: bold;-->
<!--}-->

<!--.trade-row, .job-row {-->
<!--  border-bottom: 1px solid #eee;-->
<!--}-->

<!--.trade-cell, .job-cell {-->
<!--  padding: 12px 15px;-->
<!--  text-align: left;-->
<!--}-->

<!--.trade-row:last-child, .job-row:last-child {-->
<!--  border-bottom: none;-->
<!--}-->

<!--.buy {-->
<!--  color: #28a745;-->
<!--}-->

<!--.sell {-->
<!--  color: #dc3545;-->
<!--}-->

<!--.empty-state {-->
<!--  padding: 30px;-->
<!--  text-align: center;-->
<!--  color: #888;-->
<!--  background-color: #f9f9f9;-->
<!--  border-radius: 8px;-->
<!--}-->

<!--/* Einstellungen */-->
<!--.settings-section {-->
<!--  margin-bottom: 30px;-->
<!--  padding: 20px;-->
<!--  background-color: #f9f9f9;-->
<!--  border-radius: 8px;-->
<!--}-->

<!--.settings-section h3 {-->
<!--  margin-bottom: 20px;-->
<!--  padding-bottom: 10px;-->
<!--  border-bottom: 1px solid #eee;-->
<!--}-->

<!--.settings-actions {-->
<!--  margin-top: 30px;-->
<!--}-->

<!--/* Toggle Switch */-->
<!--.toggle-switch {-->
<!--  position: relative;-->
<!--  display: inline-block;-->
<!--  width: 50px;-->
<!--  height: 24px;-->
<!--}-->

<!--.toggle-switch input {-->
<!--  opacity: 0;-->
<!--  width: 0;-->
<!--  height: 0;-->
<!--}-->

<!--.toggle-switch label {-->
<!--  position: absolute;-->
<!--  cursor: pointer;-->
<!--  top: 0;-->
<!--  left: 0;-->
<!--  right: 0;-->
<!--  bottom: 0;-->
<!--  background-color: #ccc;-->
<!--  transition: .4s;-->
<!--  border-radius: 34px;-->
<!--}-->

<!--.toggle-switch label:before {-->
<!--  position: absolute;-->
<!--  content: "";-->
<!--  height: 16px;-->
<!--  width: 16px;-->
<!--  left: 4px;-->
<!--  bottom: 4px;-->
<!--  background-color: white;-->
<!--  transition: .4s;-->
<!--  border-radius: 50%;-->
<!--}-->

<!--.toggle-switch input:checked + label {-->
<!--  background-color: #2a3f54;-->
<!--}-->

<!--.toggle-switch input:checked + label:before {-->
<!--  transform: translateX(26px);-->
<!--}-->

<!--/* Fehlerboxen */-->
<!--.error-box {-->
<!--  background-color: #f8d7da;-->
<!--  color: #721c24;-->
<!--  padding: 12px;-->
<!--  border-radius: 4px;-->
<!--  margin-bottom: 20px;-->
<!--  border: 1px solid #f5c6cb;-->
<!--}-->

<!--.error-hint {-->
<!--  color: #dc3545;-->
<!--  font-size: 12px;-->
<!--  margin-top: 5px;-->
<!--}-->

<!--.error-message {-->
<!--  position: fixed;-->
<!--  top: 80px;-->
<!--  right: 20px;-->
<!--  background-color: rgba(42, 63, 84, 0.9);-->
<!--  color: white;-->
<!--  padding: 15px;-->
<!--  border-radius: 4px;-->
<!--  max-width: 350px;-->
<!--  z-index: 1000;-->
<!--  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);-->
<!--  display: flex;-->
<!--  justify-content: space-between;-->
<!--  align-items: flex-start;-->
<!--}-->

<!--.dismiss-button {-->
<!--  background: none;-->
<!--  border: none;-->
<!--  color: white;-->
<!--  font-size: 18px;-->
<!--  cursor: pointer;-->
<!--  margin-left: 10px;-->
<!--}-->

<!--/* Lademeldungen */-->
<!--.loading-overlay {-->
<!--  position: fixed;-->
<!--  top: 0;-->
<!--  left: 0;-->
<!--  width: 100%;-->
<!--  height: 100%;-->
<!--  background-color: rgba(255, 255, 255, 0.7);-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--  justify-content: center;-->
<!--  align-items: center;-->
<!--  z-index: 1000;-->
<!--}-->

<!--.loading-spinner {-->
<!--  border: 4px solid #f3f3f3;-->
<!--  border-top: 4px solid #2a3f54;-->
<!--  border-radius: 50%;-->
<!--  width: 40px;-->
<!--  height: 40px;-->
<!--  animation: spin 1s linear infinite;-->
<!--  margin-bottom: 10px;-->
<!--}-->

<!--.loading-text {-->
<!--  color: #2a3f54;-->
<!--  font-weight: 500;-->
<!--}-->

<!--@keyframes spin {-->
<!--  0% { transform: rotate(0deg); }-->
<!--  100% { transform: rotate(360deg); }-->
<!--}-->
<!--</style>-->


<template>
  <div class="container">
    <header>
      <h1>TradeBot - Prädiktiver Handelsbot</h1>
      <div class="status-indicator" :class="{ active: isActive }">
        {{ isActive ? 'Aktiv' : 'Inaktiv' }}
      </div>
    </header>

    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <div class="loading-text">Daten werden geladen...</div>
    </div>

    <div v-if="globalError" class="error-message">
      {{ globalError }}
      <button @click="dismissError" class="dismiss-button">×</button>
    </div>

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
              <div class="stat-value" :class="{ positive: (stats.daily_profit_loss || 0) > 0, negative: (stats.daily_profit_loss || 0) < 0 }">
                {{ stats.daily_profit_loss ? stats.daily_profit_loss.toFixed(2) + '%' : '0.00%' }}
              </div>
            </div>

            <div class="stat-card">
              <h3>Gewinnrate</h3>
              <div class="stat-value">{{ stats.win_rate ? stats.win_rate.toFixed(2) + '%' : '0.00%' }}</div>
            </div>
          </div>

<!--          <div class="chart-container">-->
<!--            <h3>Performance Übersicht</h3>-->
<!--            <canvas ref="performanceChart" width="400" height="200"></canvas>-->
<!--          </div>-->

          <div class="chart-container">
  <h3>Performance Übersicht</h3>
  <div class="performance-data">
    <div v-for="(value, index) in performanceData" :key="index"
         class="performance-item"
         :style="{ height: `${Math.abs(value*10)}px` }"
         :class="{ 'positive': value > 0, 'negative': value < 0 }">
    </div>
  </div>
  <div class="performance-legend">
    <div class="positive">Positiv</div>
    <div class="negative">Negativ</div>
  </div>
</div>

          <div class="active-symbols">
            <h3>Aktive Symbole</h3>
            <div v-if="jobs.length === 0" class="empty-state">
              Keine aktiven Symbole
            </div>
            <div v-else class="symbols-list">
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
              <div v-if="errors.predictionSymbol" class="error-hint">{{ errors.predictionSymbol }}</div>
            </div>

            <div class="form-group">
              <label for="prediction-timeframe">Zeitrahmen</label>
              <select id="prediction-timeframe" v-model="predictionForm.timeframe">
                <option value="1h">1 Stunde</option>
                <option value="4h">4 Stunden</option>
                <option value="1d">1 Tag</option>
              </select>
            </div>

            <button @click="makePrediction" class="primary-button" :disabled="loading.prediction">
              {{ loading.prediction ? 'Wird berechnet...' : 'Prognose erstellen' }}
            </button>
          </div>

          <div v-if="errors.prediction" class="error-box">
            {{ errors.prediction }}
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
                        :class="{ 'buy-button': latestPrediction.direction === 'up', 'sell-button': latestPrediction.direction === 'down' }"
                        :disabled="loading.trade">
                  {{ loading.trade ? 'Wird ausgeführt...' : (latestPrediction.direction === 'up' ? 'Kaufen' : 'Verkaufen') }}
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
                <div class="trade-cell">{{ trade.price ? trade.price.toFixed(2) : '0.00' }}</div>
                <div class="trade-cell">{{ trade.amount ? trade.amount.toFixed(2) : '0.00' }}</div>
                <div class="trade-cell">{{ formatTime(trade.timestamp) }}</div>
                <div class="trade-cell">{{ trade.stop_loss ? trade.stop_loss.toFixed(2) : '0.00' }}</div>
                <div class="trade-cell">{{ trade.take_profit ? trade.take_profit.toFixed(2) : '0.00' }}</div>
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
                <div class="trade-cell">{{ trade.price ? trade.price.toFixed(2) : '0.00' }}</div>
                <div class="trade-cell">{{ trade.close_price ? trade.close_price.toFixed(2) : '0.00' }}</div>
                <div class="trade-cell" :class="{ 'positive': trade.profit_loss > 0, 'negative': trade.profit_loss < 0 }">
                  {{ trade.profit_loss ? trade.profit_loss.toFixed(2) : '0.00' }}%
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
              <div v-if="errors.jobSymbol" class="error-hint">{{ errors.jobSymbol }}</div>
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

            <button @click="addJob" class="primary-button" :disabled="loading.addJob">
              {{ loading.addJob ? 'Wird hinzugefügt...' : 'Job hinzufügen' }}
            </button>
          </div>

          <div v-if="errors.jobs" class="error-box">
            {{ errors.jobs }}
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
                  <button @click="removeJob(job.id)" class="delete-button" :disabled="loading.removeJob === job.id">
                    {{ loading.removeJob === job.id ? 'Wird gelöscht...' : 'Löschen' }}
                  </button>
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
              <input type="number" id="max-trades-day" v-model.number="settings.trader.max_trades_per_day" min="1" max="50">
            </div>

            <div class="form-group">
              <label for="trade-amount">Betrag pro Trade</label>
              <input type="number" id="trade-amount" v-model.number="settings.trader.trade_amount" min="1">
            </div>
          </div>

          <div class="settings-section">
            <h3>Risikomanagement</h3>

            <div class="form-group">
              <label for="stop-loss">Stop-Loss (%)</label>
              <input type="number" id="stop-loss" v-model.number="settings.trader.stop_loss_pct" min="0.1" max="10" step="0.1">
            </div>

            <div class="form-group">
              <label for="take-profit">Take-Profit (%)</label>
              <input type="number" id="take-profit" v-model.number="settings.trader.take_profit_pct" min="0.1" max="20" step="0.1">
            </div>

            <div class="form-group">
              <label for="max-risk">Maximales Risiko pro Trade (%)</label>
              <input type="number" id="max-risk"
                    v-model.number="settings.trader.risk_management && settings.trader.risk_management.max_risk_per_trade !== undefined
                      ? settings.trader.risk_management.max_risk_per_trade
                      : 2.0"
                    min="0.1" max="10" step="0.1">
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
              <input type="number" id="prediction-horizon" v-model.number="settings.model.prediction_horizon" min="1" max="24">
            </div>

            <div class="form-group">
              <label for="confidence-threshold">Vertrauensschwelle</label>
              <input type="number" id="confidence-threshold" v-model.number="settings.trader.confidence_threshold" min="0.1" max="1" step="0.05">
            </div>

            <div class="form-group">
              <label for="min-change">Minimale Änderung für Trade (%)</label>
              <input type="number" id="min-change" v-model.number="settings.trader.min_change_pct" min="0.1" max="5" step="0.1">
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

          <div v-if="errors.settings" class="error-box">
            {{ errors.settings }}
          </div>

          <div class="settings-actions">
            <button @click="saveSettings" class="primary-button" :disabled="loading.settings">
              {{ loading.settings ? 'Wird gespeichert...' : 'Einstellungen speichern' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
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
      },

      // API-Request-Status
      loading: {
        status: false,
        stats: false,
        jobs: false,
        trades: false,
        prediction: false,
        settings: false,
        trade: false,
        addJob: false,
        removeJob: null
      },

      // Fehlermeldungen
      errors: {
        status: null,
        stats: null,
        jobs: null,
        trades: null,
        prediction: null,
        settings: null,
        predictionSymbol: null,
        jobSymbol: null
      },

      // Globaler Fehler
      globalError: null,

      // Timer für automatische Aktualisierung
      updateTimer: null
    };
  },

  created() {
    this.loadData();

    // Daten periodisch aktualisieren
    this.updateTimer = setInterval(this.loadData, 30000);
  },

  beforeUnmount() {
    // Timer stoppen, wenn die Komponente zerstört wird
    if (this.updateTimer) {
      clearInterval(this.updateTimer);
    }

    // Chart aufräumen
    if (this.performanceChart) {
      this.performanceChart.destroy();
      this.performanceChart = null;
    }
  },

  mounted() {
    // Performance-Chart initialisieren
    this.$nextTick(() => {
      this.initPerformanceChart();
    });
  },

  computed: {
    isLoading() {
      // Prüfen, ob irgendein Ladevorgang aktiv ist
      return Object.values(this.loading).some(status => status === true && status !== null);
    }
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
      this.loading.status = true;
      this.errors.status = null;

      try {
        const response = await axios.get('/api/status');
        this.isActive = response.data.status === 'running';
      } catch (error) {
        this.errors.status = `Fehler beim Laden des Status: ${this.getErrorMessage(error)}`;
        console.error('Fehler beim Laden des Status:', error);
      } finally {
        this.loading.status = false;
      }
    },

    async loadStats() {
      this.loading.stats = true;
      this.errors.stats = null;

      try {
        const response = await axios.get('/api/stats');
        this.stats = response.data;
      } catch (error) {
        this.errors.stats = `Fehler beim Laden der Statistiken: ${this.getErrorMessage(error)}`;
        console.error('Fehler beim Laden der Statistiken:', error);
      } finally {
        this.loading.stats = false;
      }
    },

    async loadJobs() {
      this.loading.jobs = true;
      this.errors.jobs = null;

      try {
        const response = await axios.get('/api/jobs');
        this.jobs = response.data.jobs || [];
      } catch (error) {
        this.errors.jobs = `Fehler beim Laden der Jobs: ${this.getErrorMessage(error)}`;
        console.error('Fehler beim Laden der Jobs:', error);
      } finally {
        this.loading.jobs = false;
      }
    },

    async loadTrades() {
      this.loading.trades = true;
      this.errors.trades = null;

      try {
        // Offene Trades laden
        const openResponse = await axios.get('/api/trades?status=open');
        this.openTrades = openResponse.data.trades || [];

        // Geschlossene Trades laden
        const closedResponse = await axios.get('/api/trades?status=closed');
        this.closedTrades = closedResponse.data.trades || [];
      } catch (error) {
        this.errors.trades = `Fehler beim Laden der Trades: ${this.getErrorMessage(error)}`;
        console.error('Fehler beim Laden der Trades:', error);
      } finally {
        this.loading.trades = false;
      }
    },

    async loadSettings() {
      this.loading.settings = true;
      this.errors.settings = null;

      try {
        const response = await axios.get('/api/config');

        if (response.data.model_config) {
          this.settings.model = response.data.model_config;
        }

        if (response.data.trader_config) {
          // Sicherstellen, dass risk_management existiert
          if (!response.data.trader_config.risk_management) {
            response.data.trader_config.risk_management = {
              max_risk_per_trade: 2.0,
              daily_drawdown_limit: 5.0
            };
          }
          this.settings.trader = response.data.trader_config;
        }
      } catch (error) {
        this.errors.settings = `Fehler beim Laden der Einstellungen: ${this.getErrorMessage(error)}`;
        console.error('Fehler beim Laden der Einstellungen:', error);
      } finally {
        this.loading.settings = false;
      }
    },

    async makePrediction() {
      // Formularvalidierung
      this.errors.predictionSymbol = null;
      this.errors.prediction = null;

      if (!this.predictionForm.symbol || this.predictionForm.symbol.trim() === '') {
        this.errors.predictionSymbol = 'Bitte geben Sie ein Symbol ein';
        return;
      }

      this.loading.prediction = true;

      try {
        const response = await axios.post('/api/predict', this.predictionForm);
        this.latestPrediction = response.data;
      } catch (error) {
        this.errors.prediction = `Fehler bei der Prognose: ${this.getErrorMessage(error)}`;
        console.error('Fehler bei der Prognose:', error);
      } finally {
        this.loading.prediction = false;
      }
    },

    async executeTrade(symbol, action) {
      this.loading.trade = true;
      this.globalError = null;

      try {
        const response = await axios.post('/api/trade', {
          symbol: symbol,
          action: action
        });

        if (response.data.success) {
          // Erfolgsmeldung
          this.globalError = `Trade erfolgreich ausgeführt: ${action.toUpperCase()} ${symbol}`;
          // Trades neu laden
          this.loadTrades();
        } else {
          this.globalError = `Fehler beim Ausführen des Trades: ${response.data.reason || 'Unbekannter Fehler'}`;
        }
      } catch (error) {
        this.globalError = `Fehler beim Ausführen des Trades: ${this.getErrorMessage(error)}`;
        console.error('Fehler beim Ausführen des Trades:', error);
      } finally {
        this.loading.trade = false;
      }
    },

    async addJob() {
      // Formularvalidierung
      this.errors.jobSymbol = null;
      this.errors.jobs = null;

      if (!this.jobForm.symbol || this.jobForm.symbol.trim() === '') {
        this.errors.jobSymbol = 'Bitte geben Sie ein Symbol ein';
        return;
      }

      this.loading.addJob = true;

      try {
        const response = await axios.post('/api/jobs', this.jobForm);

        if (response.data.job_id) {
          this.globalError = `Job erfolgreich hinzugefügt: ${response.data.job_id}`;
          // Jobs neu laden
          this.loadJobs();
        } else {
          this.errors.jobs = 'Fehler beim Hinzufügen des Jobs';
        }
      } catch (error) {
        this.errors.jobs = `Fehler beim Hinzufügen des Jobs: ${this.getErrorMessage(error)}`;
        console.error('Fehler beim Hinzufügen des Jobs:', error);
      } finally {
        this.loading.addJob = false;
      }
    },

    async removeJob(jobId) {
      if (confirm(`Sind Sie sicher, dass Sie den Job ${jobId} löschen möchten?`)) {
        this.loading.removeJob = jobId;
        this.errors.jobs = null;

        try {
          const response = await axios.delete(`/api/jobs/${jobId}`);

          if (response.data.message) {
            this.globalError = response.data.message;
            // Jobs neu laden
            this.loadJobs();
          } else {
            this.errors.jobs = 'Fehler beim Löschen des Jobs';
          }
        } catch (error) {
          this.errors.jobs = `Fehler beim Löschen des Jobs: ${this.getErrorMessage(error)}`;
          console.error('Fehler beim Löschen des Jobs:', error);
        } finally {
          this.loading.removeJob = null;
        }
      }
    },

    async saveSettings() {
      this.loading.settings = true;
      this.errors.settings = null;

      try {
        // Sicherstellen, dass risk_management existiert
        if (!this.settings.trader.risk_management) {
          this.settings.trader.risk_management = {
            max_risk_per_trade: 2.0,
            daily_drawdown_limit: 5.0
          };
        }

        // Trader-Einstellungen speichern
        await axios.post('/api/config', {
          section: 'trader',
          config: this.settings.trader
        });

        // Modell-Einstellungen speichern
        await axios.post('/api/config', {
          section: 'model',
          config: this.settings.model
        });

        this.globalError = 'Einstellungen erfolgreich gespeichert';
      } catch (error) {
        this.errors.settings = `Fehler beim Speichern der Einstellungen: ${this.getErrorMessage(error)}`;
        console.error('Fehler beim Speichern der Einstellungen:', error);
      } finally {
        this.loading.settings = false;
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
      return reason || '';
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

    // initPerformanceChart() {
    //   if (!this.$refs.performanceChart) return;
    //
    //   // Chart.js global deaktivieren
    //   Chart.defaults.animation = false;
    //   Chart.defaults.animations = {
    //     colors: false,
    //     x: false,
    //     y: false
    //   };
    //   Chart.defaults.transitions.active.animation.duration = 0;
    //
    //   const ctx = this.$refs.performanceChart.getContext('2d');
    //
    //   // Daten erzeugen
    //   const labels = [];
    //   const profitLossData = [];
    //
    //   const today = new Date();
    //   for (let i = 30; i >= 0; i--) {
    //     const date = new Date();
    //     date.setDate(today.getDate() - i);
    //     labels.push(date.toLocaleDateString());
    //     const randomValue = Math.random() * 4 - 1;
    //     profitLossData.push(randomValue);
    //   }
    //
    //   if (this.performanceChart) {
    //     this.performanceChart.destroy();
    //   }
    //
    //   this.performanceChart = new Chart(ctx, {
    //     type: 'line',
    //     data: {
    //       labels: labels,
    //       datasets: [{
    //         label: 'Tägliche P/L (%)',
    //         data: profitLossData,
    //         borderColor: '#2a3f54',
    //         backgroundColor: 'rgba(42, 63, 84, 0.1)',
    //         tension: 0.4,
    //         fill: true,
    //         animation: false
    //       }]
    //     },
    //     options: {
    //       animation: false,
    //       animations: {
    //         colors: false,
    //         x: false,
    //         y: false
    //       },
    //       responsive: true,
    //       maintainAspectRatio: false,
    //       interaction: {
    //         mode: 'nearest',
    //         intersect: false,
    //         axis: 'x'
    //       },
    //       plugins: {
    //         legend: {
    //           position: 'top',
    //         },
    //         tooltip: {
    //           enabled: true,
    //           animation: false,
    //           callbacks: {
    //             label: function(context) {
    //               return `${context.dataset.label}: ${context.raw.toFixed(2)}%`;
    //             }
    //           }
    //         }
    //       },
    //       scales: {
    //         y: {
    //           beginAtZero: false,
    //           grid: {
    //             drawBorder: false
    //           },
    //           ticks: {
    //             animation: false
    //           }
    //         },
    //         x: {
    //           grid: {
    //             display: false
    //           },
    //           ticks: {
    //             animation: false
    //           }
    //         }
    //       },
    //       transitions: {
    //         active: {
    //           animation: {
    //             duration: 0
    //           }
    //         }
    //       }
    //     }
    //   });
    // },


    initPerformanceChart() {
  if (!this.$refs.performanceChart) return;

  const ctx = this.$refs.performanceChart.getContext('2d');

  // Daten erzeugen
  const labels = [];
  const profitLossData = [];

  const today = new Date();
  for (let i = 30; i >= 0; i--) {
    const date = new Date();
    date.setDate(today.getDate() - i);
    labels.push(date.toLocaleDateString());
    const randomValue = Math.random() * 4 - 1;
    profitLossData.push(randomValue);
  }

  if (this.performanceChart) {
    this.performanceChart.destroy();
  }

  // Chart mit Chart.js V2 erstellen
  this.performanceChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Tägliche P/L (%)',
        data: profitLossData,
        borderColor: '#2a3f54',
        backgroundColor: 'rgba(42, 63, 84, 0.1)',
        fill: true
      }]
    },
    options: {
      animation: {
        duration: 0
      },
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        position: 'top'
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          },
          gridLines: {
            drawBorder: false
          }
        }],
        xAxes: [{
          gridLines: {
            display: false
          }
        }]
      }
    }
  });
},

    updatePerformanceChart() {
      if (!this.performanceChart) return;

      // Nur die letzten 30 Datenpunkte behalten
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

      this.performanceChart.data.labels = labels;
      this.performanceChart.data.datasets[0].data = profitLossData;
      this.performanceChart.update({
        duration: 0 // Animationen deaktivieren
      });
    },

    dismissError() {
      this.globalError = null;
    },

    getErrorMessage(error) {
      if (error.response) {
        // Der Server hat mit einem Statuscode außerhalb des 2xx-Bereichs geantwortet
        if (error.response.data && error.response.data.detail) {
          return error.response.data.detail;
        }
        return `${error.response.status} ${error.response.statusText}`;
      } else if (error.request) {
        // Die Anfrage wurde gesendet, aber keine Antwort erhalten
        return 'Keine Antwort vom Server erhalten. Bitte überprüfen Sie Ihre Internetverbindung.';
      } else {
        // Etwas ist bei der Einrichtung der Anfrage schiefgegangen
        return error.message || 'Unbekannter Fehler';
      }
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

.primary-button:disabled {
  background-color: #97a4b3;
  cursor: not-allowed;
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

.delete-button:disabled {
  background-color: #e48690;
  cursor: not-allowed;
}

.action-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.action-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.buy-button {
  background-color: #28a745;
  color: white;
}

.buy-button:hover:not(:disabled) {
  background-color: #218838;
}

.sell-button {
  background-color: #dc3545;
  color: white;
}

.sell-button:hover:not(:disabled) {
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

/* Fehlerboxen */
.error-box {
  background-color: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 20px;
  border: 1px solid #f5c6cb;
}

.error-hint {
  color: #dc3545;
  font-size: 12px;
  margin-top: 5px;
}

.error-message {
  position: fixed;
  top: 80px;
  right: 20px;
  background-color: rgba(42, 63, 84, 0.9);
  color: white;
  padding: 15px;
  border-radius: 4px;
  max-width: 350px;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.dismiss-button {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  margin-left: 10px;
}

/* Lademeldungen */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #2a3f54;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

.loading-text {
  color: #2a3f54;
  font-weight: 500;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>