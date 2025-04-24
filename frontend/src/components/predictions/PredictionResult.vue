<template>
  <Card title="Letzte Prognose" v-if="prediction" class="prediction-result">
    <div class="prediction-header">
      <div class="prediction-symbol">{{ prediction.symbol }}</div>
      <div class="prediction-time">{{ formatTime(prediction.timestamp) }}</div>
    </div>

    <div class="prediction-details">
      <div class="prediction-row">
        <div class="prediction-label">Aktueller Preis:</div>
        <div class="prediction-value">{{ prediction.current.toFixed(2) }}</div>
      </div>

      <div class="prediction-row">
        <div class="prediction-label">Prognostizierter Preis:</div>
        <div class="prediction-value">{{ prediction.prediction.toFixed(2) }}</div>
      </div>

      <div class="prediction-row">
        <div class="prediction-label">Richtung:</div>
        <div
          class="prediction-value"
          :class="{
            'positive': prediction.direction === 'up',
            'negative': prediction.direction === 'down'
          }"
        >
          {{ prediction.direction === 'up' ? '↑ Aufwärts' : '↓ Abwärts' }}
        </div>
      </div>

      <div class="prediction-row">
        <div class="prediction-label">Änderung:</div>
        <div
          class="prediction-value"
          :class="{
            'positive': prediction.change_pct > 0,
            'negative': prediction.change_pct < 0
          }"
        >
          {{ prediction.change_pct.toFixed(2) }}%
        </div>
      </div>

      <div class="prediction-row">
        <div class="prediction-label">Vertrauen:</div>
        <div class="prediction-value">{{ (prediction.confidence * 100).toFixed(2) }}%</div>
      </div>
    </div>

    <template #footer>
      <div class="prediction-actions">
        <Button
          @click="$emit('execute-trade', prediction.symbol, prediction.direction === 'up' ? 'buy' : 'sell')"
          :variant="prediction.direction === 'up' ? 'primary' : 'danger'"
          :loading="loading"
          :text="loading ? 'Wird ausgeführt...' : (prediction.direction === 'up' ? 'Kaufen' : 'Verkaufen')"
        />
      </div>
    </template>
  </Card>
</template>

<script>
import Card from '../common/Card.vue';
import Button from '../common/Button.vue';

export default {
  name: 'PredictionResult',
  components: {
    Card,
    Button
  },
  props: {
    prediction: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    formatTime(timestamp) {
      if (!timestamp) return '';

      const date = new Date(timestamp);
      return date.toLocaleString();
    }
  }
}
</script>

<style scoped>
.prediction-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--color-border);
}

.prediction-symbol {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-foreground);
}

.prediction-time {
  font-size: 0.875rem;
  color: var(--color-muted);
}

.prediction-details {
  margin-bottom: 1.5rem;
}

.prediction-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--color-border);
}

.prediction-row:last-child {
  border-bottom: none;
}

.prediction-label {
  font-weight: 500;
  color: var(--color-muted-foreground);
}

.prediction-value {
  font-weight: 600;
}

.prediction-value.positive {
  color: var(--color-positive);
}

.prediction-value.negative {
  color: var(--color-negative);
}

.prediction-actions {
  display: flex;
  justify-content: flex-end;
}
</style>