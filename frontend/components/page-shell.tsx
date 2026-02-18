"use client";

import { motion } from "framer-motion";
import { ReactNode } from "react";
import { Nav } from "@/components/nav";

export function PageShell({ title, children }: { title: string; children: ReactNode }) {
  return (
    <main className="min-h-screen p-8 md:p-12 bg-gradient-to-br from-night via-[#101020] to-[#0a1320]">
      <div className="max-w-6xl mx-auto space-y-8">
        <header className="flex justify-between items-center">
          <h1 className="text-xl tracking-[0.2em]">AURORA CORE</h1>
          <Nav />
        </header>
        <motion.section initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="glass p-8 shadow-glow space-y-4">
          <h2 className="text-3xl font-semibold">{title}</h2>
          {children}
        </motion.section>
      </div>
    </main>
  );
}
