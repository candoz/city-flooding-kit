setInterval( () => {
    const IOT_BROKER_ENDPOINT = "azhkicv1gj9gc-ats.iot.us-east-2.amazonaws.com" // also called the REST API endpoint
    const IOT_BROKER_REGION = "us-east-2"
    const IOT_THING_NAME = "AlarmStation"
    const POOL_ID = "us-east-2:ced405e2-0c87-4692-8279-ff909e664aa1"

    AWS.config.region = IOT_BROKER_REGION;
    AWS.config.credentials = new AWS.CognitoIdentityCredentials({ "IdentityPoolId": POOL_ID })

    const iotData = new AWS.IotData({ "endpoint": IOT_BROKER_ENDPOINT })
    const paramsGet = { "thingName": IOT_THING_NAME }


    iotData.getThingShadow(paramsGet, function (err, data) {
        if (err) {
            console.log("Error while trying to get AlarmStation shadow: " + err, err.stack)
            return "errore"
        } else {
            const payload = JSON.parse(data.payload)
            const alarm = payload.state.desired.alarm
            var alarmTime = JSON.stringify(payload.state.desired.alarmTime).replace("T"," ")
            var text_alarm = "Reason: "+ payload.state.desired.alarmReason+ " <br /> Timestamp: "+alarmTime
            document.getElementById("snackbar").innerHTML= text_alarm
            if(alarm =="on"){
                window.document.getElementById("inconAlarm").style="color: red;"
            }else{
                window.document.getElementById("inconAlarm").style="color: black;"
            }
            console.log(alarm)
            return data.payload
        }
    })
} , 2000)