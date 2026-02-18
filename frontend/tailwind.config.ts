import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        night: "#0a0a12",
        aurora: "#8b5cf6",
        cyanlux: "#06b6d4"
      },
      boxShadow: {
        glow: "0 0 40px rgba(139, 92, 246, 0.35)"
      }
    }
  },
  plugins: []
} satisfies Config;
