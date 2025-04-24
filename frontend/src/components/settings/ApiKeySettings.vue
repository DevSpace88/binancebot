<template>
  <Card title="API-Schlüssel" class="settings-section">
    <div class="form-group">
      <label for="binance-api-key" class="label">Binance API-Schlüssel</label>
      <input
        type="password"
        id="binance-api-key"
        v-model="localSettings.api_key"
        class="input"
        @change="emitChanges"
      >
    </div>

    <div class="form-group">
      <label for="binance-api-secret" class="label">Binance API-Secret</label>
      <input
        type="password"
        id="binance-api-secret"
        v-model="localSettings.api_secret"
        class="input"
        @change="emitChanges"
      >
    </div>

    <div class="form-group">
      <div class="flex-space-between">
        <label for="binance-test-mode" class="label">Testmodus</label>
        <div class="toggle-switch">
          <input type="checkbox" id="binance-test-mode" v-model="localSettings.test_mode" @change="emitChanges">
          <label for="binance-test-mode"></label>
        </div>
      </div>
    </div>
  </Card>
</template>

<script>
import Card from '../common/Card.vue';

export default {
  name: 'ApiKeySettings',
  components: {
    Card
  },
  props: {
    apiSettings: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localSettings: {
        api_key: '',
        api_secret: '',
        test_mode: true
      }
    };
  },
  methods: {
    // Änderungen an Parent weitergeben
    emitChanges() {
      this.$emit('change-api', { ...this.localSettings });
    },

    // Lokale Einstellungen aus Props aktualisieren
    updateFromProps() {
      this.localSettings = {
        api_key: this.apiSettings.api_key || '',
        api_secret: this.apiSettings.api_secret || '',
        test_mode: this.apiSettings.test_mode ?? true
      };
    }
  },
  watch: {
    apiSettings: {
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