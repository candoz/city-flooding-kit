function authentication() {
    
    var username = String(document.getElementById('username').value);
    var password = String(""+document.getElementById("psw").value);
    
    fetch("https://54q6hpps8a.execute-api.us-east-2.amazonaws.com/prod/manager", {
    "method": "POST",
    "body": JSON.stringify(
        {
            "operation": "list",
            "payload": {
                "TableName": "administrators"
            }
        }
    )

    }).then(response => {
        return response.json();
    
    }).then(responseData => {
        responseData.Items.forEach(element => {
        if(element.username == username && element.password == password){
                window.location.href = "add-new-kit.html";
        }else{
            window.alert("Wrong Credential.")
        }
        });

    }).catch(error => console.error(error))
 
}
     