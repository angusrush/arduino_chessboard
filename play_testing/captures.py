#!/usr/bin/python

import serial
import time 

port = '/dev/pts/3'

ser = serial.Serial(port, 9600)


events = ["12 up",
          "28 down",
          "B down",
          "51 up",
          "35 down",
          "B down",
          "28 up",
          "35 up",
          "35 down",
          "B down",
          "59 up",
          "35 up",
          "35 down",
          "35 up",
          "35 down",
          "35 up",
          "35 down",
          "35 up"]

for event in events:
    ser.write(bytes(event + "\n", encoding='utf8'))
    time.sleep(0.5)

