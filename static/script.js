function openLogin(role){
 const modal=document.getElementById("loginModal");
 const form=document.getElementById("loginForm");
 document.getElementById("loginTitle").textContent =
   role==="farmer" ? "👨‍🌾 Farmer Login" : "🧑‍💼 Admin Login";
 form.action="/login/"+role;
 modal.style.display="flex";
}
function closeLogin(){document.getElementById("loginModal").style.display="none"}
window.onclick=function(e){if(e.target===document.getElementById("loginModal"))closeLogin()}
