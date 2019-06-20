const map = L.map('map',{ center: [44.3239, 10.590], zoom: 8})
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { attribution: ':copyright: OpenStreetMap' }).addTo(map)

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
        const kitId = element.kitId
        const namePopup = kitId.split("-").join(" ").toUpperCase();
        
        var marker = L.marker([lat, lon]);
        marker.on('click',function (e) {
            window.location.href = "./sensorForKit.html?kitId="+kitId;
        });

        marker.on('mouseover', function (e) {
            this.openPopup();
        });
        marker.on('mouseout', function (e) {
            this.closePopup();
        });

        const title = "<p align='center'>"+namePopup+"</p> <p align='center'>latitude:"+ lat + " longitude:"+ lon+"</p>"; 
        marker.bindPopup(title).addTo(map);
    });
    

}).catch(error => console.error(error))
