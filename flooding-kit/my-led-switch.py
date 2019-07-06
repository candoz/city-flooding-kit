# Import package
import paho.mqtt.client as mqtt
import ssl, time, sys

# =======================================================
# Set Following Variables
# AWS IoT Endpoint
MQTT_HOST = "azhkicv1gj9gc-ats.iot.us-east-2.amazonaws.com"
# CA Root Certificate File Path
CA_ROOT_CERT_FILE = "../certs/alarm-station/AmazonRootCA1.pem"
# AWS IoT Thing Name
THING_NAME = "AlarmStation"
# AWS IoT Thing Certificate File Path
THING_CERT_FILE = "../certs/alarm-station/e2360f5815-certificate.pem.crt"
# AWS IoT Thing Private Key File Path
THING_PRIVATE_KEY_FILE = "../certs/alarm-station/e2360f5815-private.pem"
# =======================================================


# =======================================================
# No need to change following variables
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
SHADOW_UPDATE_TOPIC = "$aws/things/" + THING_NAME + "/shadow/update"
SHADOW_UPDATE_ACCEPTED_TOPIC = "$aws/things/" + THING_NAME + "/shadow/update/accepted"
SHADOW_UPDATE_REJECTED_TOPIC = "$aws/things/" + THING_NAME + "/shadow/update/rejected"
# =======================================================



# Initiate MQTT Client
mqttc = mqtt.Client("client1")

# Define on connect event function
# We shall subscribe to Shadow Accepted and Rejected Topics in this function
def on_connect(mosq, obj, rc):
    mqttc.subscribe(SHADOW_UPDATE_ACCEPTED_TOPIC, 1)
    mqttc.subscribe(SHADOW_UPDATE_REJECTED_TOPIC, 1)

# Define on_message event function. 
# This function will be invoked every time,
# a new message arrives for the subscribed topic 
def on_message(mosq, obj, msg):
	if str(msg.topic) == SHADOW_UPDATE_ACCEPTED_TOPIC:
		print "\n---SUCCESS---\nShadow State Doc Accepted by AWS IoT."
		print "Response JSON:\n" + str(msg.payload)
	elif str(msg.topic) == SHADOW_UPDATE_REJECTED_TOPIC:
		print "\n---FAILED---\nShadow State Doc Rejected by AWS IoT."
		print "Error Response JSON:\n" + str(msg.payload)
	else:
		print "AWS Response Topic: " + str(msg.topic)
		print "QoS: " + str(msg.qos)
		print "Payload: " + str(msg.payload)
	# Disconnect from MQTT_Broker
	mqttc.disconnect()


# Register callback functions
mqttc.on_message = on_message
mqttc.on_connect = on_connect

# Configure TLS Set
mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY_FILE, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)		
mqttc.loop_start()