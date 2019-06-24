var urlParams = new URLSearchParams(window.location.search)
var kitId = urlParams.get("kitId")

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
    return response.json()

}).then(responseData => {
    responseData.Items.forEach(element => {
        const humidity = "value: "+element.humidity
        const pressure = "value: "+element.pressure
        const proximity = "value: "+element.proximity
        const temperature = "value: "+element.temperature
        const timestamp = "timestamp: "+element.measureTime

        document.getElementById("history").innerHTML = '<h6>'+cells+'<\/h6>'
    });
    timestamp = timestamp.replace("T"," ")

    document.getElementById("value-pressure").innerHTML = pressure
    document.getElementById("value-humidity").innerHTML = humidity
    document.getElementById("value-proximity").innerHTML = proximity
    document.getElementById("value-temperature").innerHTML = temperature
    document.getElementById("value-data").innerHTML = timestamp    

}).catch(error => console.error(error))
