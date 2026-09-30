"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useAuth } from "@/context/AuthContext";

// Use at the top of any page that needs a signed-in user. Redirects to login otherwise.
export function useRequireAuth() {
  const auth = useAuth();
  const router = useRouter();
  useEffect(() => {
    if (!auth.loading && !auth.user) router.replace("/auth/login");
  }, [auth.loading, auth.user, router]);
  return auth;
}
