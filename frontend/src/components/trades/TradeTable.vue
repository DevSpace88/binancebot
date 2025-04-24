<template>
  <div class="trade-table-container">
    <div v-if="trades.length === 0" class="empty-state">
      {{ emptyStateMessage }}
    </div>
    <div v-else class="trade-table">
      <div class="trade-table-header">
        <div v-for="column in columns" :key="column.key" class="trade-cell" :class="column.class">
          {{ column.label }}
        </div>
      </div>
      <div v-for="trade in trades" :key="trade.id" class="trade-row">
        <template v-for="column in columns" :key="`${trade.id}-${column.key}`">
          <div v-if="column.key === 'action'" class="trade-cell" :class="[column.class, getActionClass(trade.action)]">
            {{ trade.action?.toUpperCase() || 'N/A' }}
          </div>
          <div v-else-if="column.key === 'profit_loss'" class="trade-cell" :class="[column.class, getProfitLossClass(trade.profit_loss)]">
            {{ formatValue(trade, column.key, column.format) }}
          </div>
          <div v-else class="trade-cell" :class="column.class">
            {{ formatValue(trade, column.key, column.format) }}
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TradeTable',
  props: {
    trades: {
      type: Array,
      default: () => []
    },
    columns: {
      type: Array,
      required: true
    },
    emptyStateMessage: {
      type: String,
      default: 'Keine Trades verfügbar'
    }
  },
  methods: {
    formatValue(trade, key, format) {
      const value = this.getNestedValue(trade, key);

      if (value === undefined || value === null) {
        return 'N/A';
      }

      if (format === 'price') {
        return value.toFixed(2);
      } else if (format === 'percent') {
        return `${value.toFixed(2)}%`;
      } else if (format === 'time') {
        return this.formatTime(value);
      } else if (format === 'closeReason') {
        return this.formatCloseReason(value);
      }

      return value;
    },

    getNestedValue(obj, path) {
      return path.split('.').reduce((o, p) => (o ? o[p] : undefined), obj);
    },

    formatTime(timestamp) {
      if (!timestamp) return 'N/A';

      const date = new Date(timestamp);
      return date.toLocaleString();
    },

    formatCloseReason(reason) {
      if (reason === 'stop_loss') return 'Stop-Loss';
      if (reason === 'take_profit') return 'Take-Profit';
      if (reason === 'manual') return 'Manuell';
      return reason || 'N/A';
    },

    getActionClass(action) {
      if (action === 'buy') return 'positive';
      if (action === 'sell') return 'negative';
      return '';
    },

    getProfitLossClass(value) {
      if (!value) return '';
      return value > 0 ? 'positive' : value < 0 ? 'negative' : '';
    }
  }
}
</script>

<style scoped>
.trade-table-container {
  width: 100%;
  overflow-x: auto;
}

.empty-state {
  padding: 2rem;
  text-align: center;
  color: var(--color-muted);
  background-color: var(--color-secondary);
  border-radius: var(--radius);
}

.trade-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: var(--radius);
  overflow: hidden;
}

.trade-table-header {
  display: flex;
  background-color: var(--color-secondary);
  font-weight: 600;
  border-bottom: 1px solid var(--color-border);
}

.trade-row {
  display: flex;
  border-bottom: 1px solid var(--color-border);
  transition: background-color 0.2s;
}

.trade-row:last-child {
  border-bottom: none;
}

.trade-row:hover {
  background-color: var(--color-secondary);
}

.trade-cell {
  padding: 0.75rem 1rem;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: flex;
  align-items: center;
}

.cell-small {
  flex: 0.7;
}

.cell-medium {
  flex: 1;
}

.cell-large {
  flex: 1.5;
}

.positive {
  color: var(--color-positive);
}

.negative {
  color: var(--color-negative);
}
</style>