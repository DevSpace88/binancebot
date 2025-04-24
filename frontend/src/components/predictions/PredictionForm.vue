<template>
  <Card title="Neue Prognose" class="prediction-form">
    <div class="form-group">
      <label for="prediction-symbol" class="label">Symbol</label>
      <input
        type="text"
        id="prediction-symbol"
        v-model="form.symbol"
        placeholder="z.B. BTC-USDT"
        class="input"
      />
      <div v-if="error.symbol" class="error-message">{{ error.symbol }}</div>
    </div>

    <div class="form-group">
      <label for="prediction-timeframe" class="label">Zeitrahmen</label>
      <select id="prediction-timeframe" v-model="form.timeframe" class="input">
        <option value="1h">1 Stunde</option>
        <option value="4h">4 Stunden</option>
        <option value="1d">1 Tag</option>
      </select>
    </div>

    <Button
      @click="makePrediction"
      :loading="loading"
      :disabled="loading || !form.symbol"
      :text="loading ? 'Wird berechnet...' : 'Prognose erstellen'"
      variant="primary"
      class="w-full"
    />
  </Card>
</template>

<script>
import Card from '../common/Card.vue';
import Button from '../common/Button.vue';

export default {
  name: 'PredictionForm',
  components: {
    Card,
    Button
  },
  props: {
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      form: {
        symbol: 'BTC-USDT',
        timeframe: '1h'
      },
      error: {
        symbol: null
      }
    };
  },
  methods: {
    validate() {
      this.error.symbol = null;

      if (!this.form.symbol || this.form.symbol.trim() === '') {
        this.error.symbol = 'Bitte geben Sie ein Symbol ein';
        return false;
      }

      return true;
    },
    makePrediction() {
      if (this.validate()) {
        this.$emit('make-prediction', { ...this.form });
      }
    }
  }
}
</script>

<style scoped>
.prediction-form {
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

.w-full {
  width: 100%;
}
</style>