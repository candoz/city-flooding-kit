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
        const humidity = element.humidity+" %"
        const pressure = element.pressure+" mPa"
        const proximity = element.proximity+" cm"
        const temperature = element.temperature+ "°C"
        var raining=""
        console.log(element.raining)
        if(element.raining){
            raining = "YES"
        }else{
            raining= "NO"
        }
            
        var time = new Date(element.measureTime*1000).toLocaleString()
        
        document.getElementById("value-pressure").innerHTML = pressure
        document.getElementById("value-humidity").innerHTML = humidity
        document.getElementById("value-proximity").innerHTML = proximity
        document.getElementById("value-temperature").innerHTML = temperature
        document.getElementById("value-data").innerHTML = time
        document.getElementById("value-raining").innerHTML = raining
    } else {
        document.getElementById("value-pressure").innerHTML = NOT_AVAILABLE_STR
        document.getElementById("value-humidity").innerHTML = NOT_AVAILABLE_STR
        document.getElementById("value-proximity").innerHTML = NOT_AVAILABLE_STR
        document.getElementById("value-temperature").innerHTML = NOT_AVAILABLE_STR
        document.getElementById("value-rain").innerHTML = NOT_AVAILABLE_STR
    }

}).catch(error => console.error(error))
