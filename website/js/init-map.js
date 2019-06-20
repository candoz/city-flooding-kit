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
   /* //definizione dei markers di default con relativo popup
    var marker1 = L.marker([44.1247, 12.3966], {clickable: false});
    var marker2 = L.marker([44.1161, 12.3867]).bindPopup('<b>Marker2</b>:<br>Università di Perugia');
    var marker3 = L.marker([43.1021, 12.3893]).bindPopup('<b>Marker3</b>:<br>Parco Sant\'Anna');
    
    //aggiunta marker nella mappa
    marker1.addTo(map);
    marker2.addTo(map);
    marker3.addTo(map);**/

}).then(function(responseData){
    console.log("ehiii  "+ responseData);

}).catch(error => console.error(error))

// var http = new XMLHttpRequest();
// var url = 'https://54q6hpps8a.execute-api.us-east-2.amazonaws.com/prod/manager';
// http.open('POST', url, true);
// http.setRequestHeader('Content-type', 'application/json');

// http.onreadystatechange = function() {
//     if (http.readyState == XMLHttpRequest.DONE) {
//         console.log("Helloooooo")
//         console.log(http.responseType);
//     }
// }
// http.send(JSON.stringify({ "operation": "echo", "payload": { "TableName": "Kits" } }))

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