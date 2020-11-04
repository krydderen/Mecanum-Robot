#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""[summary]
CLIENT DOCCCC
- - S C R I P T  D O C S T R I N G  W I P - -
Reference:
    https://realpython.com/documenting-python-code/
"""
import pickle
from queue import Queue
import socket
import struct
from threading import Event
import time
import logging
import threading
import queue
import cv2
from roboclaw_3 import Roboclaw
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import NoReturn


class Client(object):
    def __init__(self):
        # TODO: DO THIS EVERYWHERE, GOOD CODING? ORRECT?
        self.HEADER : int = 4086
        self.PORT   : int = 8080
        self.FORMAT : str = 'utf-8'
        self.SERVER : str = '192.168.43.18'
        # self.SERVER  = socket.gethostbyname(socket.gethostname())
        self.ADDR   = (self.SERVER, self.PORT)
        self.socket = None
        self.connected = False
        # - - - - Set basic logging config - - - - - - - -
        logging.basicConfig(format='%(asctime)s - %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        # - - - - Initialize motor controller - - - - -
        self.drivetime = 0.2
        # self.moco = MotorController()
        self.rc = Roboclaw("/dev/ttyS0", 38400)
        sleep(0.1)
        self.rc.Open()

    def start(self) -> NoReturn:
        self.logger.info("Starting camera...")
        self.logger.debug(f"SERVER - {self.ADDR}")
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 256)
        self.cap.set(4, 144)
        _, self.frame = self.cap.read()
        time.sleep(1)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.ADDR)
        self.connected = True
        self.logger.info(f"Successfully connected to {self.ADDR}")

    def disconnect(self) -> NoReturn:
        self.connected = False
        self.socket.close()
        self.cap.stop()
        self.logger.info(f"Successfully disconnected from {self.ADDR}")

    def handle_send(self, queue: Queue, event: Event) -> NoReturn:
        while not event.is_set():
            while self.connected:
                try:
                    # self.socket.settimeout(5)
                    # logging.debug("Reading frame..")
                    cv2.waitKey(100)  # delay
                    _, self.frame = self.cap.read()
                    frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    data = pickle.dumps(frame)
                    self.socket.sendall(struct.pack("L", len(data)) + data)
                    # logging.debug(f"sent: {len(data)}")
                except Exception as e:
                    self.logger.exception(f"[ERROR] Closing.. {e}")
                    break

    def handle_read(self, queue: Queue, event: Event) -> NoReturn:
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
                    logging.info(f"Server sent data: {msg}")
                    logging.debug(f"data: {data}")
                    logging.debug(f"msg: {msg}")
                    # !DEBUG-END
                    if msg == 'w':
                        logging.debug(f"Sending command to MOCO. |{msg}| ")
                        # self.moco.forward(
                        #     drivetime=0.2, inputspeed='LOW')
                        self.rc.ForwardM1(0x80, 64)
                        self.rc.ForwardM1(0x81, 64)
                        self.rc.ForwardM2(0x80, 64)
                        self.rc.ForwardM2(0x81, 64)
                        logging.debug(f"Sent command to MOCO. |{msg}| ")
                    elif msg == 'a':
                        logging.debug(f"Sending command to MOCO. |{msg}| ")
                        # self.moco.left(drivetime=0.2,
                        #                inputspeed='LOW')
                        self.rc.BackwardM2(0x80,64)
                        self.rc.ForwardM1(0x80,64)
                        self.rc.ForwardM1(0x81,64)
                        self.rc.BackwardM2(0x81,64)
                        logging.debug(f"Sent command to MOCO. |{msg}| ")
                    elif msg == 's':
                        logging.debug(f"Sending command to MOCO. |{msg}| ")
                        # self.moco.backward(
                        #     drivetime=0.2, inputspeed='LOW')
                        self.rc.BackwardM1(0x80, 64)
                        self.rc.BackwardM1(0x81, 64)
                        self.rc.BackwardM2(0x80, 64)
                        self.rc.BackwardM2(0x81, 64)
                        logging.debug(f"Sent command to MOCO. |{msg}| ")
                    elif msg == 'd':
                        logging.debug(f"Sending command to MOCO. |{msg}| ")
                        # self.moco.right(
                        #     drivetime=0.2, inputspeed='LOW')
                        self.rc.BackwardM1(0x80,64)
                        self.rc.ForwardM2(0x80,64)
                        self.rc.ForwardM2(0x81,64)
                        self.rc.BackwardM1(0x81,64)
                        logging.debug(f"Sent command to MOCO. |{msg}| ")
                    elif msg == 'wd':
                        logging.debug(f"Sending command to MOCO. |{msg}| ")
                        # self.moco.wddiagonal(
                        #     drivetime=0.2, inputspeed='LOW')
                        self.rc.ForwardM2(0x80, 64)
                        self.rc.ForwardM2(0x81, 64)
                    elif msg == 'wa':
                        logging.debug(f"Sending command to MOCO. |{msg}| ")
                        # self.moco.wadiagonal(
                        #     drivetime=0.2, inputspeed='LOW')
                        self.rc.ForwardM1(0x80, 64)
                        self.rc.ForwardM1(0x81, 64)
                    elif msg == 'sd':
                        logging.debug(f"Sending command to MOCO. |{msg}| ")
                        # self.moco.sddiagonal(
                        #     drivetime=0.2, inputspeed='LOW')
                        self.rc.BackwardM1(0x80, 64)
                        self.rc.BackwardM1(0x81, 64)
                    elif msg == 'sa':
                        logging.debug(f"Sending command to MOCO. |{msg}| ")
                        # self.moco.sadiagonal(
                        #     drivetime=0.2, inputspeed='LOW')
                        self.rc.BackwardM2(0x80, 64)
                        self.rc.BackwardM2(0x81, 64)
                    elif msg == 'q':
                        logging.debug(f"Sending command to MOCO. |{msg}| ")
                        # self.moco.rotate(direction='COUNTER_CLOCKWISE',
                        #                  drivetime=0.2, inputspeed='LOW')
                        self.rc.BackwardM2(0x80, 64)
                        self.rc.ForwardM1(0x80, 64)
                        self.rc.ForwardM2(0x81, 64)
                        self.rc.BackwardM1(0x81, 64)
                    elif msg == 'e':
                        logging.debug(f"Sending command to MOCO. |{msg}| ")
                        # self.moco.rotate(direction='CLOCKWISE',
                        #                  drivetime=0.2, inputspeed='LOW')
                        self.rc.BackwardM1(0x80, 64)
                        self.rc.ForwardM2(0x80, 64)
                        self.rc.ForwardM1(0x81, 64)
                        self.rc.BackwardM2(0x81, 64)
                    elif msg == 'stop':
                        logging.debug(f"Sending command to MOCO. |{msg}| ")
                        # self.moco.stop()
                        self.rc.ForwardM1(0x80,0)
                        self.rc.ForwardM2(0x80,0)
                        self.rc.BackwardM1(0x80,0)
                        self.rc.BackwardM2(0x80,0)
                        self.rc.ForwardM1(0x81,0)
                        self.rc.ForwardM2(0x81,0)
                        self.rc.BackwardM1(0x81,0)
                        self.rc.BackwardM2(0x81,0)
                        logging.debug(f"Sent command to MOCO. |{msg}| ")
                        
                    # TODO: Test this method.
                    # elif msg == '!DISCONNECT':
                    #     logging.debug(f"Disconnecting..")
                    #     self.disconnect()                        
                except Exception as e:
                    logging.debug(f"Exception occured: {e}")
                    logging.debug(e.with_traceback())


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG)
    logging.debug("Started program")
    client = Client()
    logging.debug("Created Client")
    client.start()
    logging.debug("Started Client")

    pipeline = queue.Queue(maxsize=5)
    event = threading.Event()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(client.handle_read, pipeline, event)
        executor.submit(client.handle_send, pipeline, event)