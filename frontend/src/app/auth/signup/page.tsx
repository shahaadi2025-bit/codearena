"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState, type FormEvent } from "react";
import AuthShell from "@/components/AuthShell";
import Field from "@/components/Field";
import { useAuth } from "@/context/AuthContext";
import { ApiError } from "@/lib/api";

type Errors = Partial<Record<"username" | "email" | "password" | "form", string>>;

function validate(username: string, email: string, password: string): Errors {
  const errors: Errors = {};
  if (!/^[A-Za-z0-9_]{3,20}$/.test(username)) errors.username = "Use 3 to 20 letters, numbers or underscores.";
  if (!/^\S+@\S+\.\S+$/.test(email)) errors.email = "Enter a valid email address.";
  if (password.length < 8) errors.password = "Use at least 8 characters.";
  return errors;
}

export default function SignupPage() {
  const { signup, user, loading } = useAuth();
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<Errors>({});
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && user) router.replace("/dashboard");
  }, [loading, user, router]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    const found = validate(username, email, password);
    setErrors(found);
    if (Object.keys(found).length) return;
    setSubmitting(true);
    try {
      await signup(username, email, password);
      router.push("/dashboard");
    } catch (err) {
      if (err instanceof ApiError) {
        const field = err.field === "username" || err.field === "email" || err.field === "password" ? err.field : "form";
        setErrors({ [field]: err.message });
      } else {
        setErrors({ form: "Something went wrong. Try again." });
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthShell
      title="Create your account"
      subtitle="Pick a username and start at 1200 rating."
      footer={<>Already have an account? <Link href="/auth/login" className="text-gold underline-offset-4 hover:underline">Log in</Link></>}
    >
      <form onSubmit={onSubmit} noValidate className="space-y-5">
        <Field label="Username" id="username" autoComplete="username" value={username} onChange={(e) => setUsername(e.target.value)} error={errors.username} />
        <Field label="Email" id="email" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} error={errors.email} />
        <Field label="Password" id="password" type="password" autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} error={errors.password} hint="At least 8 characters." />
        {errors.form && <p role="alert" className="rounded-lg border border-coral/50 bg-coral/10 px-3.5 py-2.5 text-sm text-coral">{errors.form}</p>}
        <button
          type="submit"
          disabled={submitting}
          className="w-full rounded-lg bg-gold px-5 py-2.5 font-semibold text-ink transition hover:brightness-110 disabled:opacity-60"
        >
          {submitting ? "Creating account..." : "Create account"}
        </button>
      </form>
    </AuthShell>
  );
}
