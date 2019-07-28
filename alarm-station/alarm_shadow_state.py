import time
import datetime
import json as JSON
import serial
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

HOST_NAME = "azhkicv1gj9gc-ats.iot.us-east-2.amazonaws.com"
ROOT_CA = "./certs/AmazonRootCA1.pem"
PRIVATE_KEY = "./certs/e2360f5815-private.pem.key"
CERT_FILE = "./certs/e2360f5815-certificate.pem.crt"

SHADOW_CLIENT = "AlarmStation"
SHADOW_HANDLER = "AlarmStation"
TIMEOUT_IN_SECONDS = 2
SECONDS_TO_SLEEP = 5

ARDUINO_SERIAL = serial.Serial("/dev/cu.usbmodem1421", 9600)  # "COM3" on Windows

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
    desired = state["desired"]
    if desired["alarm"] == "on":
        ARDUINO_SERIAL.write(str.encode("H"))
        to_update = '{"state":{"reported":' + JSON.dumps(desired) + '}}'
        MY_DEVICE_SHADOW.shadowUpdate(to_update, update_shadow_callback, TIMEOUT_IN_SECONDS)

    data = ARDUINO_SERIAL.read()
    if str(data) == "b'B'":
        now = datetime.datetime.now()
        now_str = now.isoformat()  # Convert to ISO 8601 string
        json_payload = ('{"state":{' +
                        '"desired":{"alarm":"off", "alarmTime":"' + now_str + '", "alarmReason":""}' +
                        '"reported":{"alarm":"off", "alarmTime":"' + now_str + '", "alarmReason":""}' +
                        '}}')
        MY_DEVICE_SHADOW.shadowUpdate(json_payload, update_shadow_callback, TIMEOUT_IN_SECONDS)
        ARDUINO_SERIAL.write(str.encode("L"))


def update_shadow_callback(payload, response_status, token):
    if response_status == "accepted":
        print("report update accepted")
    elif response_status == "timeout":
        print("report update timed out!")
        # maybe opt for an automatic retry?
    elif response_status == "rejected":
        print("report rejected!")


while True:
    MY_DEVICE_SHADOW.shadowGet(get_shadow_callback, TIMEOUT_IN_SECONDS)
    time.sleep(SECONDS_TO_SLEEP)
