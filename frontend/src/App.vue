<template>
  <div class="app-container">
    <header class="app-header">
      <h1 class="app-title">TradeBot</h1>
      <div class="status-badge" :class="{ active: isActive }">
        {{ isActive ? 'Aktiv' : 'Inaktiv' }}
      </div>
    </header>

    <!-- Global Loading Overlay -->
    <LoadingOverlay v-if="isLoading" />

    <!-- Global Toast/Notification -->
    <Toast
      v-if="globalMessage"
      :message="globalMessage.text"
      :type="globalMessage.type"
      @dismiss="dismissMessage"
    />

    <main class="app-content">
      <aside class="app-sidebar">
        <nav class="nav-menu">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="nav-item"
            :class="{ active: activeTab === tab.id }"
          >
            <span class="nav-icon" v-html="tab.icon"></span>
            <span class="nav-label">{{ tab.label }}</span>
          </button>
        </nav>
      </aside>

      <section class="page-container">
        <!-- Dashboard -->
        <DashboardPage v-if="activeTab === 'dashboard'"
          :stats="stats"
          :jobs="jobs"
          @error="setErrorMessage"
        />

        <!-- Predictions -->
        <PredictionsPage v-if="activeTab === 'predictions'"
          :latestPrediction="latestPrediction"
          @make-prediction="makePrediction"
          @execute-trade="executeTrade"
          @error="setErrorMessage"
        />

        <!-- Trades -->
        <TradesPage v-if="activeTab === 'trades'"
          :openTrades="openTrades"
          :closedTrades="closedTrades"
          @error="setErrorMessage"
        />

        <!-- Jobs -->
        <JobsPage v-if="activeTab === 'jobs'"
          :jobs="jobs"
          @add-job="addJob"
          @remove-job="removeJob"
          @error="setErrorMessage"
        />

        <!-- Settings -->
        <SettingsPage v-if="activeTab === 'settings'"
          :settings="settings"
          @save-settings="saveSettings"
          @error="setErrorMessage"
        />
      </section>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
import LoadingOverlay from './components/common/LoadingOverlay.vue';
import Toast from './components/common/Toast.vue';
import DashboardPage from './pages/DashboardPage.vue';
import PredictionsPage from './pages/PredictionsPage.vue';
import TradesPage from './pages/TradesPage.vue';
import JobsPage from './pages/JobsPage.vue';
import SettingsPage from './pages/SettingsPage.vue';

export default {
  name: 'App',
  components: {
    LoadingOverlay,
    Toast,
    DashboardPage,
    PredictionsPage,
    TradesPage,
    JobsPage,
    SettingsPage
  },

  data() {
    return {
      // Navigation
      activeTab: 'dashboard',
      tabs: [
        {
          id: 'dashboard',
          label: 'Dashboard',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9"></rect><rect x="14" y="3" width="7" height="5"></rect><rect x="14" y="12" width="7" height="9"></rect><rect x="3" y="16" width="7" height="5"></rect></svg>'
        },
        {
          id: 'predictions',
          label: 'Prognosen',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path></svg>'
        },
        {
          id: 'trades',
          label: 'Trades',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>'
        },
        {
          id: 'jobs',
          label: 'Jobs',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>'
        },
        {
          id: 'settings',
          label: 'Einstellungen',
          icon: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>'
        }
      ],

      // App state
      isActive: false,
      stats: {},
      jobs: [],
      openTrades: [],
      closedTrades: [],
      latestPrediction: null,
      performanceData: Array(30).fill(0).map(() => Math.random() * 4 - 1),

      // Forms
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

      // UI state
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

      globalMessage: null,
      updateTimer: null
    };
  },

  computed: {
    isLoading() {
      return Object.values(this.loading).some(status => status === true && status !== null);
    }
  },

  created() {
    this.loadData();
    this.updateTimer = setInterval(this.loadData, 30000);
  },

  beforeUnmount() {
    if (this.updateTimer) {
      clearInterval(this.updateTimer);
    }
  },

  methods: {
    // Data loading methods
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

    // Action methods
    async makePrediction(predictionData) {
      this.loading.prediction = true;
      this.errors.prediction = null;

      try {
        const response = await axios.post('/api/predict', predictionData);
        this.latestPrediction = response.data;
        return response.data;
      } catch (error) {
        const errorMsg = `Fehler bei der Prognose: ${this.getErrorMessage(error)}`;
        this.errors.prediction = errorMsg;
        console.error('Fehler bei der Prognose:', error);
        throw new Error(errorMsg);
      } finally {
        this.loading.prediction = false;
      }
    },

    async executeTrade(symbol, action) {
      this.loading.trade = true;
      this.globalMessage = null;

      try {
        const response = await axios.post('/api/trade', {
          symbol,
          action
        });

        if (response.data.success) {
          this.setSuccessMessage(`Trade erfolgreich ausgeführt: ${action.toUpperCase()} ${symbol}`);
          this.loadTrades();
          return response.data;
        } else {
          const errorMsg = `Fehler beim Ausführen des Trades: ${response.data.reason || 'Unbekannter Fehler'}`;
          this.setErrorMessage(errorMsg);
          throw new Error(errorMsg);
        }
      } catch (error) {
        const errorMsg = `Fehler beim Ausführen des Trades: ${this.getErrorMessage(error)}`;
        this.setErrorMessage(errorMsg);
        console.error('Fehler beim Ausführen des Trades:', error);
        throw new Error(errorMsg);
      } finally {
        this.loading.trade = false;
      }
    },

    async addJob(jobData) {
      this.loading.addJob = true;
      this.errors.jobs = null;

      try {
        const response = await axios.post('/api/jobs', jobData);

        if (response.data.job_id) {
          this.setSuccessMessage(`Job erfolgreich hinzugefügt: ${response.data.job_id}`);
          this.loadJobs();
          return response.data;
        } else {
          throw new Error('Fehler beim Hinzufügen des Jobs');
        }
      } catch (error) {
        const errorMsg = `Fehler beim Hinzufügen des Jobs: ${this.getErrorMessage(error)}`;
        this.errors.jobs = errorMsg;
        console.error('Fehler beim Hinzufügen des Jobs:', error);
        throw new Error(errorMsg);
      } finally {
        this.loading.addJob = false;
      }
    },

    async removeJob(jobId) {
      if (!confirm(`Sind Sie sicher, dass Sie den Job ${jobId} löschen möchten?`)) {
        return;
      }

      this.loading.removeJob = jobId;
      this.errors.jobs = null;

      try {
        const response = await axios.delete(`/api/jobs/${jobId}`);

        if (response.data.message) {
          this.setSuccessMessage(response.data.message);
          this.loadJobs();
          return response.data;
        } else {
          throw new Error('Fehler beim Löschen des Jobs');
        }
      } catch (error) {
        const errorMsg = `Fehler beim Löschen des Jobs: ${this.getErrorMessage(error)}`;
        this.errors.jobs = errorMsg;
        console.error('Fehler beim Löschen des Jobs:', error);
        throw new Error(errorMsg);
      } finally {
        this.loading.removeJob = null;
      }
    },

    async saveSettings(settingsData) {
      this.loading.settings = true;
      this.errors.settings = null;

      try {
        // Sicherstellen, dass risk_management existiert
        if (!settingsData.trader.risk_management) {
          settingsData.trader.risk_management = {
            max_risk_per_trade: 2.0,
            daily_drawdown_limit: 5.0
          };
        }

        // Trader-Einstellungen speichern
        await axios.post('/api/config', {
          section: 'trader',
          config: settingsData.trader
        });

        // Modell-Einstellungen speichern
        await axios.post('/api/config', {
          section: 'model',
          config: settingsData.model
        });

        this.settings = settingsData;
        this.setSuccessMessage('Einstellungen erfolgreich gespeichert');
      } catch (error) {
        const errorMsg = `Fehler beim Speichern der Einstellungen: ${this.getErrorMessage(error)}`;
        this.errors.settings = errorMsg;
        console.error('Fehler beim Speichern der Einstellungen:', error);
        throw new Error(errorMsg);
      } finally {
        this.loading.settings = false;
      }
    },

    // Utility methods
    setSuccessMessage(text) {
      this.globalMessage = { text, type: 'success' };
      setTimeout(() => {
        if (this.globalMessage && this.globalMessage.text === text) {
          this.globalMessage = null;
        }
      }, 5000);
    },

    setErrorMessage(text) {
      this.globalMessage = { text, type: 'error' };
    },

    dismissMessage() {
      this.globalMessage = null;
    },

    getErrorMessage(error) {
      if (error.response) {
        if (error.response.data && error.response.data.detail) {
          return error.response.data.detail;
        }
        return `${error.response.status} ${error.response.statusText}`;
      } else if (error.request) {
        return 'Keine Antwort vom Server erhalten. Bitte überprüfen Sie Ihre Internetverbindung.';
      } else {
        return error.message || 'Unbekannter Fehler';
      }
    }
  }
};
</script>

<style>
:root {
  --color-primary: #6366f1; /* Indigo 500 */
  --color-primary-foreground: white;
  --color-primary-hover: #4f46e5; /* Indigo 600 */
  --color-secondary: #f9fafb; /* Gray 50 */
  --color-secondary-foreground: #111827; /* Gray 900 */
  --color-secondary-hover: #f3f4f6; /* Gray 100 */
  --color-positive: #22c55e; /* Green 500 */
  --color-negative: #ef4444; /* Red 500 */
  --color-background: #ffffff;
  --color-foreground: #111827; /* Gray 900 */
  --color-muted: #6b7280; /* Gray 500 */
  --color-muted-foreground: #374151; /* Gray 700 */
  --color-border: #e5e7eb; /* Gray 200 */
  --color-input: #f9fafb; /* Gray 50 */
  --color-ring: rgba(99, 102, 241, 0.5); /* Indigo 500 with opacity */

  --radius: 0.5rem;
  --header-height: 64px;
  --sidebar-width: 220px;
}

.dark {
  --color-primary: #6366f1; /* Indigo 500 */
  --color-primary-foreground: white;
  --color-primary-hover: #818cf8; /* Indigo 400 */
  --color-secondary: #1f2937; /* Gray 800 */
  --color-secondary-foreground: #f9fafb; /* Gray 50 */
  --color-secondary-hover: #374151; /* Gray 700 */
  --color-positive: #22c55e; /* Green 500 */
  --color-negative: #ef4444; /* Red 500 */
  --color-background: #111827; /* Gray 900 */
  --color-foreground: #f9fafb; /* Gray 50 */
  --color-muted: #9ca3af; /* Gray 400 */
  --color-muted-foreground: #d1d5db; /* Gray 300 */
  --color-border: #374151; /* Gray 700 */
  --color-input: #1f2937; /* Gray 800 */
  --color-ring: rgba(99, 102, 241, 0.5); /* Indigo 500 with opacity */
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  line-height: 1.5;
  color: var(--color-foreground);
  background-color: var(--color-background);
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  height: var(--header-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  border-bottom: 1px solid var(--color-border);
  background-color: var(--color-background);
  position: sticky;
  top: 0;
  z-index: 20;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-foreground);
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  background-color: var(--color-secondary);
  color: var(--color-muted-foreground);
}

.status-badge.active {
  background-color: var(--color-positive);
  color: white;
}

.app-content {
  display: flex;
  flex: 1;
}

.app-sidebar {
  width: var(--sidebar-width);
  border-right: 1px solid var(--color-border);
  background-color: var(--color-background);
  overflow-y: auto;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  gap: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  gap: 0.75rem;
  border-radius: var(--radius);
  border: none;
  background-color: transparent;
  color: var(--color-muted-foreground);
  font-size: 0.875rem;
  font-weight: 500;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background-color: var(--color-secondary);
  color: var(--color-foreground);
}

.nav-item.active {
  background-color: var(--color-primary);
  color: var(--color-primary-foreground);
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon svg {
  width: 18px;
  height: 18px;
}

.page-container {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}

/* Reusable utility classes */
.card {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.positive {
  color: var(--color-positive);
}

.negative {
  color: var(--color-negative);
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius);
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1.5;
  transition: all 0.2s ease;
  cursor: pointer;
  border: 1px solid transparent;
}

.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-primary-foreground);
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
}

.btn-secondary {
  background-color: var(--color-secondary);
  color: var(--color-secondary-foreground);
}

.btn-secondary:hover:not(:disabled) {
  background-color: var(--color-secondary-hover);
}

.btn-danger {
  background-color: var(--color-negative);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  opacity: 0.9;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input {
  display: block;
  width: 100%;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius);
  border: 1px solid var(--color-border);
  background-color: var(--color-input);
  color: var(--color-foreground);
  font-size: 0.875rem;
  line-height: 1.5;
}

.input:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-ring);
}

.label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: var(--color-foreground);
}

.form-group {
  margin-bottom: 1rem;
}
</style>