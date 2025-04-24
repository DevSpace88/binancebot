<template>
  <div class="settings-page">
    <h1 class="page-title">Einstellungen</h1>

    <GeneralSettings
      :settings="traderSettings"
      @change="updateTraderSettings"
    />

    <RiskSettings
      :settings="traderSettings"
      :risk-settings="riskManagement"
      @change="updateTraderSettings"
      @change-risk="updateRiskSettings"
    />

    <ModelSettings
      :model-settings="modelSettings"
      :confidence-settings="traderSettings"
      @change-model="updateModelSettings"
      @change-confidence="updateTraderSettings"
    />

    <ModelTraining
      @model-trained="onModelTrained"
    />

    <ApiKeySettings
      :api-settings="exchangeSettings"
      @change-api="updateExchangeSettings"
    />

    <div class="settings-actions">
      <Button
        @click="saveSettings"
        variant="primary"
        :loading="loading"
        :disabled="loading"
        text="Einstellungen speichern"
      />
    </div>
  </div>
</template>

<script>
import Button from '../components/common/Button.vue';
import GeneralSettings from '../components/settings/GeneralSettings.vue';
import RiskSettings from '../components/settings/RiskSettings.vue';
import ModelSettings from '../components/settings/ModelSettings.vue';
import ModelTraining from '../components/settings/ModelTraining.vue';
import ApiKeySettings from '../components/settings/ApiKeySettings.vue';

export default {
  name: 'SettingsPage',
  components: {
    Button,
    GeneralSettings,
    RiskSettings,
    ModelSettings,
    ModelTraining,
    ApiKeySettings
  },
  props: {
    settings: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      loading: false,
      traderSettings: { ...this.settings.trader },
      modelSettings: { ...this.settings.model },
      riskManagement: { ...(this.settings.trader.risk_management || {
        max_risk_per_trade: 2.0,
        daily_drawdown_limit: 5.0
      })},
      exchangeSettings: { ...(this.settings.trader.exchanges?.binance || {
        api_key: '',
        api_secret: '',
        test_mode: true
      })}
    };
  },
  methods: {
    updateTraderSettings(newSettings) {
      // Tiefe Kopie erstellen, damit Vue die Änderung als neu erkennt
      this.traderSettings = { ...this.traderSettings, ...newSettings };
    },

    updateModelSettings(newSettings) {
      this.modelSettings = { ...this.modelSettings, ...newSettings };
    },

    updateRiskSettings(newSettings) {
      this.riskManagement = { ...this.riskManagement, ...newSettings };
    },

    updateExchangeSettings(newSettings) {
      this.exchangeSettings = { ...this.exchangeSettings, ...newSettings };
    },

    onModelTrained(result) {
      // Modell wurde trainiert - optional könnten wir hier die aktualisierten Modelleinstellungen laden
      this.$emit('success', `Modell erfolgreich für ${result.symbol} trainiert`);
    },

    async saveSettings() {
      try {
        this.loading = true;

        // Strukturieren der Einstellungen in das Format der API
        const completeSettings = {
          trader: {
            ...this.traderSettings,
            risk_management: this.riskManagement,
            exchanges: {
              binance: this.exchangeSettings
            }
          },
          model: this.modelSettings
        };

        // Event emittieren, damit die App die Einstellungen speichern kann
        this.$emit('save-settings', completeSettings);
      } catch (error) {
        this.$emit('error', error.message || 'Fehler beim Speichern der Einstellungen');
      } finally {
        this.loading = false;
      }
    }
  },
  watch: {
    settings: {
      handler(newSettings) {
        // Hier wurde eine direkte Zuweisung verwendet, was die Rekursion unterbrechen sollte
        this.traderSettings = JSON.parse(JSON.stringify(newSettings.trader || {}));
        this.modelSettings = JSON.parse(JSON.stringify(newSettings.model || {}));
        this.riskManagement = JSON.parse(JSON.stringify(newSettings.trader?.risk_management || {
          max_risk_per_trade: 2.0,
          daily_drawdown_limit: 5.0
        }));
        this.exchangeSettings = JSON.parse(JSON.stringify(newSettings.trader?.exchanges?.binance || {
          api_key: '',
          api_secret: '',
          test_mode: true
        }));
      },
      deep: true,
      immediate: true
    }
  }
}
</script>

<style scoped>
.settings-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-foreground);
}

.settings-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
  margin-bottom: 3rem;
}
</style>