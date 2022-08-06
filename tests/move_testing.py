#!/usr/bin/python

import serial
import time 

port = '/dev/pts/3'

ser = serial.Serial(port, 9600)

events = ["14 up",
          "22 down",
          "B down",
          "48 up",
          "40 down",
          "B down",
          "5 up",
          "14 down",
          "B down",
          "40 up",
          "32 down",
          "B down",
          "6 up",
          "21 down",
          "B down",
          "32 up",
          "24 down",
          "B down",
          "4 up",
          "7 up",
          "5 down",
          "5 up",
          "6 down",
          "6 up",
          "6 down",
          "5 down",
          "B down",
          "49 up",
          "41 down",
          "B down",
          "9 up",
          "25 down",
          "B down",
          "24 up",
          "17 down",
          "25 up",
          "B down"]

for event in events:
    ser.write(bytes(event + "\n", encoding='utf8'))
    time.sleep(0.5)

