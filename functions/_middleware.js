// Protect VPN pages and API with a short-lived signed session.
// Set VPN_PORTAL_PASSWORD as a Cloudflare Pages secret, not in Git.
const enc = new TextEncoder();
const b64 = bytes => btoa(String.fromCharCode(...bytes)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
async function hmac(secret, value) {
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return b64(new Uint8Array(await crypto.subtle.sign("HMAC", key, enc.encode(value))));
}
export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  if (!url.pathname.startsWith("/vpn/") && !url.pathname.startsWith("/api/vpn/")) return context.next();
  const secret = env.VPN_PORTAL_PASSWORD;
  if (!secret || secret.length < 24) return new Response("VPN portal is not configured", { status: 503, headers: { "Cache-Control": "no-store" } });
  if (url.pathname === "/vpn/login.html" || url.pathname === "/api/vpn/login") return context.next();
  const raw = (request.headers.get("Cookie") || "").split(";").map(s => s.trim()).find(s => s.startsWith("vpn_session="))?.slice(12);
  let authenticated = false;
  if (raw) {
    const [expiry, sig] = raw.split(".");
    if (/^\d{10,13}$/.test(expiry || "") && Number(expiry) > Date.now() && Number(expiry) < Date.now() + 86400000 && sig) {
      const expected = await hmac(secret, expiry);
      const a = enc.encode(expected), b = enc.encode(sig);
      authenticated = a.length === b.length && a.reduce((diff, x, i) => diff | (x ^ b[i]), 0) === 0;
    }
  }
  if (!authenticated) {
    if (url.pathname.startsWith("/api/")) return Response.json({ error: "unauthorized" }, { status: 401, headers: { "Cache-Control": "no-store" } });
    return Response.redirect(new URL("/vpn/login.html", request.url), 302);
  }
  const response = await context.next();
  const headers = new Headers(response.headers);
  headers.set("Cache-Control", "no-store");
  headers.set("X-Robots-Tag", "noindex, nofollow");
  return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
}
export { hmac };
