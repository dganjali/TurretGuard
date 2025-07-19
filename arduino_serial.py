import serial
import time

# Connect to Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Connect to camera (OpenMV or similar)
cam = serial.Serial('/dev/ttyACM0', 115200, timeout=1)  # <-- try 115200

time.sleep(2)

while True:
    if cam.in_waiting:
        data = cam.readline().decode().strip()
        print("cam:", data)

        # Parse dx/dy
        if "dx:" in data and "dy:" in data:
            try:
                parts = data.split(';')
                dx = int(parts[0].split(':')[1])
                dy = int(parts[1].split(':')[1])

                # You can decide how to convert dx/dy to azimuth/elevation
                azimuth = dx  # TEMP: direct map
                elevation = dy  # TEMP: direct map
                fire = 1 if abs(dx) < 5 and abs(dy) < 5 else 0

                msg = f"A:{azimuth};E:{elevation};F:{fire}\n"
                print("sending:", msg.strip())
                ser.write(msg.encode())
            except Exception as e:
                print("Error parsing camera data:", e)

    if ser.in_waiting:
        print("Arduino:", ser.readline().decode().strip())
