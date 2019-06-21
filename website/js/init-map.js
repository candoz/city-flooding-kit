const DEFAULT_LAT = 44.3239
const DEFAULT_LON = 10.590
const DEFAULT_ZOOM = 8

const KITS_TABLENAME = "Kits"

const map = L.map('map',{ center: [DEFAULT_LAT, DEFAULT_LON], zoom: DEFAULT_ZOOM})
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { attribution: ':copyright: OpenStreetMap' }).addTo(map)

fetch("https://54q6hpps8a.execute-api.us-east-2.amazonaws.com/prod/manager", {
    "method": "POST",
    "body": JSON.stringify(
        {
            "operation": "list",
            "payload": {
                "TableName": KITS_TABLENAME
            }
        }
    )

}).then(response => {
    console.log("Dentro la response")
    return response.json()

}).then(responseData => {
    const markers = []
    responseData.Items.forEach(element => {
        const lat = element.latitude
        const lon = element.longitude
        const kitId = element.kitId
        const namePopup = kitId.split("-").join(" ").toUpperCase()
        const marker = L.marker([lat, lon])

        marker.on('click', function(_) {
           window.location.href = "./sensor-kit.html?kitId=" + kitId
        })
        marker.on('mouseover', function(_) {
            this.openPopup()
        })
        marker.on('mouseout', function(_) {
            this.closePopup()
        })
        const title = "<p align='center'>" + namePopup + "</p> <p align='center'>latitude:" + lat + " longitude:" + lon + "</p>"; 
        marker.bindPopup(title).addTo(map)
        markers.push(marker)
    })
    return markers

}).then(markers => {
    const group = new L.featureGroup(markers)
    map.fitBounds(group.getBounds().pad(0.5))

}).catch(error => console.error(error))
