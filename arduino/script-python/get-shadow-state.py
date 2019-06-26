from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import random, time, json

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

# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
  print()
  print('UPDATE: $aws/things/' + SHADOW_HANDLER + 
    '/shadow/update/#')
  print("payload = " + payload)
  print("responseStatus = " + responseStatus)
  print("token = " + token)

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY,
  CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(
  SHADOW_HANDLER, True)


def myCustomCallback(payload, responseStatus, token):
    shadow_data = json.loads(payload.read().decode())

    print(shadow_data)
# Keep generating random test data until this script 
# stops running.
# To stop running this script, press Ctrl+C.
while True:
    myDeviceShadow.shadowGet(myCustomCallback, 1)
    time.sleep(8)
    
 


