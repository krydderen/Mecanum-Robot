from struct import pack
import cv2
import pickle
import socket
import struct

HEADER  = 4096
PORT    = 8080
FORMAT  = 'utf-8'
SERVER  = '192.168.43.18'
ADDR    = (SERVER,PORT)

cap = cv2.VideoCapture(0)
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(ADDR)

while True:
    ret,frame = cap.read()
    data = pickle.dumps(frame)
    clientsocket.sendall(struct.pack("L", len(data)) + data)