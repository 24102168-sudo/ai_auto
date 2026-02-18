"use client";
import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { PageShell } from "@/components/page-shell";
import { api } from "@/lib/api";

export default function JobDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data } = useQuery({ queryKey: ["job", id], queryFn: async () => (await api.get(`/jobs/${id}`)).data });
  return (
    <PageShell title={`Job #${id}`}>
      <pre className="text-xs overflow-x-auto bg-black/30 p-4 rounded-xl">{JSON.stringify(data, null, 2)}</pre>
      <div className="flex gap-3">
        <button className="px-4 py-2 bg-aurora rounded-xl">Download Audio</button>
        <button className="px-4 py-2 bg-cyanlux text-black rounded-xl">Download Video</button>
      </div>
    </PageShell>
  );
}
