import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
cam = serial.Serial('/dev/ttyACM0', 11600,timeout=1)

time.sleep(2)  # Give time for Arduino to reset

fire = 1

# Optionally, wait for a response from Arduino
while True:
    if cam.in_waiting:
        data = cam.readline().decode().strip()
        print("cam:", data)

        if "dx:" in data and "dy:" in data:
            try:
                parts = data.split(';')
                azimuth = int(parts[0].split(':')[1])
                elevation = int(parts[1].split(':')[1])
                print(f"Parsed dx = {azimuth}, dy = {elevation}")
            except (IndexError, ValueError) as e:
                print("Error parsing dx/dy:", e)

                message = f"A:{azimuth};E:{elevation};F:{fire}\n"

                ser.write(message.encode())

    if ser.in_waiting:
        response = ser.readline().decode().strip()
        print("received", response)