<template>
  <Card title="Performance Übersicht" class="performance-chart-container">
    <div class="chart-wrapper">
      <canvas ref="chartCanvas" width="400" height="200"></canvas>
    </div>
  </Card>
</template>

<script>
import Card from '../common/Card.vue';
import Chart from 'chart.js/auto';

export default {
  name: 'PerformanceChart',
  components: {
    Card
  },
  props: {
    data: {
      type: Array,
      default: () => Array(30).fill(0).map(() => Math.random() * 4 - 1) // Default dummy data
    }
  },
  data() {
    return {
      chart: null
    };
  },
  mounted() {
    this.initChart();
  },
  methods: {
    initChart() {
      if (!this.$refs.chartCanvas) return;

      const ctx = this.$refs.chartCanvas.getContext('2d');

      if (this.chart) {
        this.chart.destroy();
      }

      const labels = [];
      const today = new Date();
      for (let i = 30; i >= 0; i--) {
        const date = new Date();
        date.setDate(today.getDate() - i);
        labels.push(date.toLocaleDateString());
      }

      const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        interaction: {
          mode: 'nearest',
          intersect: false,
          axis: 'x'
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              usePointStyle: true,
              padding: 15
            }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `${context.dataset.label}: ${context.raw.toFixed(2)}%`;
              }
            }
          },
          filler: {
            propagate: false
          }
        },
        scales: {
          x: {
            grid: {
              display: false
            },
            ticks: {
              maxRotation: 0,
              autoSkip: true,
              maxTicksLimit: 10
            }
          },
          y: {
            beginAtZero: false,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          }
        }
      };

      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Tägliche P/L (%)',
            data: this.data,
            borderColor: 'rgb(99, 102, 241)',
            backgroundColor: 'rgba(99, 102, 241, 0.1)',
            tension: 0.4,
            fill: true,
            borderWidth: 2,
            pointRadius: 3,
            pointHoverRadius: 5
          }]
        },
        options: chartOptions
      });
    }
  },
  watch: {
    data: {
      handler() {
        this.$nextTick(() => {
          this.initChart();
        });
      },
      deep: true
    }
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }
  }
}
</script>

<style scoped>
.performance-chart-container {
  margin-bottom: 1.5rem;
}

.chart-wrapper {
  position: relative;
  height: 300px;
  width: 100%;
}
</style>