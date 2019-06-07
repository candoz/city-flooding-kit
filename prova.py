from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

import logging
import json
import time

# First you need to configure the SDK settings
# Usually looks like this:
aws_iot_mqtt_client = None
aws_iot_mqtt_client = AWSIoTMQTTClient("basicPubSub")
port = 8883
host = "azzh4c40pkqc9-ats.iot.us-east-1.amazonaws.com"
rootCA_path = "./AmazonRootCA1.pem"
private_key_path = "./acb5e1e298-private.pem.key"
certificate_path = "./acb5e1e298-certificate.pem.crt"

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

def shadow_delta_callback(payload, responseStatus, token):
    print("payload ", payload)
    print("responseStatus ", responseStatus)
    print("token ", token)

thing_name = "FloodingKit1"
topic = "FloodingKit1/proximitySensor"

aws_iot_mqtt_client.connect()

while True:
    aws_iot_mqtt_client.publish(topic, '{"ciao":"prova2"}', 0)
    time.sleep(10)
