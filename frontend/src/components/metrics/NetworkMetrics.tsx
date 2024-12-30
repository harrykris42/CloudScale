// src/components/metrics/NetworkMetrics.tsx
"use client";

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface NetworkMetricsProps {
  networkIn: number;
  networkOut: number;
}

export function NetworkMetrics({ networkIn, networkOut }: NetworkMetricsProps) {
  const data = [
    { name: 'Input', value: networkIn / 1024 / 1024 },
    { name: 'Output', value: networkOut / 1024 / 1024 },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Network Traffic (MB/s)</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[200px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip
                formatter={(value: number) => value.toFixed(2) + ' MB/s'}
              />
              <Bar dataKey="value" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}