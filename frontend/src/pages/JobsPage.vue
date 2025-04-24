<template>
  <div class="jobs-page">
    <h1 class="page-title">Automatisierte Jobs</h1>

    <JobForm
      :loading="loading.addJob"
      @add-job="addJob"
    />

    <JobList
      :jobs="jobs"
      :loading-job-id="loading.removeJob"
      @remove-job="removeJob"
    />
  </div>
</template>

<script>
import JobForm from '../components/jobs/JobForm.vue';
import JobList from '../components/jobs/JobList.vue';

export default {
  name: 'JobsPage',
  components: {
    JobForm,
    JobList
  },
  props: {
    jobs: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      loading: {
        addJob: false,
        removeJob: null
      }
    };
  },
  methods: {
    async addJob(jobData) {
      try {
        this.loading.addJob = true;
        this.$emit('add-job', jobData);
      } catch (error) {
        this.$emit('error', error.message || 'Fehler beim Hinzufügen des Jobs');
      } finally {
        this.loading.addJob = false;
      }
    },

    async removeJob(jobId) {
      try {
        this.loading.removeJob = jobId;
        this.$emit('remove-job', jobId);
      } catch (error) {
        this.$emit('error', error.message || 'Fehler beim Löschen des Jobs');
      } finally {
        this.loading.removeJob = null;
      }
    }
  }
}
</script>

<style scoped>
.jobs-page {
  max-width: 1000px;
  margin: 0 auto;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-foreground);
}
</style>