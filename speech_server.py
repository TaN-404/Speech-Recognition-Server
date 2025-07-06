import socket
import speech_recognition as sr
import threading
import time

HOST = "127.0.0.1"
PORT = 65432

recognizer = sr.Recognizer()


# Flag to stop threads
running = True

def recognize_and_send(conn):
    global running
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("[INFO] Adjusted for ambient noise. Listening...")
        while running:
            try:
                print("[INFO] Listening for speech...")
                audio = recognizer.listen(source, timeout=5)
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"[RECOGNIZED] {text}")
                    conn.sendall((text + "\n").encode("utf-8"))
                except sr.UnknownValueError:
                    print("[WARN] Speech was unintelligible.")
                except sr.RequestError as e:
                    print(f"[ERROR] Could not request results; {e}")
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"[ERROR] {e}")
                break

def start_server():
    global running
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"[INFO] Listening on {HOST}:{PORT}...")
        conn, addr = server.accept()
        with conn:
            print(f"[INFO] Client connected from {addr}")
            recognize_and_send(conn)

try:
    start_server()
except KeyboardInterrupt:
    print("\n[INFO] Shutting down.")
    running = False
except Exception as e:
    print(f"[FATAL ERROR] {e}")
finally:
    running = False
    time.sleep(1)
    print("[INFO] Server closed.")
