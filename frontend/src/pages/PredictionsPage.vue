<template>
  <div class="predictions-page">
    <h1 class="page-title">Prognosen</h1>

    <PredictionForm
      :loading="loading.prediction"
      @make-prediction="makePrediction"
    />

    <PredictionResult
      :prediction="latestPrediction"
      :loading="loading.trade"
      @execute-trade="executeTrade"
    />

    <Card title="Prognosehistorie" class="prediction-history">
      <div v-if="predictionHistory.length === 0" class="empty-state">
        Noch keine Prognosehistorie verfügbar
      </div>
      <div v-else class="prediction-history-list">
        <!-- Hier könnte die Historie angezeigt werden, wenn verfügbar -->
      </div>
    </Card>
  </div>
</template>

<script>
import Card from '../components/common/Card.vue';
import PredictionForm from '../components/predictions/PredictionForm.vue';
import PredictionResult from '../components/predictions/PredictionResult.vue';

export default {
  name: 'PredictionsPage',
  components: {
    Card,
    PredictionForm,
    PredictionResult
  },
  props: {
    latestPrediction: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      predictionHistory: [],
      loading: {
        prediction: false,
        trade: false
      }
    };
  },
  methods: {
    async makePrediction(formData) {
      try {
        this.loading.prediction = true;
        // Emit the event up to parent to handle API call
        this.$emit('make-prediction', formData);
      } catch (error) {
        this.$emit('error', error.message || 'Fehler bei der Prognose');
      } finally {
        this.loading.prediction = false;
      }
    },
    async executeTrade(symbol, action) {
      try {
        this.loading.trade = true;
        // Emit the event up to parent to handle API call
        this.$emit('execute-trade', symbol, action);
      } catch (error) {
        this.$emit('error', error.message || 'Fehler beim Ausführen des Trades');
      } finally {
        this.loading.trade = false;
      }
    }
  }
}
</script>

<style scoped>
.predictions-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-foreground);
}

.prediction-history {
  margin-top: 1.5rem;
}

.empty-state {
  padding: 2rem;
  text-align: center;
  color: var(--color-muted);
  background-color: var(--color-secondary);
  border-radius: var(--radius);
}
</style>