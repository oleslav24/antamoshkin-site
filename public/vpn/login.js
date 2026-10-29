document.querySelector("#login").addEventListener("submit", async (event) => {
 event.preventDefault();
 const message=document.querySelector("#message");
 const button=event.target.querySelector("button");
 button.disabled=true; message.textContent="Проверяем доступ…";
 try {
   const response=await fetch("/api/vpn/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({password:document.querySelector("#password").value}),cache:"no-store"});
   if (!response.ok) throw new Error(response.status===503?"Раздел ещё не настроен":"Неверный пароль");
   location.replace("/vpn/");
 } catch(e){message.textContent=e.message;button.disabled=false;}
});