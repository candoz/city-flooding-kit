
fetch("https://azhkicv1gj9gc-ats.iot.us-east-2.amazonaws.com/things/AlarmStation/shadow", {
    "method": "GET",
    "headers" : {
       "Authorization": "AWS AKIAJ47MY3YPY4CDUJ6Q:lwWgRSqimXBm7anAS025RFk9NaQrSzgprTTFqgQJ="
    }
}).then(response => {
console.log("Dentro la response")
    return response.json();
  
}).then(responseData => {
    console.log(responseData)

}).catch(error => console.error(error))