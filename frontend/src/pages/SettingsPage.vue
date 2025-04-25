<template>
  <div class="settings-page">
    <h1 class="page-title">Einstellungen</h1>

    <form @submit.prevent="saveSettings" class="settings-form">
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
          type="submit"
          variant="primary"
          :loading="loading"
          :disabled="loading"
          text="Einstellungen speichern"
        />
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
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

      if (this.newsApiSettings.sentiment_enabled) {
        if (!this.modelSettings.features.includes('sentiment')) {
          this.modelSettings.features = [...this.modelSettings.features, 'sentiment'];
        }
      } else {
        if (this.modelSettings.features.includes('sentiment')) {
          this.modelSettings.features = this.modelSettings.features.filter(
            feature => feature !== 'sentiment'
          );
        }
      }
    },

    onModelTrained(result) {
      this.$emit('success', `Modell erfolgreich für ${result.symbol} trainiert`);
    },

    async saveSettings() {
      try {
        this.loading = true;

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

        await this.updateModelConfig();

        await this.updateTraderConfig();

        await this.updateApiKeysConfig();

        this.$emit('save-settings', completeSettings);
        this.$emit('success', 'Einstellungen erfolgreich gespeichert');
      } catch (error) {
        this.$emit('error', error.message || 'Fehler beim Speichern der Einstellungen');
      } finally {
        this.loading = false;
      }
    },

    async updateModelConfig() {
      return axios.post('/api/config', {
        section: 'model',
        config: this.modelSettings
      });
    },

    async updateTraderConfig() {
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

.settings-form {
  width: 100%;
}

.settings-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
  margin-bottom: 3rem;
}
</style>