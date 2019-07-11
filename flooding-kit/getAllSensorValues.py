import time
import datetime
import json
import smbus
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte

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

def readDistance():
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

def getShort(data, index):
    # return two bytes from data as a signed 16-bit value
    return c_short((data[index+1] << 8) + data[index]).value

def getUShort(data, index):
    # return two bytes from data as an unsigned 16-bit value
    return (data[index+1] << 8) + data[index]

def getChar(data,index):
    # return one byte from data as a signed char
    result = data[index]
    if result > 127:
        result -= 256
    return result

def getUChar(data,index):
    # return one byte from data as an unsigned char
    result =  data[index] & 0xFF
    return result

def readBME280ID(addr=DEVICE):
    # Chip ID Register Address
    REG_ID     = 0xD0
    (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
    return (chip_id, chip_version)

def readBME280All(addr=DEVICE):
    # Register Addresses
    REG_DATA = 0xF7
    REG_CONTROL = 0xF4
    REG_CONFIG  = 0xF5

    REG_CONTROL_HUM = 0xF2
    REG_HUM_MSB = 0xFD
    REG_HUM_LSB = 0xFE

    # Oversample setting - page 27
    OVERSAMPLE_TEMP = 2
    OVERSAMPLE_PRES = 2
    MODE = 1

    # Oversample setting for humidity register - page 26
    OVERSAMPLE_HUM = 2
    bus.write_byte_data(addr, REG_CONTROL_HUM, OVERSAMPLE_HUM)

    control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
    bus.write_byte_data(addr, REG_CONTROL, control)

    # Read blocks of calibration data from EEPROM
    # See Page 22 data sheet
    cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
    cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
    cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)

    # Convert byte data to word values
    dig_T1 = getUShort(cal1, 0)
    dig_T2 = getShort(cal1, 2)
    dig_T3 = getShort(cal1, 4)

    dig_P1 = getUShort(cal1, 6)
    dig_P2 = getShort(cal1, 8)
    dig_P3 = getShort(cal1, 10)
    dig_P4 = getShort(cal1, 12)
    dig_P5 = getShort(cal1, 14)
    dig_P6 = getShort(cal1, 16)
    dig_P7 = getShort(cal1, 18)
    dig_P8 = getShort(cal1, 20)
    dig_P9 = getShort(cal1, 22)

    dig_H1 = getUChar(cal2, 0)
    dig_H2 = getShort(cal3, 0)
    dig_H3 = getUChar(cal3, 2)

    dig_H4 = getChar(cal3, 3)
    dig_H4 = (dig_H4 << 24) >> 20
    dig_H4 = dig_H4 | (getChar(cal3, 4) & 0x0F)

    dig_H5 = getChar(cal3, 5)
    dig_H5 = (dig_H5 << 24) >> 20
    dig_H5 = dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)

    dig_H6 = getChar(cal3, 6)

    # Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
    wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
    time.sleep(wait_time/1000)  # Wait the required time

    # Read temperature/pressure/humidity
    data = bus.read_i2c_block_data(addr, REG_DATA, 8)
    pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    hum_raw = (data[6] << 8) | data[7]

    #Refine temperature
    var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
    var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
    t_fine = var1+var2
    temperature = float(((t_fine * 5) + 128) >> 8);

    # Refine pressure and adjust for temperature
    var1 = t_fine / 2.0 - 64000.0
    var2 = var1 * var1 * dig_P6 / 32768.0
    var2 = var2 + var1 * dig_P5 * 2.0
    var2 = var2 / 4.0 + dig_P4 * 65536.0
    var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * dig_P1
    if var1 == 0:
        pressure=0
    else:
        pressure = 1048576.0 - pres_raw
        pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
        var1 = dig_P9 * pressure * pressure / 2147483648.0
        var2 = pressure * dig_P8 / 32768.0
        pressure = pressure + (var1 + var2 + dig_P7) / 16.0

    # Refine humidity
    humidity = t_fine - 76800.0
    humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity))
    humidity = humidity * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
    humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
    if humidity > 100:
        humidity = 100
    elif humidity < 0:
        humidity = 0

    return temperature/100.0, pressure/100.0, humidity


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
                proximities[i] = readDistance()
                temperatures[i], pressures[i], humidities[i] = readBME280All()
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
