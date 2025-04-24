import axios from 'axios';

// API-Endpunkte
const API = {
  // Status & Stats
  STATUS: '/api/status',
  STATS: '/api/stats',

  // Jobs
  JOBS: '/api/jobs',

  // Trades
  TRADES: '/api/trades',
  TRADE: '/api/trade',

  // Predictions
  PREDICT: '/api/predict',

  // Settings/Config
  CONFIG: '/api/config'
};

// API-Service
const apiService = {
  // Status & Stats
  getStatus() {
    return axios.get(API.STATUS);
  },

  getStats() {
    return axios.get(API.STATS);
  },

  // Jobs
  getJobs() {
    return axios.get(API.JOBS);
  },

  addJob(jobData) {
    return axios.post(API.JOBS, jobData);
  },

  removeJob(jobId) {
    return axios.delete(`${API.JOBS}/${jobId}`);
  },

  // Trades
  getTrades(status = 'all') {
    return axios.get(`${API.TRADES}?status=${status}`);
  },

  executeTrade(symbol, action) {
    return axios.post(API.TRADE, { symbol, action });
  },

  // Predictions
  makePrediction(predictionData) {
    return axios.post(API.PREDICT, predictionData);
  },

  // Settings/Config
  getConfig() {
    return axios.get(API.CONFIG);
  },

  saveConfig(section, config) {
    return axios.post(API.CONFIG, { section, config });
  },

  // Helper Methoden
  formatError(error) {
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
};

export default apiService;