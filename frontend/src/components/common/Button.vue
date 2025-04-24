<template>
  <button
    class="btn"
    :class="buttonClasses"
    :type="type"
    :disabled="disabled || loading"
    @click="onClick"
  >
    <span v-if="loading" class="btn-spinner">
      <svg class="btn-spinner-svg" viewBox="0 0 24 24">
        <circle class="btn-spinner-circle" cx="12" cy="12" r="10" fill="none" stroke-width="2"></circle>
      </svg>
    </span>
    <span v-else-if="icon" class="btn-icon">
      <span v-html="icon"></span>
    </span>
    <span class="btn-content" :class="{ 'ml-2': loading || icon }">
      <slot>{{ text }}</slot>
    </span>
  </button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    variant: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'outline', 'danger', 'ghost', 'link'].includes(value)
    },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg'].includes(value)
    },
    type: {
      type: String,
      default: 'button',
      validator: (value) => ['button', 'submit', 'reset'].includes(value)
    },
    text: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    icon: {
      type: String,
      default: ''
    },
    block: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    buttonClasses() {
      return {
        [`btn-${this.variant}`]: true,
        [`btn-${this.size}`]: true,
        'btn-block': this.block,
        'btn-loading': this.loading,
        'btn-icon-only': this.icon && !this.$slots.default && !this.text
      }
    }
  },
  methods: {
    onClick(event) {
      if (!this.disabled && !this.loading) {
        this.$emit('click', event)
      }
    }
  }
}
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius);
  font-weight: 500;
  transition: all 0.2s ease;
  cursor: pointer;
  border: 1px solid transparent;
}

.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-primary-foreground);
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
}

.btn-secondary {
  background-color: var(--color-secondary);
  color: var(--color-secondary-foreground);
}

.btn-secondary:hover:not(:disabled) {
  background-color: var(--color-secondary-hover);
}

.btn-outline {
  background-color: transparent;
  border-color: var(--color-border);
  color: var(--color-foreground);
}

.btn-outline:hover:not(:disabled) {
  background-color: var(--color-secondary);
  border-color: var(--color-muted);
}

.btn-danger {
  background-color: var(--color-negative);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-ghost {
  background-color: transparent;
  color: var(--color-foreground);
}

.btn-ghost:hover:not(:disabled) {
  background-color: var(--color-secondary);
}

.btn-link {
  background-color: transparent;
  color: var(--color-primary);
  text-decoration: underline;
  padding: 0;
}

.btn-link:hover:not(:disabled) {
  text-decoration: none;
}

.btn-sm {
  height: 2rem;
  padding: 0 0.75rem;
  font-size: 0.75rem;
}

.btn-md {
  height: 2.5rem;
  padding: 0 1rem;
  font-size: 0.875rem;
}

.btn-lg {
  height: 3rem;
  padding: 0 1.5rem;
  font-size: 1rem;
}

.btn-block {
  width: 100%;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-icon {
  display: flex;
  align-items: center;
}

.btn-icon svg {
  width: 1rem;
  height: 1rem;
}

.btn-icon-only {
  padding: 0;
  width: 2.5rem;
}

.btn-spinner {
  display: inline-flex;
  width: 1rem;
  height: 1rem;
}

.btn-spinner-svg {
  animation: spin 1s linear infinite;
  width: 100%;
  height: 100%;
}

.btn-spinner-circle {
  stroke: currentColor;
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}

.btn-content {
  display: inline-block;
}

.ml-2 {
  margin-left: 0.5rem;
}

@keyframes spin {
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