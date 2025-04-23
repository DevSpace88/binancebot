import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

// Globale Axios-Konfiguration
axios.defaults.baseURL = process.env.VUE_APP_API_URL || '';
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Axios-Interceptors für globale Fehlerbehandlung
axios.interceptors.response.use(
  response => response,
  error => {
    // Hier könnten globale Fehler wie 401 (Unauthorized) abgefangen werden
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