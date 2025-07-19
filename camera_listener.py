import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)
while True:
    if ser.in_waiting > 0:
        print(ser.readline().decode().strip())
    else:
        print("Waiting...")
        time.sleep(0.15)