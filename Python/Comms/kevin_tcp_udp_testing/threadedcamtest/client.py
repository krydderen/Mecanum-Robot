import pickle
import socket
import struct
import time
from threading import Thread
from WebcamVideoStream import CameraStream
import cv2

HEADER  = 4086
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
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        data = pickle.dumps(frame)
        clientsocket.sendall(struct.pack("i", len(data)) + data)
    except Exception as e:
        print(f"[ERROR] Closing.. {e}")
        break
    
clientsocket.close()
cap.stop()