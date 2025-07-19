import serial
import time


ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)

azimuth="35"
elevation="10"
fire="1"

message = b"A:"+azimuth+";E:"+elevation+";F:"+fire+"\n"

ser.write(message)

while True:
    if ser.in_waiting:
        response = ser.readline().decode().strip()
        print("received", response)
        break
