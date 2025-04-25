import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

import './styles/main.css'

axios.defaults.baseURL = '';
axios.defaults.headers.common['Content-Type'] = 'application/json';

axios.interceptors.request.use(config => {
  if (config.url && config.url.startsWith('/api/')) {
    config.url = config.url;
  } else if (config.url && !config.url.startsWith('/')) {
    config.url = `/${config.url}`;
  }
  return config;
});

axios.interceptors.response.use(
  response => response,
  error => {
    console.error('API-Fehler:', error);
    return Promise.reject(error);
  }
);

const app = createApp(App);

app.config.errorHandler = (err, vm, info) => {
  console.error('Unbehandelte App-Fehler:', err, info);
};

app.mount('#app');