"use client";
import { useQuery } from "@tanstack/react-query";
import { PageShell } from "@/components/page-shell";
import { api } from "@/lib/api";

export default function DashboardPage() {
  const { data } = useQuery({ queryKey: ["admin-stats"], queryFn: async () => (await api.get("/admin/stats")).data });
  return (
    <PageShell title="Organization Dashboard">
      <div className="grid md:grid-cols-2 gap-4">
        <article className="glass p-5"><p className="text-white/60">Organizations</p><p className="text-3xl">{data?.organizations ?? "-"}</p></article>
        <article className="glass p-5"><p className="text-white/60">Total Jobs</p><p className="text-3xl">{data?.jobs ?? "-"}</p></article>
      </div>
    </PageShell>
  );
}
