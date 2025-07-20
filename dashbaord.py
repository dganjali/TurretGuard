import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import serial
import threading
import io
import time

# ==== Config ====
SERIAL_PORT = '/dev/ttyUSB0'  # Adjust if needed
BAUD_RATE = 115200

# ==== UI Class ====
class TurretGuardUI:
    def __init__(self, master):
        self.master = master
        master.title("TurretGuard Control Panel")
        master.geometry("800x600")
        master.configure(bg="#1e1e1e")

        # Serial setup
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        except Exception as e:
            print("Failed to open serial port:", e)
            exit()

        # Image Display
        self.image_label = tk.Label(master, bg="black")
        self.image_label.pack(pady=10)

        # Status Frame
        self.status_frame = tk.Frame(master, bg="#1e1e1e")
        self.status_frame.pack()

        self.azimuth_var = tk.StringVar(value="Azimuth: --°")
        self.elevation_var = tk.StringVar(value="Elevation: --°")
        self.confidence_var = tk.StringVar(value="Confidence: --")
        self.state_var = tk.StringVar(value="System: ---")

        self.add_status_label("Azimuth", self.azimuth_var)
        self.add_status_label("Elevation", self.elevation_var)
        self.add_status_label("Confidence", self.confidence_var)
        self.add_status_label("System", self.state_var)

        # Controls
        self.controls_frame = tk.Frame(master, bg="#1e1e1e")
        self.controls_frame.pack(pady=10)

        tk.Button(self.controls_frame, text="Manual Fire", command=self.manual_fire,
                  bg="#e74c3c", fg="white", width=15).grid(row=0, column=0, padx=10)

        tk.Button(self.controls_frame, text="Abort Launch", command=self.abort_launch,
                  bg="#f1c40f", fg="black", width=15).grid(row=0, column=1, padx=10)

        # Start threads
        self.running = True
        threading.Thread(target=self.serial_loop, daemon=True).start()
        threading.Thread(target=self.image_loop, daemon=True).start()

    def add_status_label(self, name, var):
        label = tk.Label(self.status_frame, textvariable=var, font=("Helvetica", 14),
                         bg="#1e1e1e", fg="white", width=30, anchor="w")
        label.pack()

    def serial_loop(self):
        while self.running:
            try:
                line = self.ser.readline()
                if b'\xFF\xD8' in line:
                    continue  # Skip image bytes here
                decoded = line.decode(errors='ignore').strip()
                if decoded.startswith("A:"):
                    self.parse_status(decoded)
            except Exception as e:
                print("Serial error:", e)

    def parse_status(self, data):
        try:
            parts = data.split(";")
            az = parts[0].split(":")[1]
            el = parts[1].split(":")[1]
            conf = parts[2].split(":")[1]
            state = parts[3].split(":")[1]

            self.azimuth_var.set(f"Azimuth: {az}°")
            self.elevation_var.set(f"Elevation: {el}°")
            self.confidence_var.set(f"Confidence: {float(conf)*100:.1f}%")
            self.state_var.set(f"System: {state}")
        except:
            pass

    def image_loop(self):
        while self.running:
            try:
                if self.ser.in_waiting > 0:
                    img = self.read_image()
                    if img:
                        self.show_image(img)
            except Exception as e:
                print("Image error:", e)

    def read_image(self):
        # Look for JPEG start marker
        start = self.ser.read(2)
        if start != b'\xFF\xD8':
            return None
        img_data = bytearray(start)
        while True:
            b = self.ser.read(1)
            if not b:
                return None
            img_data.extend(b)
            if img_data[-2:] == b'\xFF\xD9':  # JPEG end marker
                break
        try:
            return Image.open(io.BytesIO(img_data))
        except:
            return None

    def show_image(self, img):
        img = img.resize((640, 480))
        tk_img = ImageTk.PhotoImage(img)
        self.image_label.config(image=tk_img)
        self.image_label.image = tk_img

    def manual_fire(self):
        try:
            self.ser.write(b"FIRE\n")
        except:
            print("Failed to send fire command")

    def abort_launch(self):
        try:
            self.ser.write(b"ABORT\n")
        except:
            print("Failed to send abort command")

    def on_close(self):
        self.running = False
        try:
            self.ser.close()
        except:
            pass
        self.master.destroy()

# ==== Run the App ====
if __name__ == "__main__":
    root = tk.Tk()
    app = TurretGuardUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
