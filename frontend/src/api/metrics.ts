// src/api/metrics.ts
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1/monitoring';

export interface Metrics {
  id: number;
  resource_id: string;
  resource_type: string;
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  network_in: number;
  network_out: number;
  timestamp: string;
}

export const metricsApi = {
  getMetrics: async (resourceId: string): Promise<Metrics[]> => {
    try {
      const response = await axios.get(`${API_BASE_URL}/metrics/${resourceId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching metrics:', error);
      return [];
    }
  },

  getLatestMetrics: async (): Promise<Metrics | null> => {
    try {
      const response = await axios.get(`${API_BASE_URL}/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching latest metrics:', error);
      return null;
    }
  },

  createMetrics: async (metrics: Omit<Metrics, 'id' | 'timestamp'>): Promise<Metrics> => {
    const response = await axios.post(`${API_BASE_URL}/metrics/`, metrics);
    return response.data;
  }
};