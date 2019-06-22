// import AWS from 'aws-sdk/global'
// import AWSMqttClient from 'aws-mqtt'

AWS.config.region = 'us-east-2'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-east-2:c3a218d8-1a75-421f-a3a2-21f77683cf25',
});

const client = new AWSMqttClient({
    region: AWS.config.region,
    credentials: AWS.config.credentials,
    endpoint: 'azhkicv1gj9gc-ats.iot.us-east-2.amazonaws.com', // NOTE: get this value with `aws iot describe-endpoint`
    expires: 600, // Sign url with expiration of 600 seconds
    clientId: 'mqtt-client-' + (Math.floor((Math.random() * 100000) + 1)), // clientId to register with MQTT broker. Need to be unique per client
    will: {
        topic: 'WillMsg',
        payload: 'Connection Closed abnormally..!',
        qos: 0,
        retain: false
    } 
})

client.on('connect', () => {
    client.subscribe('flooding-kit/ponte-vecchio-kit')
})

client.on('message', (topic, message) => {
    console.log(topic, message)
})

client.on('close', () => {
    // ...
})

client.on('offline', () => {
    // ...
})
