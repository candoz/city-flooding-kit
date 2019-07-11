var urlParams = new URLSearchParams(window.location.search)

window.onload = () => {
    document.getElementById("nameKit").innerHTML = urlParams.get("kitId").split("-").join(" ").toUpperCase()
}
