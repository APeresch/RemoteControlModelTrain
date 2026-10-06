import socket
import time

PICO_IP = "192.168.0.194"  # Replace with the IP printed by the Pico
PORT = 5000

print(f"Connecting to Pico 2 W at {PICO_IP}:{PORT}...")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((PICO_IP, PORT))
    print("Connected! Reading data stream...\n")

    buffer = ""
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break
        buffer += data
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            print(f"[Pico Data]: {line}")

except KeyboardInterrupt:
    print("\nClosing connection...")
finally:
    client_socket.close()