from machine import I2C, Pin
import time
from bno055 import BNO055
import socket
import network


# Initialize I2C bus 0 on Pico 2 W (GP4 = SDA, GP5 = SCL)
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)

print("Initializing BNO055 sensor...")
try:
    sensor = BNO055(i2c)
    print("BNO055 successfully initialized!")
except Exception as e:
    print(f"Initialization failed: {e}")
    sensor = None


# 1. Connect to Wi-Fi
SSID = "asdfasdf"
PASSWORD = "adfasdf"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    time.sleep(0.5)

pico_ip = wlan.ifconfig()[0]
print(f"Connected! Pico IP Address: {pico_ip}")

# 2. Start TCP Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", 5000))
server_socket.listen(1)

print("Listening for incoming PC connection on port 5000...")


if sensor:
    print("Reading data... Press Ctrl+C to stop.")
    conn, addr = server_socket.accept()
    print(f"PC connected from: {addr}")
    
    try:
        while True:
            # Read acceleration data (m/s^2)
            accel_x, accel_y, accel_z = sensor.read_acceleration()
                
            # Read absolute pose / orientation (Euler angles in degrees)
            heading, roll, pitch = sensor.read_euler()
                
            # Print formatted data to the Thonny IDE Shell
            data_str_accel = f"Accel (m/s^2) -> X: {accel_x:6.2f} | Y: {accel_y:6.2f} | Z: {accel_z:6.2f}"
            data_str_absPose = f"Absolute Pose -> Heading: {heading:6.2f}° | Roll: {roll:6.2f}° | Pitch: {pitch:6.2f}°"
            data_str_socket = data_str_accel + "\n" + data_str_absPose + "\n"
            print(data_str_accel) # Thonny shell print
            print(data_str_absPose) # Thonny shell print
            print("-" * 55)
            conn.send(data_str_socket.encode("utf-8")) # Wifi packet send
            
            time.sleep(0.5)
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        conn.close()

        
