console.log("create map")
const map = L.map('map',{ center: [44.3239, 10.590], zoom: 8})
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { attribution: ':copyright: OpenStreetMap' }).addTo(map)
console.log("post method")

fetch("https://54q6hpps8a.execute-api.us-east-2.amazonaws.com/prod/manager", {
    "method": "POST",
    "body": JSON.stringify(
        {
            "operation": "list",
            "payload": {
                "TableName": "Kits"
            }
        }
    )
}).then(function(response) {
console.log("Dentro la response")
    return response.json();
  
}).then(function(responseData){
    responseData.Items.forEach(element => {
        const lat = element.latitude
        const lon = element.longitude
        
        var marker = L.marker([lat, lon]);
        marker.on('click',function (e) {
            window.location.href = "./sensorForKit.html";
        });
        
        marker.on('mouseover', function (e) {marker
            this.openPopup();
        });
        marker.on('mouseout', function (e) {
            this.closePopup();
        });

        const title = "<p align='center'>"+element.kitId+"</p> <p align='center'>latitude:"+ lat + " longitude:"+ lon+"</p>"; 
        marker.bindPopup(title).addTo(map);
    });
    

}).catch(error => console.error(error))
