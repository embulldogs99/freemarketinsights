

name=document.cookie.split(";")[0];
document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
window.location.replace("/html/home");
