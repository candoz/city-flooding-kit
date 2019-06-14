# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# BMP280
# This code is designed to work with the BMP280_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Barometer?sku=BMP280_I2CSs#tabs-0-product_tabset-2

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import smbus
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

topic = "floodingKit/p280"

aws_iot_mqtt_client.connect()

# Get I2C bus
bus = smbus.SMBus(1)

def getP280values():
    # BMP280 address, 0x76(118)
    # Read data back from 0x88(136), 24 bytes
    b1 = bus.read_i2c_block_data(0x76, 0x88, 24)

    # Convert the data
    # Temp coefficents
    dig_T1 = b1[1] * 256 + b1[0]
    dig_T2 = b1[3] * 256 + b1[2]
    if dig_T2 > 32767 :
        dig_T2 -= 65536
    dig_T3 = b1[5] * 256 + b1[4]
    if dig_T3 > 32767 :
        dig_T3 -= 65536

    # Pressure coefficents
    dig_P1 = b1[7] * 256 + b1[6]
    dig_P2 = b1[9] * 256 + b1[8]
    if dig_P2 > 32767 :
        dig_P2 -= 65536
    dig_P3 = b1[11] * 256 + b1[10]
    if dig_P3 > 32767 :
        dig_P3 -= 65536
    dig_P4 = b1[13] * 256 + b1[12]
    if dig_P4 > 32767 :
        dig_P4 -= 65536
    dig_P5 = b1[15] * 256 + b1[14]
    if dig_P5 > 32767 :
        dig_P5 -= 65536
    dig_P6 = b1[17] * 256 + b1[16]
    if dig_P6 > 32767 :
        dig_P6 -= 65536
    dig_P7 = b1[19] * 256 + b1[18]
    if dig_P7 > 32767 :
        dig_P7 -= 65536
    dig_P8 = b1[21] * 256 + b1[20]
    if dig_P8 > 32767 :
        dig_P8 -= 65536
    dig_P9 = b1[23] * 256 + b1[22]
    if dig_P9 > 32767 :
        dig_P9 -= 65536

    # BMP280 address, 0x76(118)
    # Select Control measurement register, 0xF4(244)
    #		0x27(39)	Pressure and Temperature Oversampling rate = 1
    #					Normal mode
    bus.write_byte_data(0x76, 0xF4, 0x27)
    # BMP280 address, 0x76(118)
    # Select Configuration register, 0xF5(245)
    #		0xA0(00)	Stand_by time = 1000 ms
    bus.write_byte_data(0x76, 0xF5, 0xA0)

    time.sleep(0.5)

    # BMP280 address, 0x76(118)
    # Read data back from 0xF7(247), 8 bytes
    # Pressure MSB, Pressure LSB, Pressure xLSB, Temperature MSB, Temperature LSB
    # Temperature xLSB, Humidity MSB, Humidity LSB
    data = bus.read_i2c_block_data(0x76, 0xF7, 8)

   # Convert pressure and temperature data to 19-bits
    adc_p = ((data[0] * 65536) + (data[1] * 256) + (data[2] & 0xF0)) / 16
    adc_t = ((data[3] * 65536) + (data[4] * 256) + (data[5] & 0xF0)) / 16
    adc_h = (data[6] << 8) | data[7]

    # Temperature offset calculations
    var1 = ((adc_t) / 16384.0 - (dig_T1) / 1024.0) * (dig_T2)
    var2 = (((adc_t) / 131072.0 - (dig_T1) / 8192.0) * ((adc_t)/131072.0 - (dig_T1)/8192.0)) * (dig_T3)
    t_fine = (var1 + var2)
    cTemp = (var1 + var2) / 5120.0

    # Pressure offset calculations
    var1 = (t_fine / 2.0) - 64000.0
    var2 = var1 * var1 * (dig_P6) / 32768.0
    var2 = var2 + var1 * (dig_P5) * 2.0
    var2 = (var2 / 4.0) + ((dig_P4) * 65536.0)
    var1 = ((dig_P3) * var1 * var1 / 524288.0 + ( dig_P2) * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * (dig_P1)
    p = 1048576.0 - adc_p
    p = (p - (var2 / 4096.0)) * 6250.0 / var1
    var1 = (dig_P9) * p * p / 2147483648.0
    var2 = p * (dig_P8) / 32768.0
    pressure = (p + (var1 + var2 + (dig_P7)) / 16.0) / 100

    # Refine humidity
    humidity = t_fine - 76800.0
    humidity = (adc_h - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity))
    humidity = humidity * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
    humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
    if humidity > 100:
        humidity = 100
    elif humidity < 0:
        humidity = 0

    return cTemp, pressure, humidity

if __name__ == '__main__':
    try:
        counter = 0
        while True:
            counter = counter + 1
            temperature, pressure, humidity = getP280values()
            now = datetime.datetime.now()  # Store current datetime
            now_str = now.isoformat()  # Convert to ISO 8601 string
            msg = '{"counterId":' + str(counter) + ', "temperatureValue":' + str(temperature) + ' , "pressureValue":' + str(pressure) + ', "humidityValue":' + str(humidity) + ', "timestamp":"' + now_str + '", "emergency":false}'
            print "Temperature in Celsius : %.2f C" %temperature
            print "Pressure : %.2f hPa " %pressure
            print "Pressure : %.2f % " %humidity
            aws_iot_mqtt_client.publish(topic, msg, 0)
            time.sleep(4.5)
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
