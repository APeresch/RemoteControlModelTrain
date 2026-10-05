from machine import Pin, I2C
from lsm9ds1 import LSM9DS1_I2C
# Create sensor object, communicating over the board's default I2C bus
i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=100000) # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C() # For using the built-in STEMMA QT connector on amicrocontroller
sensor = LSM9DS1_I2C(i2c)


# # Set sensor rang accordingly
# sensor.accel_range = adafruit_lsm9ds1.ACCELRANGE_4G
#sensor.mag_gain = adafruit_lsm9ds1.MAGGAIN_8GAUSS
# sensor.gyro_scale = adafruit_lsm9ds1.GYROSCALE_500DP

print(i2c.scan())

while True:
    ax, ay, az = sensor.accel
    gx, gy, gz = sensor.gyro
    mx, my, mz = sensor.mag

    print(f"Accel (m/s²): X={ax:6.2f}, Y={ay:6.2f}, Z={az:6.2f}")
    print(f"Gyro  (deg/s): X={gx:6.2f}, Y={gy:6.2f}, Z={gz:6.2f}")
    print(f"Mag   (gauss): X={mx:6.2f}, Y={my:6.2f}, Z={mz:6.2f}")
    print("-" * 40)
    time.sleep(0.5)

