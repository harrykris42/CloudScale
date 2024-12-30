// src/components/metrics/AlertHistory.tsx
"use client";

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertCircle, AlertTriangle, XCircle } from "lucide-react";
import { Alert } from '@/utils/alerts';

interface AlertHistoryProps {
  alerts: Alert[];
  onDismiss: (index: number) => void;
}

export function AlertHistory({ alerts, onDismiss }: AlertHistoryProps) {
  const [showAll, setShowAll] = useState(false);
  const displayAlerts = showAll ? alerts : alerts.slice(0, 5);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex justify-between items-center">
          <span>Alert History</span>
          <button
            onClick={() => setShowAll(!showAll)}
            className="text-sm text-blue-500 hover:text-blue-700"
          >
            {showAll ? 'Show Less' : 'Show All'}
          </button>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {displayAlerts.map((alert, index) => (
            <div
              key={index}
              className={`flex items-start justify-between p-4 rounded-lg ${
                alert.severity === 'critical'
                  ? 'bg-red-50 border-red-200'
                  : 'bg-yellow-50 border-yellow-200'
              } border`}
            >
              <div className="flex items-start space-x-3">
                {alert.severity === 'critical' ? (
                  <AlertCircle className="h-5 w-5 text-red-500 mt-0.5" />
                ) : (
                  <AlertTriangle className="h-5 w-5 text-yellow-500 mt-0.5" />
                )}
                <div>
                  <h4 className="text-sm font-semibold">
                    {alert.type.toUpperCase()} Alert
                  </h4>
                  <p className="text-sm text-gray-600">{alert.message}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    Value: {alert.value.toFixed(1)}% (Threshold: {alert.threshold}%)
                  </p>
                </div>
              </div>
              <button
                onClick={() => onDismiss(index)}
                className="text-gray-400 hover:text-gray-600"
              >
                <XCircle className="h-5 w-5" />
              </button>
            </div>
          ))}
          {alerts.length === 0 && (
            <div className="text-center text-gray-500 py-4">
              No alerts to display
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}