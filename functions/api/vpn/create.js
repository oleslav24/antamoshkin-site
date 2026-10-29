// Authenticated admin-only provisioning bridge. Never log or persist private profiles in D1.
const headers={"Cache-Control":"no-store","Content-Type":"application/json","X-Content-Type-Options":"nosniff"};
const respond=(data,status=200)=>new Response(JSON.stringify(data),{status,headers});
export async function onRequestPost({request,env}) {
  const origin=new URL(request.url).origin;
  if(request.headers.get("Origin")!==origin)return respond({error:"invalid_origin"},403);
  if(!request.headers.get("content-type")?.startsWith("application/json"))return respond({error:"invalid_type"},415);
  if(!env.VPN_DB)return respond({error:"database_not_configured"},503);
  if(!env.VPN_PROVISION_URL||!env.VPN_PROVISION_TOKEN||!env.CF_ACCESS_CLIENT_ID||!env.CF_ACCESS_CLIENT_SECRET)return respond({error:"provisioning_not_enabled"},503);
  let data;try{data=await request.json();}catch{return respond({error:"invalid_json"},400);}
  const id=typeof data?.id==="string"?data.id:"";
  if(!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(id))return respond({error:"invalid_id"},400);
  const device=await env.VPN_DB.prepare("SELECT id,label,protocol,state FROM vpn_devices WHERE id=?").bind(id).first();
  if(!device)return respond({error:"not_found"},404);
  if(device.state!=="draft"||device.protocol!=="xray")return respond({error:"not_provisionable"},409);
  const lock=await env.VPN_DB.prepare("INSERT OR IGNORE INTO vpn_provision_attempts(device_id,created_at) VALUES(?,?)").bind(id,new Date().toISOString()).run();
  if(!lock.meta?.changes)return respond({error:"already_attempted",message:"Requires administrator reconciliation before retry."},409);
  let response;
  try {
    response=await fetch(env.VPN_PROVISION_URL.replace(/\/$/,"")+"/v1/xray/provision",{
      method:"POST",
      headers:{"Authorization":"Bearer "+env.VPN_PROVISION_TOKEN,"Content-Type":"application/json","Accept":"application/json","Idempotency-Key":id,"CF-Access-Client-Id":env.CF_ACCESS_CLIENT_ID,"CF-Access-Client-Secret":env.CF_ACCESS_CLIENT_SECRET},
      body:JSON.stringify({id,label:device.label}),
      signal:AbortSignal.timeout(25000)
    });
  } catch {
    await env.VPN_DB.prepare("UPDATE vpn_provision_attempts SET state='uncertain',error_code='upstream_unreachable' WHERE device_id=?").bind(id).run();
    return respond({error:"upstream_unreachable",message:"Provisioning outcome uncertain. Check the VPS before retry."},502);
  }
  if(!response.ok) {
    await env.VPN_DB.prepare("UPDATE vpn_provision_attempts SET state='failed',error_code=? WHERE device_id=?").bind("upstream_"+response.status,id).run();
    return respond({error:"upstream_failed",message:"Check VPS service; no automatic retry."},502);
  }
  let result;
  try{result=await response.json();}catch{return respond({error:"invalid_upstream_response"},502);}
  if(result?.device_id!==id || typeof result?.vpn!=="string" || !result.vpn.startsWith("vpn://") || result.vpn.length>20000) {
    await env.VPN_DB.prepare("UPDATE vpn_provision_attempts SET state='uncertain',error_code='invalid_response' WHERE device_id=?").bind(id).run();
    return respond({error:"invalid_upstream_response"},502);
  }
  const update=await env.VPN_DB.prepare("UPDATE vpn_devices SET state='active' WHERE id=? AND state='draft'").bind(id).run();
  if(!update.meta?.changes)return respond({error:"registry_conflict"},409);
  await env.VPN_DB.prepare("UPDATE vpn_provision_attempts SET state='completed',error_code=NULL WHERE device_id=?").bind(id).run();
  return respond({id,label:device.label,protocol:"xray",state:"active",vpn:result.vpn});
}
