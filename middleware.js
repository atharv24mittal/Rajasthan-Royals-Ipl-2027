// Vercel Routing Middleware: server-side HTTP Basic auth. A client-side password would NOT be secure.
// FAILS CLOSED: if DASHBOARD_USER / DASHBOARD_PASS are missing the site returns 503, unless ACCESS_MODE=open is set explicitly.
import { next } from "@vercel/functions";
export const config = { matcher: ["/((?!favicon.ico).*)"] };
const te = new TextEncoder();
function safeEqual(a, b) { const x = te.encode(a), y = te.encode(b); let d = x.length ^ y.length; for (let i = 0; i < Math.max(x.length, y.length); i++) d |= (x[i] || 0) ^ (y[i] || 0); return d === 0; }
export default function middleware(request) {
  const u = process.env.DASHBOARD_USER, p = process.env.DASHBOARD_PASS;
  const hdr = { "X-Robots-Tag": "noindex, nofollow", "Cache-Control": "private, no-store" };
  if (!u || !p) return process.env.ACCESS_MODE === "open" ? next() : new Response("Dashboard locked: credentials not configured.", { status: 503, headers: hdr });
  const h = request.headers.get("authorization") || "";
  if (h.startsWith("Basic ")) {
    try { const raw = atob(h.slice(6)), i = raw.indexOf(":"); if (i > -1 && safeEqual(raw.slice(0, i), u) && safeEqual(raw.slice(i + 1), p)) return next({ headers: hdr }); } catch (e) {}
  }
  return new Response("Authentication required", { status: 401, headers: { ...hdr, "WWW-Authenticate": 'Basic realm="SUPERR INTELLIGENCE", charset="UTF-8"' } });
}
