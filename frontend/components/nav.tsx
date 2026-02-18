import Link from "next/link";

const items = ["pricing", "dashboard", "studio", "team", "billing", "admin"];

export function Nav() {
  return (
    <nav className="flex gap-4 text-sm text-white/80">
      {items.map((item) => (
        <Link key={item} href={`/${item}`} className="hover:text-white transition">
          {item.toUpperCase()}
        </Link>
      ))}
    </nav>
  );
}
