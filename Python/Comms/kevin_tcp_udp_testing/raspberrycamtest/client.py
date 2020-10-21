from struct import pack
import cv2
import pickle
import socket
import struct
from imutils.video import VideoStream
import time

HEADER  = 4096
PORT    = 8080
FORMAT  = 'utf-8'
SERVER  = '192.168.43.18'
ADDR    = (SERVER,PORT)

print("[INFO] Starting camera...")
picamera = VideoStream(usePiCamera=True, resolution=(640,480),framerate=32).start()
# cap = cv2.VideoCapture(0)
time.sleep(2.0)

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(ADDR)

while True:
    frame = picamera.read()
    data = pickle.dumps(frame)
    clientsocket.sendall(struct.pack("i", len(data)) + data)