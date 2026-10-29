export async function onRequestPost() {
  return Response.json({ok:true},{headers:{"Set-Cookie":"vpn_session=; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=0","Cache-Control":"no-store"}});
}
