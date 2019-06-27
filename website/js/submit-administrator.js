function mySubmit() {
    
   var kitUser = String(document.getElementById('kitUser').value);
   var latitude = parseFloat(""+document.getElementById("lat").value);
   var longitude = parseFloat(""+document.getElementById("long").value);

    fetch("https://54q6hpps8a.execute-api.us-east-2.amazonaws.com/prod/manager", {
        "method": "POST",
        "body": JSON.stringify(
        {
            "operation": "create",
            "payload": {
                "TableName": "Kits",
                "Item":{
                    "kitId": kitUser,
                    "latitude": latitude,
                    "longitude": longitude
                }
            }
        })
        }).then(response => {
            return response.json()

        }).then(responseData => {
            document.getElementById("kitUser").value=""
            document.getElementById("lat").value=""
            document.getElementById("long").value=""  
            fetch("https://54q6hpps8a.execute-api.us-east-2.amazonaws.com/prod/manager", {
                "method": "POST",
                "body": JSON.stringify(
                {
                    "operation": "new",
                    "payload": { 
    	                "AttributeDefinitions": 
    	                [{
    		                "AttributeName": "itemId",
    		                "AttributeType": "S"
    	                }],
		                "KeySchema": [{
    		                "AttributeName": "itemId",
    		                "KeyType": "HASH"
		                }],
		            "TableName": kitUser,
		            "BillingMode": "PAY_PER_REQUEST"
                    }   
                })
                }).then(response => {
                    window.alert("Kit added.")
                    return true;
        
                }).catch(error => console.error(error))
                
            
            

        }).catch(error => console.error(error))
        

   
       
    }
    