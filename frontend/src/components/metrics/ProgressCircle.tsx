// src/components/metrics/ProgressCircle.tsx
"use client";

import React from 'react';

interface ProgressCircleProps {
  value: number;
  label: string;
  color?: string;
}

export function ProgressCircle({ value, label, color = "#3B82F6" }: ProgressCircleProps) {
  const radius = 35;
  const circumference = 2 * Math.PI * radius;
  const progress = ((100 - value) / 100) * circumference;

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg className="transform -rotate-90 w-24 h-24">
        <circle
          className="text-gray-200"
          strokeWidth="8"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="48"
          cy="48"
        />
        <circle
          className="transition-all duration-300 ease-in-out"
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={progress}
          strokeLinecap="round"
          stroke={color}
          fill="transparent"
          r={radius}
          cx="48"
          cy="48"
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="text-xl font-bold">{value.toFixed(1)}%</span>
        <span className="text-sm text-gray-500">{label}</span>
      </div>
    </div>
  );
}