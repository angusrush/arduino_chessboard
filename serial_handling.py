import serial

def myfunc():

ser = serial.Serial('/dev/pts/1', 9600)

while True:
    reading = ser.readline().decode('utf-8')
    print(reading)

