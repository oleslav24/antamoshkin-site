// Fail closed until a separately authenticated VPS API and durable registry are connected.
export async function onRequestGet() {
  return Response.json({mode:"preview",devices:[],backendConnected:false}, {headers:{"Cache-Control":"no-store"}});
}
