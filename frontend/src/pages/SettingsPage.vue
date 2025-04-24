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

    <NewsApiSettings
      :news-settings="newsApiSettings"
      @change-news-api="updateNewsApiSettings"
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
import NewsApiSettings from '../components/settings/NewsApiSettings.vue';
import ApiKeySettings from '../components/settings/ApiKeySettings.vue';

export default {
  name: 'SettingsPage',
  components: {
    Button,
    GeneralSettings,
    RiskSettings,
    ModelSettings,
    ModelTraining,
    NewsApiSettings,
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
      })},
      newsApiSettings: {
        news_api_key: this.settings.api_keys?.news_api || '',
        sentiment_enabled: this.settings.model?.features?.includes('sentiment') || false
      }
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

    updateNewsApiSettings(newSettings) {
      this.newsApiSettings = { ...this.newsApiSettings, ...newSettings };

      // Wenn sentiment_enabled geändert wurde, auch die Modell-Features aktualisieren
      if (this.newsApiSettings.sentiment_enabled) {
        // Stellen sicher, dass 'sentiment' in den Features ist
        if (!this.modelSettings.features.includes('sentiment')) {
          this.modelSettings.features = [...this.modelSettings.features, 'sentiment'];
        }
      } else {
        // 'sentiment' aus Features entfernen, wenn es deaktiviert wurde
        if (this.modelSettings.features.includes('sentiment')) {
          this.modelSettings.features = this.modelSettings.features.filter(
            feature => feature !== 'sentiment'
          );
        }
      }
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
          model: this.modelSettings,
          api_keys: {
            news_api: this.newsApiSettings.news_api_key
          }
        };

        // Zuerst Modell-Konfiguration aktualisieren
        await this.updateModelConfig();

        // Dann Trader-Konfiguration aktualisieren
        await this.updateTraderConfig();

        // Dann API-Keys aktualisieren
        await this.updateApiKeysConfig();

        // Event emittieren, damit die App weiß, dass die Einstellungen gespeichert wurden
        this.$emit('save-settings', completeSettings);
        this.$emit('success', 'Einstellungen erfolgreich gespeichert');
      } catch (error) {
        this.$emit('error', error.message || 'Fehler beim Speichern der Einstellungen');
      } finally {
        this.loading = false;
      }
    },

    async updateModelConfig() {
      // Modell-Konfiguration über API aktualisieren
      return axios.post('/api/config', {
        section: 'model',
        config: this.modelSettings
      });
    },

    async updateTraderConfig() {
      // Trader-Konfiguration über API aktualisieren
      return axios.post('/api/config', {
        section: 'trader',
        config: {
          ...this.traderSettings,
          risk_management: this.riskManagement,
          exchanges: {
            binance: this.exchangeSettings
          }
        }
      });
    },

    async updateApiKeysConfig() {
      // API-Keys über API aktualisieren
      return axios.post('/api/config', {
        section: 'global',
        config: {
          api_keys: {
            news_api: this.newsApiSettings.news_api_key
          }
        }
      });
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
        this.newsApiSettings = {
          news_api_key: newSettings.api_keys?.news_api || '',
          sentiment_enabled: newSettings.model?.features?.includes('sentiment') || false
        };
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