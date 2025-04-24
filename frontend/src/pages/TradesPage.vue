<template>
  <div class="trades-page">
    <h1 class="page-title">Trades</h1>

    <div class="tabs">
      <button
        @click="activeTab = 'open'"
        class="tab-button"
        :class="{ active: activeTab === 'open' }"
      >
        Offene Trades
      </button>
      <button
        @click="activeTab = 'closed'"
        class="tab-button"
        :class="{ active: activeTab === 'closed' }"
      >
        Geschlossene Trades
      </button>
    </div>

    <Card class="trades-card">
      <TradeTable
        v-if="activeTab === 'open'"
        :trades="openTrades"
        :columns="openTradesColumns"
        emptyStateMessage="Keine offenen Trades"
      />

      <TradeTable
        v-else
        :trades="closedTrades"
        :columns="closedTradesColumns"
        emptyStateMessage="Keine geschlossenen Trades"
      />
    </Card>
  </div>
</template>

<script>
import Card from '../components/common/Card.vue';
import TradeTable from '../components/trades/TradeTable.vue';

export default {
  name: 'TradesPage',
  components: {
    Card,
    TradeTable
  },
  props: {
    openTrades: {
      type: Array,
      default: () => []
    },
    closedTrades: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      activeTab: 'open',
      openTradesColumns: [
        { key: 'symbol', label: 'Symbol', class: 'cell-medium' },
        { key: 'action', label: 'Aktion', class: 'cell-small' },
        { key: 'price', label: 'Preis', format: 'price', class: 'cell-medium' },
        { key: 'amount', label: 'Betrag', format: 'price', class: 'cell-medium' },
        { key: 'timestamp', label: 'Zeit', format: 'time', class: 'cell-large' },
        { key: 'stop_loss', label: 'Stop-Loss', format: 'price', class: 'cell-medium' },
        { key: 'take_profit', label: 'Take-Profit', format: 'price', class: 'cell-medium' }
      ],
      closedTradesColumns: [
        { key: 'symbol', label: 'Symbol', class: 'cell-medium' },
        { key: 'action', label: 'Aktion', class: 'cell-small' },
        { key: 'price', label: 'Eröffnungspreis', format: 'price', class: 'cell-medium' },
        { key: 'close_price', label: 'Schlusspreis', format: 'price', class: 'cell-medium' },
        { key: 'profit_loss', label: 'P/L %', format: 'percent', class: 'cell-medium' },
        { key: 'close_reason', label: 'Grund', format: 'closeReason', class: 'cell-medium' },
        { key: 'close_time', label: 'Geschlossen', format: 'time', class: 'cell-large' }
      ]
    };
  }
}
</script>

<style scoped>
.trades-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-foreground);
}

.tabs {
  display: flex;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
}

.tab-button {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  font-weight: 500;
  color: var(--color-muted-foreground);
  transition: all 0.2s;
}

.tab-button:hover {
  color: var(--color-foreground);
}

.tab-button.active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.trades-card {
  margin-bottom: 1.5rem;
}
</style>