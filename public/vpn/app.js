async function refresh(){
 const status=document.querySelector("#connection"),devices=document.querySelector("#devices");
 try{
   const r=await fetch("/api/vpn/devices",{cache:"no-store"});
   if(r.status===401){location.replace("/vpn/login.html");return;}
   const data=await r.json();
   if(!r.ok)throw new Error(data.error==="database_not_configured"?"Хранилище D1 пока не подключено":"Ошибка реестра устройств");
   status.textContent="Реестр подключён. Сейчас создаются только черновики, без VPN-доступа.";
   document.querySelector("#create button").disabled=false;
   devices.replaceChildren();
   if(!data.devices.length){devices.textContent="Устройств пока нет";return;}
   for(const device of data.devices){
     const p=document.createElement("p");
     p.textContent=device.label+" · "+(device.protocol==="xray"?"Xray":"AWG 3.1")+" · черновик";
     devices.append(p);
   }
 }catch(e){status.textContent=e.message;devices.textContent="Нет данных";}
}
document.querySelector("#logout").addEventListener("click",async()=>{await fetch("/api/vpn/logout",{method:"POST"});location.replace("/vpn/login.html");});
document.querySelector("#create").addEventListener("submit",async(e)=>{
 e.preventDefault();const button=e.target.querySelector("button");button.disabled=true;
 try{
   const r=await fetch("/api/vpn/devices",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({label:document.querySelector("#device").value,protocol:document.querySelector("#protocol").value})});
   if(!r.ok)throw new Error("Не удалось создать черновик");
   e.target.reset();await refresh();
 }catch(err){document.querySelector("#connection").textContent=err.message;}
 finally{button.disabled=false;}
});
refresh();
