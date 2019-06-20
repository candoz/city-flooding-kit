var urlParams = new URLSearchParams(window.location.search);
let kitId = urlParams.get("kitId");
kitId = kitId.split("-").join(" ").toUpperCase();

window.onload = function() {
  document.getElementById("nameKit").innerHTML=kitId;
} 