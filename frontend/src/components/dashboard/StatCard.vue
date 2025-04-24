<template>
  <div class="stat-card">
    <h3 class="stat-title">{{ title }}</h3>
    <div class="stat-value" :class="valueClass">{{ value }}</div>
    <div v-if="subtitle" class="stat-subtitle">{{ subtitle }}</div>
  </div>
</template>

<script>
export default {
  name: 'StatCard',
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: [String, Number],
      required: true
    },
    subtitle: {
      type: String,
      default: ''
    },
    status: {
      type: String,
      default: 'neutral',
      validator: (value) => ['positive', 'negative', 'neutral'].includes(value)
    }
  },
  computed: {
    valueClass() {
      return {
        'positive': this.status === 'positive',
        'negative': this.status === 'negative'
      }
    }
  }
}
</script>

<style scoped>
.stat-card {
  padding: 1.25rem;
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.stat-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-muted-foreground);
  margin: 0 0 0.5rem 0;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--color-foreground);
  margin-bottom: 0.25rem;
}

.stat-value.positive {
  color: var(--color-positive);
}

.stat-value.negative {
  color: var(--color-negative);
}

.stat-subtitle {
  font-size: 0.75rem;
  color: var(--color-muted);
}
</style>