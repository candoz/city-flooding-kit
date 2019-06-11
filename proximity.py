from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

import RPi.GPIO as GPIO
import json
import time, datetime

# First you need to configure the SDK settings
# Usually looks like this:
aws_iot_mqtt_client = None
aws_iot_mqtt_client = AWSIoTMQTTClient("basicPubSub")
port = 8883
host = "azhkicv1gj9gc-ats.iot.us-east-2.amazonaws.com"
rootCA_path = "./certs/AmazonRootCA1.pem"
private_key_path = "./certs/19ecbe119d-private.pem.key"
certificate_path = "./certs/19ecbe119d-certificate.pem.crt"

aws_iot_mqtt_client.configureEndpoint(host, port)
aws_iot_mqtt_client.configureCredentials(rootCA_path, private_key_path, certificate_path)

# AWSIoTMQTTClient connection configuration
aws_iot_mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
aws_iot_mqtt_client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
aws_iot_mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
aws_iot_mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
aws_iot_mqtt_client.configureMQTTOperationTimeout(5)  # 5 sec

def topic_callback(client, userdata, message):
    print("MSG RECV:")
    print(json.loads(message.payload.decode('utf-8')))
    print("TOPIC: {}".format(message.topic))
    print()

topic = "floodingKit/proximitySensor"
#topic = "$aws/things/FloodingKit/shadow/update"

aws_iot_mqtt_client.connect()


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
    # multiply with the sonic speed (34300 cm/s) and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        counter = 0
        while True:
            counter = counter + 1
            dist = distance()
            now = datetime.datetime.now()  # Store current datetime
            now_str = now.isoformat()  # Convert to ISO 8601 string
            msg = '{"counterId":' + str(counter) + ', "value":' + str(round(dist)) + ', "timestamp":"' + now_str + '", "emergency":false}'
            print ("Measured Distance = %.1f cm" % dist)
            print ("Datetime = " + now_str)
            aws_iot_mqtt_client.publish(topic, msg, 0)
            time.sleep(5)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
