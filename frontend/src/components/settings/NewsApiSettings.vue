<template>
  <Card title="News API-Einstellungen" class="settings-section">
    <div class="form-group">
      <label for="news-api-key" class="label">News API-Schlüssel</label>
      <input
        type="password"
        id="news-api-key"
        v-model="localSettings.news_api_key"
        class="input"
        @change="emitChanges"
      >
      <div class="input-helper">Schlüssel für News und Sentiment-Analyse (z.B. Alpha Vantage)</div>
    </div>

    <div class="form-group">
      <div class="flex-space-between">
        <label for="sentiment-enabled" class="label">Sentiment-Analyse aktivieren</label>
        <div class="toggle-switch">
          <input type="checkbox" id="sentiment-enabled" v-model="localSettings.sentiment_enabled" @change="emitChanges">
          <label for="sentiment-enabled"></label>
        </div>
      </div>
      <div class="input-helper">Aktiviert die Einbeziehung von Nachrichtensentiment in die Prognosen</div>
    </div>
  </Card>
</template>

<script>
import Card from '../common/Card.vue';

export default {
  name: 'NewsApiSettings',
  components: {
    Card
  },
  props: {
    newsSettings: {
      type: Object,
      default: () => ({
        news_api_key: '',
        sentiment_enabled: false
      })
    }
  },
  data() {
    return {
      localSettings: {
        news_api_key: '',
        sentiment_enabled: false
      }
    };
  },
  methods: {
    // Änderungen an Parent weitergeben
    emitChanges() {
      this.$emit('change-news-api', { ...this.localSettings });
    },

    // Lokale Einstellungen aus Props aktualisieren
    updateFromProps() {
      this.localSettings = {
        news_api_key: this.newsSettings.news_api_key || '',
        sentiment_enabled: this.newsSettings.sentiment_enabled ?? false
      };
    }
  },
  watch: {
    newsSettings: {
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

.input-helper {
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: var(--color-muted);
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