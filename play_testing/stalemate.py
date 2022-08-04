#!/usr/bin/python

import serial
import time 

port = '/dev/pts/3'

ser = serial.Serial(port, 9600)


events = ["10 up",
          "18 down",
          "B down",
          "51 up",
          "35 down",
          "B down",
          "3 up",
          "17 down",
          "B down",
          "55 up",
          "39 down",
          "B down",
          "17 up",
          "49 up",
          "49 down",
          "B down",
          "58 up",
          "37 down",
          "B down",
          "49 up",
          "48 up",
          "48 down",
          "B down",
          "37 up",
          "55 down",
          "B down",
          "48 up",
          "57 up",
          "57 down",
          "B down",
          "56 up",
          "49 down",
          "49 up",
          "48 down",
          "48 up",
          "40 down",
          "B down",
          "57 up",
          "50 up",
          "50 down",
          "B down",
          "40 up",
          "47 down",
          "B down",
          "15 up",
          "31 down",
          "B down",
          "53 up",
          "45 down",
          "B down",
          "50 up",
          "59 up",
          "59 down",
          "B down",
          "60 up",
          "53 down",
          "B down",
          "59 up",
          "35 up",
          "35 down",
          "B down",
          "53 up",
          "46 down",
          "B down",
          "35 up",
          "44 down",
          "B down"]

for event in events:
    ser.write(bytes(event + "\n", encoding='utf8'))
    time.sleep(0.7)

