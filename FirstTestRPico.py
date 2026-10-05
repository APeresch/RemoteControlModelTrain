import serial
import time

# Configure the serial connection (Update port name as needed)
PORT = 'COM5' 
BAUDRATE = 115200

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)  # Wait for serial connection to stabilize

    test_number = 41
    print(f"[HOST] Sending number: {test_number}")
    
    # Send number followed by newline character
    ser.write(f"{test_number}\n".encode('utf-8'))
    
    # Read response from Pico 2
    while True:
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()
            print(f"[HOST] Received from Pico 2: {response}")
            if response.startswith("RESPONSE:"):
                break

    ser.close()

except serial.SerialException as e:
    print(f"Serial Error: {e}")