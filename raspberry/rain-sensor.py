#!/usr/bin/env python

from time import sleep
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.IN)
state = GPIO.input(7)

print("ehiii "+ state)