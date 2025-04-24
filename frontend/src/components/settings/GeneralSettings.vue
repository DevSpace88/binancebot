<template>
  <Card title="Allgemeine Einstellungen" class="settings-section">
    <div class="form-group">
      <div class="flex-space-between">
        <label for="trading-enabled" class="label">Trading aktivieren</label>
        <div class="toggle-switch">
          <input type="checkbox" id="trading-enabled" v-model="localSettings.trading_enabled" @change="emitChanges">
          <label for="trading-enabled"></label>
        </div>
      </div>
    </div>

    <div class="form-group">
      <label for="max-trades-day" class="label">Maximale Trades pro Tag</label>
      <input
        type="number"
        id="max-trades-day"
        v-model.number="localSettings.max_trades_per_day"
        min="1"
        max="50"
        class="input"
        @change="emitChanges"
      >
    </div>

    <div class="form-group">
      <label for="trade-amount" class="label">Betrag pro Trade</label>
      <input
        type="number"
        id="trade-amount"
        v-model.number="localSettings.trade_amount"
        min="1"
        class="input"
        @change="emitChanges"
      >
    </div>
  </Card>
</template>

<script>
import Card from '../common/Card.vue';

export default {
  name: 'GeneralSettings',
  components: {
    Card
  },
  props: {
    settings: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localSettings: {
        trading_enabled: false,
        max_trades_per_day: 5,
        trade_amount: 100
      }
    };
  },
  methods: {
    // Änderungen an Parent weitergeben
    emitChanges() {
      this.$emit('change', { ...this.localSettings });
    },

    // Lokale Einstellungen aus Props aktualisieren
    updateFromProps() {
      this.localSettings = {
        trading_enabled: this.settings.trading_enabled ?? false,
        max_trades_per_day: this.settings.max_trades_per_day ?? 5,
        trade_amount: this.settings.trade_amount ?? 100
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

.flex-space-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-switch label {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--color-muted);
  transition: .4s;
  border-radius: 34px;
}

.toggle-switch label:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

.toggle-switch input:checked + label {
  background-color: var(--color-primary);
}

.toggle-switch input:checked + label:before {
  transform: translateX(26px);
}
</style>