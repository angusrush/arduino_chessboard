#!/usr/bin/python

import serial
import time

ser = serial.Serial("/dev/ttyACM0", 9600)

while True:
    if ser.in_waiting > 0:
        reading = ser.readline().decode("utf-8")
        print(reading)

    time.sleep(0.01)
