import pickle
import socket
import struct
import time
import threading
import Queue as queue
import numpy as np
import cv2
from utils.motorcontroller import *
from concurrent.futures import ThreadPoolExecutor


class Client(object):
    def __init__(self):
        self.HEADER = 4086
        self.PORT = 8080
        self.FORMAT = 'utf-8'
        self.SERVER = '192.168.43.18'
        # self.SERVER  = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.socket = None
        self.connected = False
        # - - - - Initialize list of COMMANDS - - - - -
        self.COMMANDS = ['w', 'a', 's', 'd', 'wd',
                         'wa', 'sd', 'sa', 'q', 'e', 'stop']
        # - - - - Initialize motor controller - - - - -
        # self.drivetime = 0.2
        self.moco = MotorController()

    def start(self):
        print("Starting camera...")
        print(f"SERVER - {self.ADDR}")
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 256)
        self.cap.set(4, 144)
        _, self.frame = self.cap.read()
        time.sleep(1)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.ADDR)
        self.connected = True
        print(f"Successfully connected to {self.ADDR}")

    def disconnect(self):
        self.connected = False
        self.socket.close()
        self.cap.stop()
        print(f"Successfully disconnected from {self.ADDR}")

    def handle_send(self, queue, event):
        while not event.is_set():
            while self.connected:
                try:
                    # self.socket.settimeout(5)
                    # print("Reading frame..")
                    cv2.waitKey(100)  # delay
                    _, self.frame = self.cap.read()
                    frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    data = pickle.dumps(frame)
                    self.socket.sendall(struct.pack("L", len(data)) + data)
                    # print(f"sent: {len(data)}")
                except Exception as e:
                    print(f"[ERROR] Closing.. {e}")
                    break

    def handle_read(self, queue, event):
        while not event.is_set():
            """ 
            TODO: Handle how the client reads the response from server.
            ? Should the server only send the response as example w a s d? 
            ? Should the server format the response as JSON? Tuple? 
            TODO: Set up the protocol for the response handling.
            """
            while True:
                data = self.socket.recv(self.HEADER)  # ! Wait for this?
                msg = pickle.loads(data)
                try:
                    # !DEBUG
                    print(f"Server sent data: {msg}")
                    print(f"data: {data}")
                    print(f"msg: {msg}")
                    # !DEBUG-END
                    if msg == 'w':
                        print(f"Sending command to MOCO. |{msg}| ")
                        self.moco.forward(
                            drivetime=0.2, inputspeed='LOW')
                        print(f"Sent command to MOCO. |{msg}| ")
                    elif msg == 'a':
                        print(f"Sending command to MOCO. |{msg}| ")
                        self.moco.left(drivetime=0.2,
                                       inputspeed='LOW')
                        print(f"Sent command to MOCO. |{msg}| ")
                    elif msg == 's':
                        print(f"Sending command to MOCO. |{msg}| ")
                        self.moco.backward(
                            drivetime=0.2, inputspeed='LOW')
                        print(f"Sent command to MOCO. |{msg}| ")
                    elif msg == 'd':
                        print(f"Sending command to MOCO. |{msg}| ")
                        self.moco.right(
                            drivetime=0.2, inputspeed='LOW')
                        print(f"Sent command to MOCO. |{msg}| ")
                    elif msg == 'wd':
                        print(f"Sending command to MOCO. |{msg}| ")
                        self.moco.wddiagonal(
                            drivetime=0.2, inputspeed='LOW')
                    elif msg == 'wa':
                        print(f"Sending command to MOCO. |{msg}| ")
                        self.moco.wadiagonal(
                            drivetime=0.2, inputspeed='LOW')
                    elif msg == 'sd':
                        print(f"Sending command to MOCO. |{msg}| ")
                        self.moco.sddiagonal(
                            drivetime=0.2, inputspeed='LOW')
                    elif msg == 'sa':
                        print(f"Sending command to MOCO. |{msg}| ")
                        self.moco.sadiagonal(
                            drivetime=0.2, inputspeed='LOW')
                    elif msg == 'q':
                        print(f"Sending command to MOCO. |{msg}| ")
                        self.moco.rotate(direction='COUNTER_CLOCKWISE',
                                         drivetime=0.2, inputspeed='LOW')
                    elif msg == 'e':
                        print(f"Sending command to MOCO. |{msg}| ")
                        self.moco.rotate(direction='CLOCKWISE',
                                         drivetime=0.2, inputspeed='LOW')
                    elif msg == 'stop':
                        print(f"Sending command to MOCO. |{msg}| ")
                        self.moco.stop()
                        print(f"Sent command to MOCO. |{msg}| ")
                except Exception as e:
                    print(f"Exception occured: {e}")
                    print(e.with_traceback())


if __name__ == '__main__':
    print("Started program")
    client = Client()
    print("Created Client")
    client.start()
    print("Started Client")

    pipeline = queue.Queue(maxsize=5)
    event = threading.Event()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(client.handle_read, pipeline, event)
        executor.submit(client.handle_send, pipeline, event)

    # sendthread = Thread(target=client.handle_send, args=(), daemon=True)
    # readthread = Thread(target=client.handle_read, args=(), daemon=True)
    # # sendthread.start()
    # readthread.start()

    # run = True
    # while run:
    #     if readthread.join() != None:
    #         print(readthread.join())
