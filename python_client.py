import socket
import speech_recognition as sr
import time
import sys

# ---- SINGLE INSTANCE LOCK ----
LOCK_PORT = 54321  # Use any port that's not in use

def is_already_running():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", LOCK_PORT))
        return False
    except socket.error:
        return True

if is_already_running():
    print("[INFO] Another instance is already running.")
    sys.exit()
# ------------------------------

# ---- UDP SETUP ----
UDP_IP = "127.0.0.1"
UDP_PORT = 4242
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ---- SPEECH RECOGNITION SETUP ----
recognizer = sr.Recognizer()
mic = sr.Microphone()

running = True
print(f"[UDP SPEECH] Sending to {UDP_IP}:{UDP_PORT}")

try:
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("[INFO] Calibrated. Listening for speech...")
        while running:
            try:
                print("[INFO] Listening...")
                audio = recognizer.listen(source, timeout=5)

                try:
                    text = recognizer.recognize_google(audio)
                    print(f"[RECOGNIZED] {text}")
                    sock.sendto(text.encode('utf-8'), (UDP_IP, UDP_PORT))
                except sr.UnknownValueError:
                    print("[WARN] Could not understand audio.")
                except sr.RequestError as e:
                    print(f"[ERROR] API error: {e}")

            except sr.WaitTimeoutError:
                continue

except KeyboardInterrupt:
    print("[INFO] Exiting.")
    running = False

finally:
    sock.close()
