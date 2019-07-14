setInterval( () => {
    const IOT_BROKER_ENDPOINT = "azhkicv1gj9gc-ats.iot.us-east-2.amazonaws.com" // also called the REST API endpoint
    const IOT_BROKER_REGION = "us-east-2"
    const IOT_THING_NAME = "AlarmStation"
    const POOL_ID = "us-east-2:ced405e2-0c87-4692-8279-ff909e664aa1"

    AWS.config.region = IOT_BROKER_REGION;
    AWS.config.credentials = new AWS.CognitoIdentityCredentials({ "IdentityPoolId": POOL_ID })

    const iotData = new AWS.IotData({ "endpoint": IOT_BROKER_ENDPOINT })
    const paramsGet = { "thingName": IOT_THING_NAME }

    getCurrentValue()

    iotData.getThingShadow(paramsGet, function (err, data) {
        if (err) {
            console.log("Error while trying to get AlarmStation shadow: " + err, err.stack)
            return "errore"
        } else {
            const payload = JSON.parse(data.payload)
            const alarm = payload.state.desired.alarm
            var alarmTime = new Date(payload.state.desired.alarmTime*1000).toLocaleString()
            var text_alarm = "Reason: "+ payload.state.desired.alarmReason+ " <br /> Timestamp: "+alarmTime
            if(alarm =="on"){
                document.getElementById("snackbar").innerHTML= text_alarm
                window.document.getElementById("inconAlarm").style="color: red;"
            }else{
                document.getElementById("snackbar").innerHTML= "No alarm"
                window.document.getElementById("inconAlarm").style="color: black;"
            }
            console.log(alarm)
            return data.payload
        }
    })
} , 2000)

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