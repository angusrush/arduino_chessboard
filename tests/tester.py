#!/usr/bin/python

import serial
import time
import sys

port = "/dev/pts/3"

ser = serial.Serial(port, 9600)

try:
    file = open(sys.argv[1], "r")
    events = file.readlines()

    for event in events:
        ser.write(bytes(event, encoding="utf8"))
        print(port + ": " + str(event), end="")
        time.sleep(0.5)
except:
    pass

while True:
    message = input(port + ": ")
    ser.write(bytes(message + "\n", encoding="utf8"))
