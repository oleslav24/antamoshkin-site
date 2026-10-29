const encoder = new TextEncoder();
const b64 = bytes => btoa(String.fromCharCode(...bytes)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
async function digest(s) { return new Uint8Array(await crypto.subtle.digest("SHA-256", encoder.encode(s))); }
async function sign(secret, payload) {
  const key = await crypto.subtle.importKey("raw", encoder.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return b64(new Uint8Array(await crypto.subtle.sign("HMAC", key, encoder.encode(payload))));
}
export async function onRequestPost({request,env}) {
  if (!env.VPN_PORTAL_PASSWORD || env.VPN_PORTAL_PASSWORD.length < 24) return new Response("Not configured", {status:503});
  if (!request.headers.get("content-type")?.includes("application/json")) return Response.json({error:"invalid_request"}, {status:400});
  let data; try { data = await request.json(); } catch { return Response.json({error:"invalid_request"},{status:400}); }
  if (typeof data.password !== "string" || data.password.length > 512) return Response.json({error:"invalid_credentials"},{status:401});
  const a=await digest(data.password), b=await digest(env.VPN_PORTAL_PASSWORD);
  const valid = a.reduce((d,x,i)=>d | (x ^ b[i]), 0) === 0;
  if (!valid) return Response.json({error:"invalid_credentials"},{status:401,headers:{"Cache-Control":"no-store"}});
  const expiry = String(Date.now()+3600000);
  const token = expiry+"."+(await sign(env.VPN_PORTAL_PASSWORD,expiry));
  return Response.json({ok:true},{headers:{"Set-Cookie":`vpn_session=${token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=3600`,"Cache-Control":"no-store"}});
}
