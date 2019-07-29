import time
from statistics import mean
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import smbus
import RPi.GPIO as GPIO

import hc_sr04
import bme280

DEVICE = 0x76  # 0x77 was default device I2C address
TOPIC = "flooding-kit/ponte-vecchio-kit"

READS_PER_CYCLE = 10
LOWEST_READS_TO_DISCARD = 3
HIGHEST_READS_TO_DISCARD = 3
SECONDS_BETWEEN_READS = 1

# Configure AWS IoT SDK settings
AWS_IOT_MQTT_CLIENT = AWSIoTMQTTClient("basicPubSub")
PORT = 8883
HOST = "azhkicv1gj9gc-ats.iot.us-east-2.amazonaws.com"
ROOT_CA_PATH = "./certs/AmazonRootCA1.pem"
PRIVATE_KEY_PATH = "./certs/19ecbe119d-private.pem.key"
CERTIFICATE_PATH = "./certs/19ecbe119d-certificate.pem.crt"

AWS_IOT_MQTT_CLIENT.configureEndpoint(HOST, PORT)
AWS_IOT_MQTT_CLIENT.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)
AWS_IOT_MQTT_CLIENT.configureAutoReconnectBackoffTime(1, 32, 20)
AWS_IOT_MQTT_CLIENT.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
AWS_IOT_MQTT_CLIENT.configureDrainingFrequency(2)  # Draining: 2 Hz
AWS_IOT_MQTT_CLIENT.configureConnectDisconnectTimeout(10)  # 10 sec
AWS_IOT_MQTT_CLIENT.configureMQTTOperationTimeout(5)  # 5 sec
AWS_IOT_MQTT_CLIENT.connect()

bus = smbus.SMBus(1)  # I2C bus

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 24
GPIO_ECHO = 23
GPIO_RAIN = 7

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_RAIN, GPIO.IN)

proximities = [0] * READS_PER_CYCLE
temperatures = [0] * READS_PER_CYCLE
pressures = [0] * READS_PER_CYCLE
humidities = [0] * READS_PER_CYCLE

try:
    while True:
        print("\nStarting new acquisition cicle...")
        for i in range(READS_PER_CYCLE):
            proximities[i] = hc_sr04.read_distance(GPIO_TRIGGER, GPIO_ECHO)
            temperatures[i], pressures[i], humidities[i] = bme280.read_bme280_all(DEVICE, bus)
            time.sleep(SECONDS_BETWEEN_READS)

        timestamp = int(time.time())

        proximities.sort()
        temperatures.sort()
        pressures.sort()
        humidities.sort()

        trimmed_proximities = proximities[LOWEST_READS_TO_DISCARD:-HIGHEST_READS_TO_DISCARD]
        trimmed_temperatures = temperatures[LOWEST_READS_TO_DISCARD:-HIGHEST_READS_TO_DISCARD]
        trimmed_pressures = pressures[LOWEST_READS_TO_DISCARD:-HIGHEST_READS_TO_DISCARD]
        trimmed_humidities = humidities[LOWEST_READS_TO_DISCARD:-HIGHEST_READS_TO_DISCARD]

        proximity = round(mean(trimmed_proximities), 1)
        temperature = round(mean(trimmed_temperatures), 1)
        pressure = round(mean(trimmed_pressures), 2)
        humidity = round(mean(trimmed_humidities), 1)

        raining = GPIO.input(GPIO_RAIN) != 1  # True if GPIO_RAIN == 0

        print("Timestamp = %s " % str(timestamp))
        print("Proximity = %s cm" % str(proximity))
        print("Pressure = %s mPa" % str(pressure))
        print("Temperature = %s C" % str(temperature))
        print("Humidity = %s %%" % str(humidity))

        if raining:
            print("It's raining!")
        else:
            print("It's not raining")

        msg = ('{ "measureTime":' + str(timestamp) +
               ', "proximity":' + str(proximity) +
               ', "temperature":' + str(temperature) +
               ', "humidity":' + str(humidity) +
               ', "pressure":' + str(pressure) +
               ', "raining":' + (str(raining)).lower() + '}')

        AWS_IOT_MQTT_CLIENT.publish(TOPIC, msg, 0)

except KeyboardInterrupt:
    print("\nMeasurement stopped by the User\n")
finally:
    GPIO.cleanup()
