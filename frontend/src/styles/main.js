import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

// Import styles
import './styles/main.css'

// Globale Axios-Konfiguration
axios.defaults.baseURL = ''; // Leerer String, kein Präfix
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Axios-Interceptors für globale Fehlerbehandlung
axios.interceptors.request.use(config => {
  // Verhindere doppelte /api/ Präfixe in der URL
  if (config.url && config.url.startsWith('/api/')) {
    config.url = config.url; // Unverändert lassen
  } else if (config.url && !config.url.startsWith('/')) {
    config.url = `/${config.url}`; // Füge führenden Slash hinzu, wenn er fehlt
  }
  return config;
});

axios.interceptors.response.use(
  response => response,
  error => {
    // Globale Fehlerbehandlung hier
    console.error('API-Fehler:', error);
    return Promise.reject(error);
  }
);

// App erstellen und mounten
const app = createApp(App);

// Globalen Fehler-Handler hinzufügen
app.config.errorHandler = (err, vm, info) => {
  console.error('Unbehandelte App-Fehler:', err, info);
};

app.mount('#app');