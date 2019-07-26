import time
import datetime
import json as JSON
import serial
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

HOST_NAME = "azhkicv1gj9gc-ats.iot.us-east-2.amazonaws.com"
ROOT_CA = "../../certs/alarm-station/AmazonRootCA1.pem"
PRIVATE_KEY = "../../certs/alarm-station/e2360f5815-private.pem.key"
CERT_FILE = "../../certs/alarm-station/e2360f5815-certificate.pem.crt"

SHADOW_CLIENT = "AlarmStation"
SHADOW_HANDLER = "AlarmStation"
TIMEOUT_IN_SECONDS = 2
SECONDS_TO_SLEEP = 4

ARDUINO_SERIAL = serial.Serial('COM3', 9600)

# Create, configure, and connect a shadow client.
MY_SHADOW_CLIENT = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
MY_SHADOW_CLIENT.configureEndpoint(HOST_NAME, 8883)
MY_SHADOW_CLIENT.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
MY_SHADOW_CLIENT.configureConnectDisconnectTimeout(10)
MY_SHADOW_CLIENT.configureMQTTOperationTimeout(5)
MY_SHADOW_CLIENT.connect()

# Create a programmatic representation of the shadow.
MY_DEVICE_SHADOW = MY_SHADOW_CLIENT.createShadowHandlerWithName(SHADOW_HANDLER, True)

def get_shadow_callback(payload, response_status, token):
    state = JSON.loads(str(payload))["state"]
    alarm = state["desired"]["alarm"]
    print("alarm: "+ alarm)
    if alarm == "on":
        ARDUINO_SERIAL.write(str.encode("T"))
    else:
        ARDUINO_SERIAL.write(str.encode("L"))
    state["reported"] = state["desired"]
    MY_DEVICE_SHADOW.shadowUpdate(state, update_shadow_callback, TIMEOUT_IN_SECONDS)

    data = ARDUINO_SERIAL.read()
    if str(data) == "b'F'":
        now = datetime.datetime.now()
        now_str = now.isoformat()  # Convert to ISO 8601 string
        json_payload = ('{"state":{"desired":{"alarm":"off", "alarmTime":"' +
                        now_str + '", "alarmReason":"" }}}')
        MY_DEVICE_SHADOW.shadowUpdate(json_payload, update_shadow_callback, TIMEOUT_IN_SECONDS)

def update_shadow_callback(payload, response_status, token):
    if response_status == "timeout":
        print("report update timed out!")
    if response_status == "accepted":
        print("report update accepted")
    if response_status == "rejected":
        print("report rejected!")

while True:
    MY_DEVICE_SHADOW.shadowGet(get_shadow_callback, TIMEOUT_IN_SECONDS)
    time.sleep(SECONDS_TO_SLEEP)