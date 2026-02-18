"use client";
import { FormEvent, useState } from "react";
import { PageShell } from "@/components/page-shell";
import { api } from "@/lib/api";

export default function RegisterPage() {
  const [organizationName, setOrganizationName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    await api.post("/auth/register", { organization_name: organizationName, email, password }, { headers: { "x-csrf-token": "static-dev-token" } });
  };

  return (
    <PageShell title="Create Account">
      <form onSubmit={submit} className="space-y-3 max-w-md">
        <input className="w-full bg-black/30 p-3 rounded-xl" placeholder="Organization Name" value={organizationName} onChange={(e) => setOrganizationName(e.target.value)} />
        <input className="w-full bg-black/30 p-3 rounded-xl" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="w-full bg-black/30 p-3 rounded-xl" placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="px-5 py-2 bg-aurora rounded-xl">Register</button>
      </form>
    </PageShell>
  );
}
