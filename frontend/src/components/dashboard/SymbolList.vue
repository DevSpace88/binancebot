<template>
  <Card title="Aktive Symbole" class="symbol-list-container">
    <div v-if="jobs.length === 0" class="empty-state">
      Keine aktiven Symbole
    </div>
    <div v-else class="symbols-grid">
      <div v-for="job in jobs" :key="job.id" class="symbol-item">
        <div class="symbol-name">{{ extractSymbol(job.id) }}</div>
        <div class="symbol-next-run">Nächste Prognose: {{ job.next_run }}</div>
      </div>
    </div>
  </Card>
</template>

<script>
import Card from '../common/Card.vue';

export default {
  name: 'SymbolList',
  components: {
    Card
  },
  props: {
    jobs: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    extractSymbol(jobId) {
      if (!jobId) return '';

      // Format: predict_BTC-USDT_1h
      const parts = jobId.split('_');
      if (parts.length >= 2) {
        return parts[1];
      }

      return jobId;
    }
  }
}
</script>

<style scoped>
.symbol-list-container {
  margin-bottom: 1.5rem;
}

.empty-state {
  padding: 2rem;
  text-align: center;
  color: var(--color-muted);
  background-color: var(--color-secondary);
  border-radius: var(--radius);
}

.symbols-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 0.75rem;
}

.symbol-item {
  padding: 1rem;
  border-radius: var(--radius);
  background-color: var(--color-secondary);
  transition: transform 0.2s ease;
}

.symbol-item:hover {
  transform: translateY(-2px);
}

.symbol-name {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: var(--color-foreground);
}

.symbol-next-run {
  font-size: 0.875rem;
  color: var(--color-muted-foreground);
}
</style>