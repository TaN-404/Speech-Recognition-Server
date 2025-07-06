# test_client.py
import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("[CLIENT] Connected to speech server.")
    while True:
        data = s.recv(1024)
        if not data:
            break
        print("[CLIENT] Received:", data.decode("utf-8").strip())
