function openNav(sensorType) {
    var history_txt =""
    var urlParams = new URLSearchParams(window.location.search)
    var kid = urlParams.get("kitId")
    fetch("https://54q6hpps8a.execute-api.us-east-2.amazonaws.com/prod/manager", {
        "method": "POST",
        "body": JSON.stringify(
            {
                "operation": "list",
                "payload": {
                    "TableName": kid
                }
            }
        )
    }

    ).then(response => {
        return response.json()
    
    }).then(responseData => {
    const type = sensorType.toString().toLowerCase()
    responseData.Items.forEach(element => {
        const value = "value: "+element[type]
        let time = "timestamp: "+element.ciao
        time = time.replace("T", " ")
        history_txt = history_txt+"<h5 align='left'>"+value+' &nbsp&nbsp '+time+'<\/h5>'
    });
    document.getElementById("myNav").style.width = "100%"
    document.getElementById("history").style.color = "white"
    document.getElementById("sensor-name").innerHTML = ""+sensorType+" History"
    document.getElementById("history").innerHTML = ""+history_txt
        
    }).catch(error => console.error(error))
}

function closeNav() {
  document.getElementById("myNav").style.width = "0%";
}
