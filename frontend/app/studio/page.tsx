"use client";
import { FormEvent, useState } from "react";
import { PageShell } from "@/components/page-shell";
import { api } from "@/lib/api";

export default function StudioPage() {
  const [form, setForm] = useState({ project_id: 1, title: "", topic: "", duration_seconds: 60, voice_type: "alloy" });
  const [jobId, setJobId] = useState<number | null>(null);
  const [status, setStatus] = useState("idle");

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    const { data } = await api.post("/jobs", form, { headers: { "x-csrf-token": "static-dev-token" } });
    setJobId(data.id);
    const ws = new WebSocket(`${(process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000")}/ws/jobs/${data.id}`);
    ws.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      setStatus(payload.status);
    };
  };

  return (
    <PageShell title="Content Creator Studio">
      <form onSubmit={submit} className="grid md:grid-cols-2 gap-4">
        <input className="bg-black/30 p-3 rounded-xl" placeholder="Project ID" value={form.project_id} onChange={(e) => setForm({ ...form, project_id: Number(e.target.value) })} />
        <input className="bg-black/30 p-3 rounded-xl" placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
        <input className="bg-black/30 p-3 rounded-xl" placeholder="Topic" value={form.topic} onChange={(e) => setForm({ ...form, topic: e.target.value })} />
        <input className="bg-black/30 p-3 rounded-xl" placeholder="Duration seconds" type="range" min={30} max={300} value={form.duration_seconds} onChange={(e) => setForm({ ...form, duration_seconds: Number(e.target.value) })} />
        <select className="bg-black/30 p-3 rounded-xl" value={form.voice_type} onChange={(e) => setForm({ ...form, voice_type: e.target.value })}><option>alloy</option><option>nova</option><option>orion</option></select>
        <button className="bg-aurora rounded-xl px-5 py-3">Generate</button>
      </form>
      <p>Job: {jobId ?? "-"} | Status: {status}</p>
      <div className="h-2 bg-white/10 rounded-full overflow-hidden"><div className="h-full bg-cyanlux" style={{ width: status === "completed" ? "100%" : "40%" }} /></div>
    </PageShell>
  );
}
