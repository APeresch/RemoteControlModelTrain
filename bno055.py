from micropython import const
import time

# BNO055 Registers & Constants
BNO055_CHIP_ID_ADDR = const(0x00)
BNO055_OPR_MODE_ADDR = const(0x3D)
BNO055_ACC_DATA_X_LSB_ADDR = const(0x08)
BNO055_EULER_H_LSB_ADDR = const(0x1A)

# Operation Modes
OPERATION_MODE_CONFIG = const(0x00)
OPERATION_MODE_NDOF = const(0x0C)  # 9-DOF fusion mode for absolute pose & acceleration

class BNO055:
    def __init__(self, i2c, address=0x28):
        self.i2c = i2c
        self.address = address
        
        # Give sensor time to boot up (Power-on-reset time is ~650ms)
        time.sleep_ms(650)
        
        # Verify chip ID
        chip_id = self._read_byte(BNO055_CHIP_ID_ADDR)
        if chip_id != 0xA0:
            raise RuntimeError(f"BNO055 not found! Check wiring. Chip ID read: {hex(chip_id)}")
            
        # Switch to configuration mode
        self.set_mode(OPERATION_MODE_CONFIG)
        time.sleep_ms(25)
        
        # Switch to NDOF fusion mode (enables absolute orientation & sensor fusion)
        self.set_mode(OPERATION_MODE_NDOF)
        time.sleep_ms(20)

    def _read_byte(self, addr):
        return self.i2c.readfrom_mem(self.address, addr, 1)[0]

    def _read_bytes(self, addr, length):
        return self.i2c.readfrom_mem(self.address, addr, length)

    def _write_byte(self, addr, value):
        self.i2c.writeto_mem(self.address, addr, bytes([value]))

    def set_mode(self, mode):
        self._write_byte(BNO055_OPR_MODE_ADDR, mode)

    def _to_signed(self, value):
        if value >= 32768:
            value -= 65536
        return value

    def read_acceleration(self):
        """Reads linear acceleration in m/s^2. Returns tuple: (x, y, z)"""
        data = self._read_bytes(BNO055_ACC_DATA_X_LSB_ADDR, 6)
        x = self._to_signed(int.from_bytes(data[0:2], 'little'))
        y = self._to_signed(int.from_bytes(data[2:4], 'little'))
        z = self._to_signed(int.from_bytes(data[4:6], 'little'))
        # Default scaling: 1 m/s^2 = 100 LSB
        return (x / 100.0, y / 100.0, z / 100.0)

    def read_euler(self):
        """Reads absolute orientation (Heading, Roll, Pitch) in degrees. Returns tuple: (heading, roll, pitch)"""
        data = self._read_bytes(BNO055_EULER_H_LSB_ADDR, 6)
        h = self._to_signed(int.from_bytes(data[0:2], 'little'))
        r = self._to_signed(int.from_bytes(data[2:4], 'little'))
        p = self._to_signed(int.from_bytes(data[4:6], 'little'))
        # Default scaling: 1 degree = 16 LSB
        return (h / 16.0, r / 16.0, p / 16.0)