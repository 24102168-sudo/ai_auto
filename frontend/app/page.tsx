"use client";
import Link from "next/link";
import { PageShell } from "@/components/page-shell";

export default function LandingPage() {
  return (
    <PageShell title="AI Content Operating System for Scalable Creators & Agencies">
      <p className="text-white/70 max-w-3xl">AURORA CORE brings multi-tenant governance, premium creator workflows, and AI video pipelines into one cloud-native SaaS platform.</p>
      <div className="flex gap-4">
        <Link href="/register" className="px-5 py-2 rounded-xl bg-aurora">Start Free Trial</Link>
        <Link href="/pricing" className="px-5 py-2 rounded-xl border border-white/20">Pricing</Link>
      </div>
    </PageShell>
  );
}
