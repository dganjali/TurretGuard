import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
cam = serial.Serial('/dev/ttyACM0', 11600,timeout=1)

time.sleep(2)  # Give time for Arduino to reset

azimuth = "35"
elevation = "10"
fire = "1"

# Build the message as a string
message = f"A:{azimuth};E:{elevation};F:{fire}\n"

# Encode it as bytes and send
ser.write(message.encode())

# Optionally, wait for a response from Arduino
while True:
    if cam.in_waiting:
        data = cam.readline().decode().strip()
        


    if ser.in_waiting:
        response = ser.readline().decode().strip()
        print("received", response)