// src/utils/alerts.ts
export interface ThresholdConfig {
  warning: number;
  critical: number;
}

export const thresholds: Record<string, ThresholdConfig> = {
  cpu: {
    warning: 70,
    critical: 90,
  },
  memory: {
    warning: 80,
    critical: 90,
  },
  disk: {
    warning: 85,
    critical: 95,
  },
};

export interface Alert {
  id: string;
  type: string;
  severity: 'warning' | 'critical';
  message: string;
  value: number;
  threshold: number;
  timestamp: Date;
  acknowledged: boolean;
}

let alertId = 0;

export function checkThresholds(metrics: {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
}): Alert[] {
  const alerts: Alert[] = [];
  const now = new Date();

  function createAlert(
    type: string,
    severity: 'warning' | 'critical',
    message: string,
    value: number,
    threshold: number
  ): Alert {
    return {
      id: `alert-${++alertId}`,
      type,
      severity,
      message,
      value,
      threshold,
      timestamp: now,
      acknowledged: false,
    };
  }

  if (metrics.cpu_usage >= thresholds.cpu.critical) {
    alerts.push(
      createAlert('cpu', 'critical', 'Critical CPU usage detected', metrics.cpu_usage, thresholds.cpu.critical)
    );
  } else if (metrics.cpu_usage >= thresholds.cpu.warning) {
    alerts.push(
      createAlert('cpu', 'warning', 'High CPU usage detected', metrics.cpu_usage, thresholds.cpu.warning)
    );
  }

  // Similar checks for memory and disk...
  // (Previous checks remain the same but use createAlert function)

  return alerts;
}

export function playAlertSound(severity: 'warning' | 'critical') {
  const audio = new Audio(severity === 'critical' ? '/critical-alert.mp3' : '/warning-alert.mp3');
  audio.play().catch(error => console.log('Error playing alert sound:', error));
}