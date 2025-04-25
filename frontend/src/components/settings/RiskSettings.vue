<template>
  <Card title="Risikomanagement" class="settings-section">
    <div class="form-group">
      <label for="stop-loss" class="label">Stop-Loss (%)</label>
      <input
        type="number"
        id="stop-loss"
        v-model.number="localSettings.stop_loss_pct"
        min="0.1"
        max="10"
        step="0.1"
        class="input"
        @change="emitChanges"
      >
    </div>

    <div class="form-group">
      <label for="take-profit" class="label">Take-Profit (%)</label>
      <input
        type="number"
        id="take-profit"
        v-model.number="localSettings.take_profit_pct"
        min="0.1"
        max="20"
        step="0.1"
        class="input"
        @change="emitChanges"
      >
    </div>

    <div class="form-group">
      <label for="max-risk" class="label">Maximales Risiko pro Trade (%)</label>
      <input
        type="number"
        id="max-risk"
        v-model.number="localRiskSettings.max_risk_per_trade"
        min="0.1"
        max="10"
        step="0.1"
        class="input"
        @change="emitRiskChanges"
      >
    </div>

    <div class="form-group">
      <label for="daily-drawdown" class="label">Tägliches Drawdown Limit (%)</label>
      <input
        type="number"
        id="daily-drawdown"
        v-model.number="localRiskSettings.daily_drawdown_limit"
        min="0.1"
        max="20"
        step="0.1"
        class="input"
        @change="emitRiskChanges"
      >
    </div>
  </Card>
</template>

<script>
import Card from '../common/Card.vue';

export default {
  name: 'RiskSettings',
  components: {
    Card
  },
  props: {
    settings: {
      type: Object,
      required: true
    },
    riskSettings: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localSettings: {
        stop_loss_pct: 2.0,
        take_profit_pct: 3.0
      },
      localRiskSettings: {
        max_risk_per_trade: 2.0,
        daily_drawdown_limit: 5.0
      }
    };
  },
  methods: {
    emitChanges() {
      this.$emit('change', { ...this.localSettings });
    },

    emitRiskChanges() {
      this.$emit('change-risk', { ...this.localRiskSettings });
    },

    updateFromProps() {
      this.localSettings = {
        stop_loss_pct: this.settings.stop_loss_pct ?? 2.0,
        take_profit_pct: this.settings.take_profit_pct ?? 3.0
      };

      this.localRiskSettings = {
        max_risk_per_trade: this.riskSettings.max_risk_per_trade ?? 2.0,
        daily_drawdown_limit: this.riskSettings.daily_drawdown_limit ?? 5.0
      };
    }
  },
  watch: {
    settings: {
      handler() {
        this.updateFromProps();
      },
      deep: true,
      immediate: true
    },
    riskSettings: {
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