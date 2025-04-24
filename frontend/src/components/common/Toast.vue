<template>
  <div class="toast-container">
    <div class="toast" :class="toastClasses">
      <div class="toast-content">
        <div v-if="type === 'success'" class="toast-icon success">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
        </div>
        <div v-else-if="type === 'error'" class="toast-icon error">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
        </div>
        <div v-else class="toast-icon info">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
        </div>
        <div class="toast-message">{{ message }}</div>
      </div>
      <button @click="$emit('dismiss')" class="toast-close">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Toast',
  props: {
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['success', 'error', 'info'].includes(value)
    },
    duration: {
      type: Number,
      default: 5000
    }
  },
  computed: {
    toastClasses() {
      return {
        'toast-success': this.type === 'success',
        'toast-error': this.type === 'error',
        'toast-info': this.type === 'info'
      }
    }
  },
  mounted() {
    if (this.duration > 0) {
      setTimeout(() => {
        this.$emit('dismiss');
      }, this.duration);
    }
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 1.5rem;
  right: 1.5rem;
  z-index: 50;
  max-width: 420px;
  width: calc(100% - 2rem);
}

.toast {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-radius: var(--radius);
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  animation: slideIn 0.2s ease-out;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.toast-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
}

.toast-icon svg {
  width: 1.25rem;
  height: 1.25rem;
}

.toast-icon.success {
  color: var(--color-positive);
}

.toast-icon.error {
  color: var(--color-negative);
}

.toast-icon.info {
  color: var(--color-primary);
}

.toast-success {
  border-left: 4px solid var(--color-positive);
}

.toast-error {
  border-left: 4px solid var(--color-negative);
}

.toast-info {
  border-left: 4px solid var(--color-primary);
}

.toast-message {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-foreground);
}

.toast-close {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  margin-left: 0.5rem;
  background: transparent;
  border: none;
  color: var(--color-muted);
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.toast-close:hover {
  opacity: 1;
}

.toast-close svg {
  width: 1rem;
  height: 1rem;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>