import pickle
import socket
import struct
import time
from threading import Thread
from WebcamVideoStream import CameraStream

HEADER  = 131072
PORT    = 8080
FORMAT  = 'utf-8'
SERVER  = '192.168.43.18'
ADDR    = (SERVER,PORT)

print(f"[INFO] Starting camera...")
cap = CameraStream().start()
time.sleep(1)

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(ADDR)


while True:
    try:
        frame = cap.read()
        data = pickle.dumps(frame)
        clientsocket.sendall(struct.pack("L", len(data)) + data)
    except Exception as e:
        print(f"[ERROR] Closing.. {e}")
        break
    
clientsocket.close()
cap.stop()