#!/usr/bin/python

import serial

port = "/dev/pts/1"

ser = serial.Serial(port, 9600)


while True:
    message = input(port + ": ")
    ser.write(bytes(message + "\n", encoding="utf8"))
