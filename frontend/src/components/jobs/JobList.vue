<template>
  <Card title="Aktive Jobs" class="job-list">
    <div v-if="jobs.length === 0" class="empty-state">
      Keine aktiven Jobs
    </div>
    <div v-else class="job-table">
      <div class="job-table-header">
        <div class="job-cell job-id">Job ID</div>
        <div class="job-cell job-symbol">Symbol</div>
        <div class="job-cell job-interval">Intervall</div>
        <div class="job-cell job-next-run">Nächste Ausführung</div>
        <div class="job-cell job-actions">Aktionen</div>
      </div>
      <div v-for="job in jobs" :key="job.id" class="job-row">
        <div class="job-cell job-id">{{ job.id }}</div>
        <div class="job-cell job-symbol">{{ extractSymbol(job.id) }}</div>
        <div class="job-cell job-interval">{{ job.interval }} {{ job.unit || '' }}</div>
        <div class="job-cell job-next-run">{{ job.next_run }}</div>
        <div class="job-cell job-actions">
          <Button
            @click="removeJob(job.id)"
            variant="danger"
            size="sm"
            :loading="isLoading(job.id)"
            :disabled="isLoading(job.id)"
            text="Löschen"
          />
        </div>
      </div>
    </div>
  </Card>
</template>

<script>
import Card from '../common/Card.vue';
import Button from '../common/Button.vue';

export default {
  name: 'JobList',
  components: {
    Card,
    Button
  },
  props: {
    jobs: {
      type: Array,
      default: () => []
    },
    loadingJobId: {
      type: String,
      default: null
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
    },
    removeJob(jobId) {
      this.$emit('remove-job', jobId);
    },
    isLoading(jobId) {
      return this.loadingJobId === jobId;
    }
  }
}
</script>

<style scoped>
.job-list {
  margin-bottom: 1.5rem;
}

.empty-state {
  padding: 2rem;
  text-align: center;
  color: var(--color-muted);
  background-color: var(--color-secondary);
  border-radius: var(--radius);
}

.job-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: var(--radius);
  overflow: hidden;
}

.job-table-header {
  display: flex;
  background-color: var(--color-secondary);
  font-weight: 600;
  border-bottom: 1px solid var(--color-border);
}

.job-row {
  display: flex;
  border-bottom: 1px solid var(--color-border);
  transition: background-color 0.2s;
}

.job-row:last-child {
  border-bottom: none;
}

.job-row:hover {
  background-color: var(--color-secondary);
}

.job-cell {
  padding: 0.75rem 1rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: flex;
  align-items: center;
}

.job-id {
  flex: 1.5;
}

.job-symbol, .job-interval {
  flex: 1;
}

.job-next-run {
  flex: 1.5;
}

.job-actions {
  flex: 0.8;
  justify-content: flex-end;
}
</style>