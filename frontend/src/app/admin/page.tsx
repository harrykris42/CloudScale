// src/app/admin/page.tsx
import { UserManagement } from "@/components/admin/UserManagement";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";

export default function AdminPage() {
  return (
    <ProtectedRoute>
      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>
        <UserManagement />
      </div>
    </ProtectedRoute>
  );
}