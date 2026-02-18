"use client";
import { FormEvent, useState } from "react";
import { PageShell } from "@/components/page-shell";
import { api, setAuthToken } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function LoginPage() {
  const setToken = useAuthStore((s) => s.setToken);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    const { data } = await api.post("/auth/login", { email, password }, { headers: { "x-csrf-token": "static-dev-token" } });
    setToken(data.access_token);
    setAuthToken(data.access_token);
  };

  return (
    <PageShell title="Login">
      <form onSubmit={submit} className="space-y-3 max-w-md">
        <input className="w-full bg-black/30 p-3 rounded-xl" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="w-full bg-black/30 p-3 rounded-xl" placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="px-5 py-2 bg-aurora rounded-xl">Sign In</button>
      </form>
    </PageShell>
  );
}
