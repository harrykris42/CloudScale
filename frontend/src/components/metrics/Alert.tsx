// src/components/metrics/Alert.tsx
"use client";

import { AlertCircle } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

interface MetricAlert {
  type: "cpu" | "memory" | "disk" | "network";
  threshold: number;
  currentValue: number;
  message: string;
}

export function MetricAlert({ type, threshold, currentValue, message }: MetricAlert) {
  return (
    <Alert variant="destructive" className="mb-4">
      <AlertCircle className="h-4 w-4" />
      <AlertTitle className="ml-2">High {type.toUpperCase()} Usage Alert</AlertTitle>
      <AlertDescription className="ml-2">
        {message} (Current: {currentValue.toFixed(1)}%, Threshold: {threshold}%)
      </AlertDescription>
    </Alert>
  );
}