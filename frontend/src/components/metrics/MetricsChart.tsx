"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Metrics } from '@/api/metrics';

interface MetricsChartProps {
  data: Metrics[];
}

export function MetricsChart({ data }: MetricsChartProps) {
  return (
    <div className="h-[400px] mt-4">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
          <XAxis
            dataKey="timestamp"
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => new Date(value).toLocaleTimeString()}
          />
          <YAxis />
          <Tooltip
            labelFormatter={(value) => new Date(value).toLocaleString()}
            contentStyle={{ backgroundColor: 'rgb(30, 41, 59)', border: 'none' }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="cpu_usage"
            stroke="#8884d8"
            name="CPU Usage %"
            strokeWidth={2}
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="memory_usage"
            stroke="#82ca9d"
            name="Memory Usage %"
            strokeWidth={2}
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="disk_usage"
            stroke="#ffc658"
            name="Disk Usage %"
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}