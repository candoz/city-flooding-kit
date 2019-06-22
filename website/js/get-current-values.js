var urlParams = new URLSearchParams(window.location.search)
var kitId = urlParams.get("kitId")

const NOT_AVAILABLE_STR = "Not available"

fetch("https://54q6hpps8a.execute-api.us-east-2.amazonaws.com/prod/manager", {
    "method": "POST",
    "body": JSON.stringify(
        {
            "operation": "list",
            "payload": {
                "TableName": kitId
            }
        }
    )

}).then(response => {
    return response.json();
  
}).then(responseData => {
    const element = responseData.Items[0]
    if (element != undefined) {
        const humidity = "value: "+element.humidity
        const pressure = "value: "+element.pressure
        const proximity = "value: "+element.proximity
        const temperature = "value: "+element.temperature
        var timestamp = "timestamp: "+element.ciao
        timestamp = timestamp.replace("T"," ")
        
        document.getElementById("value-pressure").innerHTML = pressure
        document.getElementById("value-humidity").innerHTML = humidity
        document.getElementById("value-proximity").innerHTML = proximity
        document.getElementById("value-temperature").innerHTML = temperature
        document.getElementById("value-data").innerHTML = timestamp
    } else {
        document.getElementById("value-pressure").innerHTML = NOT_AVAILABLE_STR
        document.getElementById("value-humidity").innerHTML = NOT_AVAILABLE_STR
        document.getElementById("value-proximity").innerHTML = NOT_AVAILABLE_STR
        document.getElementById("value-temperature").innerHTML = NOT_AVAILABLE_STR
    }

}).catch(error => console.error(error))
