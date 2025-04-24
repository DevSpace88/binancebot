<template>
  <div class="dashboard-page">
    <h1 class="page-title">Dashboard</h1>

    <div class="stats-grid">
      <StatCard
        title="Offene Trades"
        :value="stats.open_trades || 0"
      />
      <StatCard
        title="Trades Heute"
        :value="stats.daily_trades || 0"
      />
      <StatCard
        title="Gewinn/Verlust Heute"
        :value="stats.daily_profit_loss ? `${stats.daily_profit_loss.toFixed(2)}%` : '0.00%'"
        :status="stats.daily_profit_loss > 0 ? 'positive' : stats.daily_profit_loss < 0 ? 'negative' : 'neutral'"
      />
      <StatCard
        title="Gewinnrate"
        :value="stats.win_rate ? `${stats.win_rate.toFixed(2)}%` : '0.00%'"
      />
    </div>

    <PerformanceChart />

    <SymbolList :jobs="jobs" />
  </div>
</template>

<script>
import StatCard from '../components/dashboard/StatCard.vue';
import PerformanceChart from '../components/dashboard/PerformanceChart.vue';
import SymbolList from '../components/dashboard/SymbolList.vue';

export default {
  name: 'DashboardPage',
  components: {
    StatCard,
    PerformanceChart,
    SymbolList
  },
  props: {
    stats: {
      type: Object,
      default: () => ({})
    },
    jobs: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>
.dashboard-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-foreground);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>