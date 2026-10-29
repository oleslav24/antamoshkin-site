// Metadata-only staging registry. The shared admin password is NOT friend-facing authentication.
const headers={"Cache-Control":"no-store","Content-Type":"application/json"};
const respond=(value,status=200)=>new Response(JSON.stringify(value),{status,headers});
const validOrigin=request=>{const u=new URL(request.url);return request.headers.get("Origin")===u.origin;};
export async function onRequestGet({env}) {
  if (!env.VPN_DB) return respond({error:"database_not_configured"},503);
  const {results}=await env.VPN_DB.prepare("SELECT id,label,protocol,state,created_at FROM vpn_devices ORDER BY created_at DESC LIMIT 50").all();
  return respond({mode:"metadata-only",backendConnected:false,devices:results});
}
export async function onRequestPost({request,env}) {
  if (!validOrigin(request)) return respond({error:"invalid_origin"},403);
  if (!env.VPN_DB) return respond({error:"database_not_configured"},503);
  if (!request.headers.get("content-type")?.startsWith("application/json")) return respond({error:"invalid_type"},415);
  let body;try{body=await request.json();}catch{return respond({error:"invalid_json"},400);}
  const label=typeof body.label==="string"?body.label.trim():"";
  if(label.length<1||label.length>64||!["xray","awg"].includes(body.protocol))return respond({error:"invalid_input"},400);
  const n=await env.VPN_DB.prepare("SELECT COUNT(*) n FROM vpn_devices").first();
  if(Number(n.n)>=30)return respond({error:"device_limit"},409);
  const id=crypto.randomUUID(),created_at=new Date().toISOString();
  await env.VPN_DB.prepare("INSERT INTO vpn_devices(id,label,protocol,state,created_at) VALUES (?,?,?,'draft',?)").bind(id,label,body.protocol,created_at).run();
  return respond({id,label,protocol:body.protocol,state:"draft",created_at},201);
}
