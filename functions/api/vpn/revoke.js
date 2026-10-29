// Revoke an existing Xray device; fail closed if upstream outcome is uncertain.
const headers={"Cache-Control":"no-store","Content-Type":"application/json","X-Content-Type-Options":"nosniff"};
const respond=(value,status=200)=>new Response(JSON.stringify(value),{status,headers});
export async function onRequestPost({request,env}) {
  if(request.headers.get("Origin")!==new URL(request.url).origin)return respond({error:"invalid_origin"},403);
  if(!request.headers.get("content-type")?.startsWith("application/json"))return respond({error:"invalid_type"},415);
  if(!env.VPN_DB)return respond({error:"database_not_configured"},503);
  if(!env.VPN_PROVISION_URL||!env.VPN_PROVISION_TOKEN||!env.CF_ACCESS_CLIENT_ID||!env.CF_ACCESS_CLIENT_SECRET)return respond({error:"provisioning_not_enabled"},503);
  let body;try{body=await request.json();}catch{return respond({error:"invalid_json"},400);}
  const id=body?.id;
  if(typeof id!=="string"||!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(id)||body.confirmation!=="REVOKE")return respond({error:"invalid_request"},400);
  const device=await env.VPN_DB.prepare("SELECT id,label,protocol,state FROM vpn_devices WHERE id=?").bind(id).first();
  if(!device)return respond({error:"not_found"},404);
  if(device.protocol!=="xray"||!["active","revoked"].includes(device.state))return respond({error:"not_revocable"},409);
  const attempt=await env.VPN_DB.prepare("SELECT state FROM vpn_provision_attempts WHERE device_id=?").bind(id).first();
  if(!attempt||attempt.state!=="completed")return respond({error:"unreconciled_device"},409);
  let upstream;
  try {
    upstream=await fetch(env.VPN_PROVISION_URL.replace(/\/$/,"")+"/v1/xray/revoke",{
      method:"POST",
      headers:{"Authorization":"Bearer "+env.VPN_PROVISION_TOKEN,"Content-Type":"application/json","Idempotency-Key":id,"CF-Access-Client-Id":env.CF_ACCESS_CLIENT_ID,"CF-Access-Client-Secret":env.CF_ACCESS_CLIENT_SECRET},
      body:JSON.stringify({id,confirmation:"REVOKE"}),signal:AbortSignal.timeout(90000)
    });
  }catch{return respond({error:"outcome_uncertain",message:"Check VPS journal before retrying."},502);}
  if(!upstream.ok)return respond({error:"upstream_revoke_failed",message:"Check VPS journal; do not issue a replacement yet."},502);
  let result;try{result=await upstream.json();}catch{return respond({error:"invalid_upstream_response"},502);}
  if(result?.device_id!==id||result?.state!=="revoked")return respond({error:"invalid_upstream_response"},502);
  await env.VPN_DB.prepare("UPDATE vpn_devices SET state='revoked' WHERE id=? AND state IN ('active','revoked')").bind(id).run();
  return respond({id,state:"revoked"});
}
