// src/components/admin/UserManagement.tsx
"use client";

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Switch } from "@/components/ui/switch";
import api from '@/api/client';

interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
}

export function UserManagement() {
  const [error, setError] = useState('');
  const queryClient = useQueryClient();

  const { data: users, isLoading } = useQuery<User[]>({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await api.get('/auth/users');
      return response.data;
    },
  });

  const updateUserMutation = useMutation({
    mutationFn: async ({ userId, data }: { userId: number; data: Partial<User> }) => {
      const response = await api.patch(`/auth/users/${userId}`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
    onError: (error: Error) => {
      setError(error.message);
    },
  });

  const deleteUserMutation = useMutation({
    mutationFn: async (userId: number) => {
      await api.delete(`/auth/users/${userId}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
    onError: (error: Error) => {
      setError(error.message);
    },
  });

  const toggleUserStatus = (user: User) => {
    updateUserMutation.mutate({
      userId: user.id,
      data: { is_active: !user.is_active },
    });
  };

  const toggleAdminStatus = (user: User) => {
    updateUserMutation.mutate({
      userId: user.id,
      data: { is_admin: !user.is_admin },
    });
  };

  if (isLoading) {
    return <div>Loading users...</div>;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>User Management</CardTitle>
      </CardHeader>
      <CardContent>
        {error && (
          <Alert variant="destructive" className="mb-4">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Username</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Active</TableHead>
              <TableHead>Admin</TableHead>
              <TableHead>Created At</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {users?.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.username}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  <Switch
                    checked={user.is_active}
                    onCheckedChange={() => toggleUserStatus(user)}
                  />
                </TableCell>
                <TableCell>
                  <Switch
                    checked={user.is_admin}
                    onCheckedChange={() => toggleAdminStatus(user)}
                  />
                </TableCell>
                <TableCell>
                  {new Date(user.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => {
                      if (confirm('Are you sure you want to delete this user?')) {
                        deleteUserMutation.mutate(user.id);
                      }
                    }}
                  >
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}