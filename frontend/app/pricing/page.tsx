import { PageShell } from "@/components/page-shell";

const plans = [
  { name: "Starter", limit: "30 jobs/mo" },
  { name: "Pro", limit: "200 jobs/mo" },
  { name: "Agency", limit: "5000 jobs/mo" }
];

export default function PricingPage() {
  return (
    <PageShell title="Pricing">
      <div className="grid md:grid-cols-3 gap-4">
        {plans.map((p) => (
          <article key={p.name} className="glass p-5">
            <h3 className="text-xl">{p.name}</h3>
            <p className="text-white/60">{p.limit}</p>
          </article>
        ))}
      </div>
    </PageShell>
  );
}
