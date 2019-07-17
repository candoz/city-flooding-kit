from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import json as JSON
import serial
import random, time, datetime

SHADOW_CLIENT = "AlarmStation"
HOST_NAME = "azhkicv1gj9gc-ats.iot.us-east-2.amazonaws.com"
ROOT_CA = "../../certs/alarm-station/AmazonRootCA1.pem"
PRIVATE_KEY = "../../certs/alarm-station/e2360f5815-private.pem.key"
CERT_FILE = "../../certs/alarm-station/e2360f5815-certificate.pem.crt"

SHADOW_HANDLER = "AlarmStation"

arduino = serial.Serial('COM3',9600)

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(SHADOW_HANDLER, True)

def myCustomCallback(payload, responseStatus, token):
    alarm= JSON.loads(str(payload))["state"]["desired"]["alarm"]
    print("alarmm  "+ alarm)
    if(alarm=="on"):
        print("on")
        arduino.write(str.encode("T"))
            
    data = arduino.read()

    if str(data)== "b'F'":
        now = datetime.datetime.now()
        now_str = now.isoformat()  # Convert to ISO 8601 string
        JSONPayload = '{"state":{"desired":{"alarm":"off", "alarmTime":"'+now_str+'", "alarmReason":"" }}}'
        myDeviceShadow.shadowUpdate(JSONPayload, updateCustomCallback, 5)
    

def updateCustomCallback(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("time out!")
    if responseStatus == "accepted":
        print("accepted")
    if responseStatus == "rejected":
        print("rejected!")

while True:
    myDeviceShadow.shadowGet(myCustomCallback, 1)
    
    time.sleep(4)
