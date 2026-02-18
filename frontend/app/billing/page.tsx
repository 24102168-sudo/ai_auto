"use client";
import { PageShell } from "@/components/page-shell";
import { api } from "@/lib/api";

export default function BillingPage() {
  const checkout = async (plan: string) => {
    const { data } = await api.post(`/billing/checkout?plan=${plan}`, {}, { headers: { "x-csrf-token": "static-dev-token" } });
    window.location.href = data.url;
  };

  return (
    <PageShell title="Billing">
      <div className="flex gap-3">
        <button onClick={() => checkout("starter")} className="px-4 py-2 bg-white/10 rounded-xl">Starter</button>
        <button onClick={() => checkout("pro")} className="px-4 py-2 bg-aurora rounded-xl">Pro</button>
        <button onClick={() => checkout("agency")} className="px-4 py-2 bg-cyanlux text-black rounded-xl">Agency</button>
      </div>
    </PageShell>
  );
}
