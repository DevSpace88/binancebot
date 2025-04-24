/**
 * Hilfsfunktionen für die Arbeit mit Diagrammen
 */

// Generiert Fake-Daten für Demo-Zwecke
export const generatePerformanceData = (days = 30, minValue = -2, maxValue = 3) => {
  return Array(days).fill(0).map(() => {
    return minValue + Math.random() * (maxValue - minValue);
  });
};

// Generiert Labels für Zeiträume
export const generateTimeLabels = (days = 30, format = 'date') => {
  const labels = [];
  const today = new Date();

  for (let i = days; i >= 0; i--) {
    const date = new Date();
    date.setDate(today.getDate() - i);

    if (format === 'date') {
      labels.push(date.toLocaleDateString());
    } else if (format === 'datetime') {
      labels.push(date.toLocaleString());
    } else if (format === 'time') {
      labels.push(date.toLocaleTimeString());
    }
  }

  return labels;
};

// Berechnet die Trendrichtung (positiv, negativ, neutral) basierend auf Daten
export const calculateTrend = (data) => {
  if (!data || data.length === 0) return 'neutral';

  const sum = data.reduce((acc, val) => acc + val, 0);
  const avg = sum / data.length;

  if (avg > 0.5) return 'positive';
  if (avg < -0.5) return 'negative';
  return 'neutral';
};

// Erzeugt eine einheitliche Farbpalette für Diagramme
export const chartColors = {
  primary: 'var(--color-primary)',
  secondary: 'var(--color-secondary)',
  positive: 'var(--color-positive)',
  negative: 'var(--color-negative)',
  muted: 'var(--color-muted)',
  background: 'var(--color-background)',
  border: 'var(--color-border)',

  // Transparente Versionen für Hintergründe
  primaryTransparent: 'rgba(99, 102, 241, 0.1)',
  positiveTransparent: 'rgba(34, 197, 94, 0.1)',
  negativeTransparent: 'rgba(239, 68, 68, 0.1)'
};

// Standardoptionen für Chart.js
export const getDefaultChartOptions = (type = 'line') => {
  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'nearest',
      intersect: false,
      axis: 'x'
    },
    plugins: {
      tooltip: {
        backgroundColor: 'var(--color-foreground)',
        titleColor: 'var(--color-background)',
        bodyColor: 'var(--color-background)',
        borderColor: 'var(--color-border)',
        borderWidth: 1,
        padding: 10,
        cornerRadius: 4
      },
      legend: {
        display: true,
        position: 'top',
        labels: {
          color: 'var(--color-foreground)',
          usePointStyle: true,
          padding: 15
        }
      }
    }
  };

  // Spezifische Optionen je nach Diagrammtyp
  if (type === 'line') {
    return {
      ...baseOptions,
      scales: {
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: 'var(--color-muted-foreground)'
          }
        },
        y: {
          beginAtZero: false,
          grid: {
            color: 'var(--color-border)'
          },
          ticks: {
            color: 'var(--color-muted-foreground)'
          }
        }
      }
    };
  }

  if (type === 'bar') {
    return {
      ...baseOptions,
      scales: {
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: 'var(--color-muted-foreground)'
          }
        },
        y: {
          beginAtZero: true,
          grid: {
            color: 'var(--color-border)'
          },
          ticks: {
            color: 'var(--color-muted-foreground)'
          }
        }
      }
    };
  }

  return baseOptions;
};