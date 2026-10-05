from machine import I2C, Pin
import time
from bno055 import BNO055

# Initialize I2C bus 0 on Pico 2 W (GP4 = SDA, GP5 = SCL)
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)

print("Initializing BNO055 sensor...")
try:
    sensor = BNO055(i2c)
    print("BNO055 successfully initialized!")
except Exception as e:
    print(f"Initialization failed: {e}")
    sensor = None

if sensor:
    print("Reading data... Press Ctrl+C to stop.")
    while True:
        try:
            # Read acceleration data (m/s^2)
            accel_x, accel_y, accel_z = sensor.read_acceleration()
            
            # Read absolute pose / orientation (Euler angles in degrees)
            heading, roll, pitch = sensor.read_euler()
            
            # Print formatted data to the Thonny IDE Shell
            print(f"Accel (m/s^2) -> X: {accel_x:6.2f} | Y: {accel_y:6.2f} | Z: {accel_z:6.2f}")
            print(f"Absolute Pose -> Heading: {heading:6.2f}° | Roll: {roll:6.2f}° | Pitch: {pitch:6.2f}°")
            print("-" * 55)
            
        except Exception as e:
            print(f"Read error: {e}")
            
        time.sleep(0.5)