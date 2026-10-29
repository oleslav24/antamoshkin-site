let pendingProfile=null;
const el=s=>document.querySelector(s);
const status=message=>{el("#connection").textContent=message;};
async function refresh(){
 const devices=el("#devices");
 try{
  const r=await fetch("/api/vpn/devices",{cache:"no-store"});
  if(r.status===401){location.replace("/vpn/login.html");return;}
  const data=await r.json();
  if(!r.ok)throw new Error("Ошибка реестра устройств");
  if(!pendingProfile)status("Реестр подключён. Создание Xray-профилей доступно через кнопку «Выпустить .vpn».");
  el("#create button").disabled=false;
  devices.replaceChildren();
  if(!data.devices.length){devices.textContent="Устройств пока нет";return;}
  for(const device of data.devices){
   const p=document.createElement("p");
   const state=device.state==="draft"?"черновик":device.state==="active"?"активен":"отозван";
   p.append(document.createTextNode(device.label+" · "+(device.protocol==="xray"?"Xray":"AWG 3.1")+" · "+state+" "));
   if(["draft","active"].includes(device.state)&&device.protocol==="xray"){
    const b=document.createElement("button");b.textContent=device.state==="active"?"Скачать .vpn повторно":"Выпустить .vpn";
    b.addEventListener("click",()=>provision(device.id,b));p.append(b);
   }
   if(device.state==="active"&&device.protocol==="xray"){
     const revokeButton=document.createElement("button");
     revokeButton.textContent="Отозвать доступ";revokeButton.className="secondary";
     revokeButton.style.marginLeft="8px";
     revokeButton.addEventListener("click",()=>revokeDevice(device,revokeButton));
     p.append(revokeButton);
   }
   devices.append(p);
  }
 }catch(e){status(e.message);devices.textContent="Нет данных";}
}
async function revokeDevice(device,button){
 if(!confirm("Безвозвратно отозвать VPN-доступ устройства «"+device.label+"»? Существующий .vpn перестанет работать. Для нового доступа потребуется новый профиль."))return;
 button.disabled=true;
 status("Отзываем доступ на сервере…");
 try{
   const r=await fetch("/api/vpn/revoke",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({id:device.id,confirmation:"REVOKE"})});
   const response=await r.json();
   if(!r.ok)throw new Error(response.message||response.error||"Ошибка отзыва");
   await refresh();
   status("Доступ «"+device.label+"» отозван. Ранее выданный .vpn больше не должен проходить новую авторизацию.");
 }catch(e){status("Не удалось подтвердить отзыв: "+e.message);}
 finally{button.disabled=false;}
}
async function provision(id,button){
 if(!confirm("Получить нативный AmneziaVPN-файл? Для нового устройства будет создан пользователь Xray."))return;
 button.disabled=true;status("Отправляем запрос на выпуск профиля…");
 try{
  const r=await fetch("/api/vpn/create",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({id})});
  const data=await r.json();
  if(!r.ok)throw new Error(data.message||data.error||"Ошибка выпуска");
  pendingProfile={text:data.vpn,name:(data.label||"device").replace(/[^a-zA-Z0-9_-]/g,"_")+".vpn"};
  el("#download-panel").hidden=false;
  el("#save-profile").click();
  await refresh();
  status("Скачивание .vpn запущено. Если браузер его заблокировал, воспользуйтесь кнопкой «Скачать .vpn» ниже списка устройств.");
 }catch(e){status("Выпуск не выполнен: "+e.message);}
 finally{button.disabled=false;}
}
el("#save-profile").addEventListener("click",()=>{
 if(!pendingProfile)return;
 const blob=new Blob([pendingProfile.text+"\n"],{type:"text/plain;charset=utf-8"});
 const url=URL.createObjectURL(blob);
 const a=document.createElement("a");a.href=url;a.download=pendingProfile.name;a.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
});
el("#dismiss-profile").addEventListener("click",()=>{pendingProfile=null;el("#download-panel").hidden=true;});
el("#logout").addEventListener("click",async()=>{await fetch("/api/vpn/logout",{method:"POST"});location.replace("/vpn/login.html");});
el("#create").addEventListener("submit",async(e)=>{
 e.preventDefault();const button=e.target.querySelector("button");button.disabled=true;
 try{
  const r=await fetch("/api/vpn/devices",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({label:el("#device").value,protocol:el("#protocol").value})});
  if(!r.ok)throw new Error("Не удалось добавить устройство");
  e.target.reset();await refresh();
 }catch(err){status(err.message);}
 finally{button.disabled=false;}
});
refresh();
