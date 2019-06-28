from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import json as JSON
import serial
import random, time, datetime

# A random programmatic shadow client ID.
SHADOW_CLIENT = "AlarmStation"

# The unique hostname that &IoT; generated for 
# this device.
HOST_NAME = "azhkicv1gj9gc-ats.iot.us-east-2.amazonaws.com"

# The relative path to the correct root CA file for &IoT;, 
# which you have already saved onto this device.
ROOT_CA = "../../certs/alarm-station/AmazonRootCA1.pem" 

# The relative path to your private key file that 
# &IoT; generated for this device, which you 
# have already saved onto this device.
PRIVATE_KEY = "../../certs/alarm-station/e2360f5815-private.pem.key"

# The relative path to your certificate file that 
# &IoT; generated for this device, which you 
# have already saved onto this device.
CERT_FILE = "../../certs/alarm-station/e2360f5815-certificate.pem.crt"

# A programmatic shadow handler name prefix.
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
    
    if(alarm=="on"):
        arduino.write(str.encode("N"))

def updateCustomCallback(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("time out!")
    if responseStatus == "accepted":
        print("accepted")
    if responseStatus == "rejected":
        print("rejected!")     
# Keep generating random test data until this script 
# stops running.
# To stop running this script, press Ctrl+C.
while True:
  myDeviceShadow.shadowGet(myCustomCallback, 1)
  data = arduino.read()
  
  if str(data)=="b'F'":
    now = datetime.datetime.now()  # Store current datetime
    now_str = now.isoformat()  # Convert to ISO 8601 string
    JSONPayload = '{"state":{"desired":{"alarm":"off", "alarmTime":"'+now_str+'", "alarmReason":"" }}}'
    myDeviceShadow.shadowUpdate(JSONPayload, updateCustomCallback, 5)

  time.sleep(8)
