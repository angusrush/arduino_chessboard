#!/usr/bin/python

import serial
import time 

port = '/dev/pts/3'

ser = serial.Serial(port, 9600)

events = ["13 up",
          "21 down",
          "B down",
          "52 up",
          "44 down",
          "B down",
          "14 up",
          "30 down",
          "B down",
          "59 up",
          "52 down",
          "52 up",
          "45 down",
          "45 up",
          "38 down",
          "38 up",
          "31 down",
          "B down"]

for event in events:
    ser.write(bytes(event + "\n", encoding='utf8'))
    time.sleep(0.5)

