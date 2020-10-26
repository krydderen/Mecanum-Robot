import cv2
import pickle
import socket
import struct
import sys
import numpy as np

HEADER  = 4096
PORT    = 8080
FORMAT  = 'utf-8'
SERVER  = socket.gethostbyname(socket.gethostname())
ADDR    = (SERVER,PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[SERVER] Socket created.")

server.bind(ADDR)
server.listen(10)
print(f"[SERVER] Server is listening on {ADDR}.")

conn, addr = server.accept()

data = b''

payload_size = struct.calcsize("i")

while True:
    while len(data) < payload_size:
        data += conn.recv(HEADER)
    packed_msg_size = data[:payload_size]

    data = data[payload_size:]
    msg_size = struct.unpack("i", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data)
    print(frame.size)
    cv2.imshow('frame', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
conn.close()