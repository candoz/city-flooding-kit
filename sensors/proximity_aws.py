from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import RPi.GPIO as GPIO
import time
import datetime

# A random programmatic shadow client ID.
SHADOW_CLIENT = "shadowKit"

# The unique hostname that AWS IoT generated for this device.
HOST_NAME = "azzh4c40pkqc9-ats.iot.us-east-1.amazonaws.com"

# The relative path to the correct root CA file for AWS IoT, 
# that you have already saved onto this device.
ROOT_CA = "AmazonRootCA1.pem"

# The relative path to your private key file that 
# AWS IoT generated for this device, that you 
# have already saved onto this device.
PRIVATE_KEY = "acb5e1e298-private.pem.key"

# The relative path to your certificate file that 
# AWS IoT generated for this device, that you 
# have already saved onto this device.
CERT_FILE = "acb5e1e298-certificate.pem.crt"

# A programmatic shadow handler name prefix.
SHADOW_HANDLER = "FloodingKit1"

# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
  print()
  print('UPDATE: $aws/things/' + SHADOW_HANDLER + '/shadow/update/#')
  print("payload = " + payload)
  print("responseStatus = " + responseStatus)
  print("token = " + token)

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(SHADOW_HANDLER, True)

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 24
GPIO_ECHO = 23

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            now = datetime.datetime.now()  # Store current datetime
            now_str = now.isoformat()  # Convert to ISO 8601 string
            print ("Measured Distance = %.1f cm" % dist)
            print ("Datetime = " + now_str)
            myDeviceShadow.shadowUpdate(
                '{"value":"' + str(dist) + '", "timestamp":"' + now_str + '", "emergency":false}',
                #'{"value":' + str(dist) + ', "emergency":false}',
                myShadowUpdateCallback,
                5)
            time.sleep(5)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
