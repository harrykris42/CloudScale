// src/components/metrics/Dashboard.tsx
"use client";

import { useQuery } from '@tanstack/react-query';
import { metricsApi } from '@/api/metrics';
import { MetricsChart } from './MetricsChart';
import { NetworkMetrics } from './NetworkMetrics';
import { ProgressCircle } from './ProgressCircle';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Activity, Cpu, HardDrive, CircuitBoard } from 'lucide-react';

export function Dashboard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['metrics', 'test-server-1'],
    queryFn: () => metricsApi.getMetrics('test-server-1'),
    refetchInterval: 5000,
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading metrics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg text-red-500">Error loading metrics</div>
      </div>
    );
  }

  const latestMetrics = data?.[0];
  if (!latestMetrics) return null;

  return (
    <div className="container mx-auto p-4 space-y-6">
      <h1 className="text-3xl font-bold">System Metrics Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">CPU Usage</CardTitle>
            <Cpu className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent className="flex justify-center pt-4">
            <ProgressCircle
              value={latestMetrics.cpu_usage}
              label="CPU"
              color="#8884d8"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Memory Usage</CardTitle>
            <CircuitBoard className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent className="flex justify-center pt-4">
            <ProgressCircle
              value={latestMetrics.memory_usage}
              label="Memory"
              color="#82ca9d"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Disk Usage</CardTitle>
            <HardDrive className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent className="flex justify-center pt-4">
            <ProgressCircle
              value={latestMetrics.disk_usage}
              label="Disk"
              color="#ffc658"
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Network Activity</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div>
                <div className="text-sm text-gray-500">Input</div>
                <div className="text-2xl font-bold">
                  {(latestMetrics.network_in / 1024 / 1024).toFixed(1)} MB/s
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-500">Output</div>
                <div className="text-2xl font-bold">
                  {(latestMetrics.network_out / 1024 / 1024).toFixed(1)} MB/s
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Resource Usage History</CardTitle>
          </CardHeader>
          <CardContent>
            <MetricsChart data={data} />
          </CardContent>
        </Card>

        <NetworkMetrics
          networkIn={latestMetrics.network_in}
          networkOut={latestMetrics.network_out}
        />
      </div>
    </div>
  );
}