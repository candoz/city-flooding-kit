import time
import RPi.GPIO as GPIO

def read_distance(trigger, echo):

    # set Trigger to HIGH, then after 0.01ms to LOW
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    start_time = time.time()
    while GPIO.input(echo) == 0:
        start_time = time.time()

    stop_time = time.time()
    while GPIO.input(echo) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time

    # multiply with the sonic speed (34300 cm/s) and divide by 2, because there and back
    distance = (elapsed_time * 34300) / 2

    return distance
