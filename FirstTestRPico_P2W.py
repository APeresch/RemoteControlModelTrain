import sys
import select
import time

# Create a polling object to check for incoming USB serial data without blocking
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

print("Pico 2 Ready. Waiting for numbers...")

while True:
    # Check if there is data available to read (timeout = 10ms)
    if poll_obj.poll(10):
        line = sys.stdin.readline().strip()
        if line:
            try:
                # Convert input string to integer, increment, and return
                number = int(line)
                incremented = number + 1
                
                # Send the response back through stdout
                print(f"RESPONSE:{incremented}")
            except ValueError:
                print("ERROR: Please send a valid integer")
    
    time.sleep(0.01)