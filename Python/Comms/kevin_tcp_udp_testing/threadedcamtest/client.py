import pickle
import socket
import struct
import time
from threading import Thread
from WebcamVideoStream import WebcamVideoStream

HEADER  = 4096
PORT    = 8080
FORMAT  = 'utf-8'
SERVER  = '192.168.43.18'
ADDR    = (SERVER,PORT)

print(f"[INFO] Starting camera...")
vs = WebcamVideoStream().start()
time.sleep(1)

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(ADDR)


while True:
    grabbed, frame = vs.read()
    data = pickle.dumps(frame)
    clientsocket.sendall(struct.pack("i", len(data)) + data)

