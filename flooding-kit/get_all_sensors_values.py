import time
import smbus
import json
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

import hc_sr04
import bme280

DEVICE = 0x76 # 0x77 was default device I2C address

# Configure AWS IoT SDK settings
aws_iot_mqtt_client = None
aws_iot_mqtt_client = AWSIoTMQTTClient("basicPubSub")
port = 8883
host = "azhkicv1gj9gc-ats.iot.us-east-2.amazonaws.com"
rootCA_path = "../certs/flooding-kit/AmazonRootCA1.pem"
private_key_path = "../certs/flooding-kit/19ecbe119d-private.pem.key"
certificate_path = "../certs/flooding-kit/19ecbe119d-certificate.pem.crt"

aws_iot_mqtt_client.configureEndpoint(host, port)
aws_iot_mqtt_client.configureCredentials(rootCA_path, private_key_path, certificate_path)

# AWSIoTMQTTClient connection configuration
aws_iot_mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
aws_iot_mqtt_client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
aws_iot_mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
aws_iot_mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
aws_iot_mqtt_client.configureMQTTOperationTimeout(5)  # 5 sec

topic = "flooding-kit/ponte-vecchio-kit"

aws_iot_mqtt_client.connect()

bus = smbus.SMBus(1) # I2C bus

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 24
GPIO_ECHO = 23
GPIO_RAIN = 7

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_RAIN, GPIO.IN)

if __name__ == '__main__':
    try:
        READS = 10
        LOWEST_READS_TO_DISCARD = 3
        HIGHEST_READS_TO_DISCARD = 3
        SECONDS_BETWEEN_READS = 1
        
        proximities = [0] * READS
        temperatures = [0] * READS
        pressures = [0] * READS
        humidities = [0] * READS
        
        while True:
            
            print("\nStarting new acquisition cicle...")
            for i in range(READS):
                proximities[i] = hc_sr04.readDistance(GPIO_TRIGGER, GPIO_ECHO)
                temperatures[i], pressures[i], humidities[i] = bme280.readBME280All(DEVICE, bus)
                time.sleep(SECONDS_BETWEEN_READS)
            
            timestamp = int(time.time())
            
            proximities.sort()
            temperatures.sort()
            pressures.sort()
            humidities.sort()
            
            clean_proximities = proximities[LOWEST_READS_TO_DISCARD : -HIGHEST_READS_TO_DISCARD]
            clean_temperatures = temperatures[LOWEST_READS_TO_DISCARD : -HIGHEST_READS_TO_DISCARD]
            clean_pressures = pressures[LOWEST_READS_TO_DISCARD : -HIGHEST_READS_TO_DISCARD]
            clean_humidities = humidities[LOWEST_READS_TO_DISCARD : -HIGHEST_READS_TO_DISCARD]
            
            proximity = round(sum(clean_proximities) / len(clean_proximities), 1)
            temperature = round(sum(clean_temperatures) / len(clean_temperatures), 1)
            pressure = round(sum(clean_pressures) / len(clean_pressures), 2)
            humidity = round(sum(clean_humidities) / len(clean_humidities), 1)
            
            raining = GPIO.input(GPIO_RAIN) != 1

            print("Timestamp = %s " % str(timestamp))
            print("Distance = %s cm" % str(proximity))
            print("Pressure = %s mPa" % str(pressure))
            print("Temperature = %s C" % str(temperature))
            print("Humidity = %s %%" % str(humidity))
            
            if raining:
                print("It's raining!")
            else:
                print("It's not raining")

            msg = ('{ "measureTime":' + str(timestamp)
                + ', "proximity":' + str(proximity)
                + ', "temperature":' + str(temperature)
                + ', "humidity":' + str(humidity)
                + ', "pressure":' + str(pressure)
                + ', "raining":' + (str(raining)).lower() + '}')

            aws_iot_mqtt_client.publish(topic, msg, 0)

    except KeyboardInterrupt:
        print("\nMeasurement stopped by the User\n")
    finally:
        GPIO.cleanup()
