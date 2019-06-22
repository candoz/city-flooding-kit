var urlParams = new URLSearchParams(window.location.search)
var kitId = urlParams.get("kitId").split("-").join(" ").toUpperCase()

window.onload = () => {
    document.getElementById("nameKit").innerHTML = kitId
}
