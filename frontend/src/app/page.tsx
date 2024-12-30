// src/app/page.tsx
import { Dashboard } from "@/components/metrics/Dashboard";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";

export default function Home() {
  return (
    <ProtectedRoute>
      <main className="min-h-screen bg-background">
        <Dashboard />
      </main>
    </ProtectedRoute>
  );
}