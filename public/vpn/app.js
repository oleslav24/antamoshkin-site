(async () => {
 const status=document.querySelector("#connection");
 const devices=document.querySelector("#devices");
 try {
   const response=await fetch("/api/vpn/devices",{cache:"no-store"});
   if(response.status===401){location.replace("/vpn/login.html");return;}
   if(!response.ok) throw new Error("Сервис недоступен");
   const data=await response.json();
   status.textContent=data.backendConnected?"Связь с сервером установлена":"Тестовый режим: выдача конфигураций пока отключена";
   devices.textContent=data.devices.length? "Записи будут доступны после подключения персонального реестра.":"Здесь появятся ваши устройства после подключения сервера.";
 } catch(e){status.textContent=e.message;devices.textContent="Нет данных";}
})();
document.querySelector("#logout").addEventListener("click",async()=>{await fetch("/api/vpn/logout",{method:"POST"});location.replace("/vpn/login.html");});
document.querySelector("#create").addEventListener("submit",e=>e.preventDefault());
