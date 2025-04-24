<template>
  <Card title="Modelleinstellungen" class="settings-section">
    <div class="form-group">
      <label for="model-type" class="label">Modelltyp</label>
      <select id="model-type" v-model="localSettings.model_type" class="input" @change="emitModelChanges">
        <option value="random_forest">Random Forest</option>
        <option value="gradient_boosting">Gradient Boosting</option>
        <option value="linear">Linear</option>
      </select>
    </div>

    <div class="form-group">
      <label for="prediction-horizon" class="label">Prognosehorizont (Stunden)</label>
      <input
        type="number"
        id="prediction-horizon"
        v-model.number="localSettings.prediction_horizon"
        min="1"
        max="24"
        class="input"
        @change="emitModelChanges"
      >
    </div>

    <div class="form-group">
      <label for="confidence-threshold" class="label">Vertrauensschwelle</label>
      <input
        type="number"
        id="confidence-threshold"
        v-model.number="localConfidenceSettings.confidence_threshold"
        min="0.1"
        max="1"
        step="0.05"
        class="input"
        @change="emitConfidenceChanges"
      >
    </div>

    <div class="form-group">
      <label for="min-change" class="label">Minimale Änderung für Trade (%)</label>
      <input
        type="number"
        id="min-change"
        v-model.number="localConfidenceSettings.min_change_pct"
        min="0.1"
        max="5"
        step="0.1"
        class="input"
        @change="emitConfidenceChanges"
      >
    </div>
  </Card>
</template>

<script>
import Card from '../common/Card.vue';

export default {
  name: 'ModelSettings',
  components: {
    Card
  },
  props: {
    modelSettings: {
      type: Object,
      required: true
    },
    confidenceSettings: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localSettings: {
        model_type: 'random_forest',
        prediction_horizon: 1
      },
      localConfidenceSettings: {
        confidence_threshold: 0.7,
        min_change_pct: 1.0
      }
    };
  },
  methods: {
    // Änderungen an Parent weitergeben
    emitModelChanges() {
      this.$emit('change-model', { ...this.localSettings });
    },

    emitConfidenceChanges() {
      this.$emit('change-confidence', { ...this.localConfidenceSettings });
    },

    // Lokale Einstellungen aus Props aktualisieren
    updateFromProps() {
      this.localSettings = {
        model_type: this.modelSettings.model_type ?? 'random_forest',
        prediction_horizon: this.modelSettings.prediction_horizon ?? 1
      };

      this.localConfidenceSettings = {
        confidence_threshold: this.confidenceSettings.confidence_threshold ?? 0.7,
        min_change_pct: this.confidenceSettings.min_change_pct ?? 1.0
      };
    }
  },
  watch: {
    modelSettings: {
      handler() {
        this.updateFromProps();
      },
      deep: true,
      immediate: true
    },
    confidenceSettings: {
      handler() {
        this.updateFromProps();
      },
      deep: true,
      immediate: true
    }
  },
  created() {
    this.updateFromProps();
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
</style>