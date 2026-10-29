// Real provisioning is deliberately disabled: no VPS credentials or config material in Pages.
export async function onRequestPost() {
  return Response.json({error:"provisioning_not_enabled",message:"The VPS provisioning API has not been connected."}, {status:503,headers:{"Cache-Control":"no-store"}});
}
