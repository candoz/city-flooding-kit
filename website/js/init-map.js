console.log("create map");
// Create variable to hold map element, give initial settings to map
 const map = L.map('map',{ center: [44.3239, 10.590], zoom: 8});
    
 // Add OpenStreetMap tile layer to map element
 L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap' }).addTo(map); 
 console.log("post method");
 
 fetch("https://ex1pp3jj9g.execute-api.us-east-1.amazonaws.com/prod/manager", {
    "method": "POST",
    "body":  
        {
        "operation": "list",
        "payload": {
            "TableName": "Kits"
        }
    }
}).then(function(response) {
    return response.json();
}).then(function(myJson) {
    console.log(JSON.stringify(myJson));
}).catch(error => console.error(error));;
 
    
    // do something with myJson
  
 /*
 //definizione dei markers di default con relativo popup
 var marker1 = L.marker([44.1247, 12.3966], {clickable: false});
 var marker2 = L.marker([44.1161, 12.3867]).bindPopup('<b>Marker2</b>:<br>Università di Perugia');
 var marker3 = L.marker([43.1021, 12.3893]).bindPopup('<b>Marker3</b>:<br>Parco Sant\'Anna');
 
 //aggiunta marker nella mappa
 marker1.addTo(map);
 marker2.addTo(map);
 marker3.addTo(map);*/