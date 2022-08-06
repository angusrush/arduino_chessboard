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
          "36 down",
          "B down",
          "35 up",
          "27 down",
          "B down",
          "36 up",
          "44 down",
          "B down",
          "27 up",
          "19 down",
          "B down",
          "44 up",
          "53 up",
          "53 down",
          "B down",
          "60 up",
          "51 down",
          "B down",
          "15 up",
          "23 down",
          "B",
          "19 up",
          "10 up",
          "10 down",
          "B",
          "53 up",
          "62 up",
          "62 down",
          "B"]

for event in events:
    ser.write(bytes(event + "\n", encoding='utf8'))
    time.sleep(0.5)

