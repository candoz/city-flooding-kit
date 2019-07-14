function getCurrentValue(){
    var urlParams = new URLSearchParams(window.location.search)
    var kitId = urlParams.get("kitId")
    var sortedItems = new Array()

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
        responseData.Items.forEach(element => {
            sortedItems.push({"humidity":element['humidity'],"pressure":element['pressure'],"proximity":element['proximity'],"temperature":element['temperature'], "timestamp": element.measureTime*1000})
        });
        sortedItems.sort((a, b) => (a.timestamp < b.timestamp) ? 1 : -1)
        const currentElement = sortedItems[0]
        if (currentElement != undefined) {
            const humidity = currentElement.humidity+" %"
            const pressure = currentElement.pressure+" mPa"
            const proximity = currentElement.proximity+" cm"
            const temperature = currentElement.temperature+ "°C"
            var raining=""
            if(currentElement.raining){
                raining = "YES"
            }else{
                raining= "NO"
            }
                
            var time = new Date(currentElement.timestamp).toLocaleString()
            
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
            document.getElementById("value-raining").innerHTML = NOT_AVAILABLE_STR
        }

    }).catch(error => console.error(error))

}

module.exports = getCurrentValue;