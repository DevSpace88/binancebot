<template>
  <Card title="Neuen Job hinzufügen" class="job-form">
    <div class="form-group">
      <label for="job-symbol" class="label">Symbol</label>
      <input
        type="text"
        id="job-symbol"
        v-model="form.symbol"
        placeholder="z.B. BTC-USDT"
        class="input"
      />
      <div v-if="error.symbol" class="error-message">{{ error.symbol }}</div>
    </div>

    <div class="form-group">
      <label for="job-interval" class="label">Intervall</label>
      <select id="job-interval" v-model="form.interval" class="input">
        <option value="15m">15 Minuten</option>
        <option value="30m">30 Minuten</option>
        <option value="1h">1 Stunde</option>
        <option value="4h">4 Stunden</option>
        <option value="1d">1 Tag</option>
      </select>
    </div>

    <Button
      @click="addJob"
      :loading="loading"
      :disabled="loading || !form.symbol"
      text="Job hinzufügen"
      variant="primary"
      class="w-full"
    />
  </Card>
</template>

<script>
import Card from '../common/Card.vue';
import Button from '../common/Button.vue';

export default {
  name: 'JobForm',
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
        interval: '1h'
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
    addJob() {
      if (this.validate()) {
        this.$emit('add-job', { ...this.form });
      }
    }
  }
}
</script>

<style scoped>
.job-form {
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