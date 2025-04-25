<template>
  <Card title="Modell-Training" class="settings-section">
    <div class="form-group">
      <label for="training-symbol" class="label">Symbol für Training</label>
      <input
        type="text"
        id="training-symbol"
        v-model="trainingSymbol"
        placeholder="z.B. BTC-USDT"
        class="input"
      >
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>

    <div class="form-group">
      <label for="data-points" class="label">Datenpunkte (ca. Stunden)</label>
      <select id="data-points" v-model="dataPoints" class="input">
        <option value="1000">~1000 Stunden (ca. 6 Wochen)</option>
        <option value="2000">~2000 Stunden (ca. 3 Monate)</option>
        <option value="5000">~5000 Stunden (ca. 7 Monate)</option>
      </select>
    </div>

    <Button
      @click="trainModel"
      :loading="loading"
      :disabled="loading || !trainingSymbol"
      text="Modell trainieren"
      variant="primary"
      class="w-full"
    />

    <div v-if="trainingResult" class="training-result">
      <div class="mt-4">
        <strong>Training abgeschlossen:</strong>
        <p>{{ trainingResult }}</p>
      </div>
    </div>
  </Card>
</template>

<script>
import Card from '../common/Card.vue';
import Button from '../common/Button.vue';
import axios from 'axios';

export default {
  name: 'ModelTraining',
  components: {
    Card,
    Button
  },
  data() {
    return {
      trainingSymbol: 'BTC-USDT',
      dataPoints: '2000',
      loading: false,
      error: null,
      trainingResult: null
    };
  },
  methods: {
    async trainModel() {
  this.error = null;
  this.trainingResult = null;

  if (!this.trainingSymbol || this.trainingSymbol.trim() === '') {
    this.error = 'Bitte geben Sie ein Symbol ein';
    return;
  }

  try {
    this.loading = true;
    console.log(`Training für Symbol: ${this.trainingSymbol}, Datenpunkte: ${this.dataPoints}`);

    const response = await axios.post('/api/train', {
      symbol: this.trainingSymbol,
      data_points: parseInt(this.dataPoints)
    });

    console.log("Erfolgreiche Antwort:", response.data);
    this.trainingResult = response.data.message || 'Modell erfolgreich trainiert';
    this.$emit('model-trained', {
      symbol: this.trainingSymbol,
      result: this.trainingResult
    });

  } catch (error) {
    console.log("Vollständige Fehlerantwort:", error.response?.data);

    if (error.response && error.response.data) {
      if (error.response.data.detail) {
        this.error = error.response.data.detail;
      } else if (typeof error.response.data === 'string') {
        this.error = error.response.data;
      } else {
        this.error = `Serverfehler: ${error.response.status}`;
      }
    } else if (error.request) {
      this.error = 'Keine Antwort vom Server. Bitte überprüfe deine Internetverbindung.';
    } else {
      this.error = `Fehler beim Training des Modells: ${error.message}`;
    }
    console.error('Fehler beim Training des Modells:', error);
  } finally {
    this.loading = false;
  }
}
  }
}
</script>

<style scoped>
.settings-section {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.error-message {
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: var(--color-negative);
}

.training-result {
  margin-top: 1rem;
  padding: 1rem;
  background-color: var(--color-secondary);
  border-radius: var(--radius);
  border-left: 4px solid var(--color-positive);
}

.w-full {
  width: 100%;
}

.mt-4 {
  margin-top: 1rem;
}
</style>