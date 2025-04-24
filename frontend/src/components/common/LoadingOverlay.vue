<template>
  <div class="loading-overlay">
    <div class="spinner">
      <svg class="spinner-svg" viewBox="0 0 24 24">
        <circle
          class="spinner-circle"
          cx="12"
          cy="12"
          r="10"
          fill="none"
          stroke-width="2"
        ></circle>
      </svg>
    </div>
    <div class="loading-text">
      <slot>Daten werden geladen...</slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadingOverlay'
}
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(2px);
  z-index: 50;
}

.spinner {
  height: 3rem;
  width: 3rem;
  margin-bottom: 1rem;
}

.spinner-svg {
  animation: rotate 2s linear infinite;
  height: 100%;
  width: 100%;
}

.spinner-circle {
  stroke: var(--color-primary);
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}

.loading-text {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-foreground);
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
}
</style>