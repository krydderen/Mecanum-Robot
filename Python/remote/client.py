#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script for client class and its methods for both 
sending and recieving frames and user commands.

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
from time import sleep
from typing import NoReturn


class Client(object):
    """[summary]
    A class used to represent a client.
    The client will be initialized through ThreadPoolExecutor
    and runned as daemon. This means that as soon as the job is done, 
    the thread will terminate itself completely.
    Args:
        object ([type]): Socket Object which acts as an client.
    """

    def __init__(self):
        """
        Initialized parameters.

        HEADER : int

        """
        # TODO: DO THIS EVERYWHERE, GOOD CODING? ORRECT?
        self.HEADER : int = 4086
        self.PORT   : int = 8080
        self.FORMAT : str = 'utf-8'
        self.SERVER : str = '192.168.43.18'
        self.ADDR   : tuple = (self.SERVER, self.PORT)
        self.socket: any = None
        self.connected: bool = False
        # - - - - Set basic logging config - - - - - - - -
        logging.basicConfig(format='%(asctime)s - %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        # - - - - Initialize motor controller - - - - -
        self.drivetime = 0.2
        self.rc = Roboclaw("/dev/ttyS0", 38400)
        sleep(0.1)
        self.rc.Open()
        self.SPEED = 100

    def start(self) -> NoReturn:
        """
        Starts the camera, initializes the socket and connects to it.
        When done, sets the conenction to true.
        """
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
        """
        Shuts the videocapture down and closes the socket.
        """
        self.socket.close()
        self.cap.stop()
        self.thread.join()
        self.connected = False
        self.logger.info(f"Successfully disconnected from {self.ADDR}")
        # self.isrunning = true

    def handle_send(self, queue: Queue, event: Event) -> NoReturn:
        """[summary]
        The thread get called to loop here continously unless
        flagged not to. Its only purpose is to read and process the 
        image from the raspberry pi camera module. After it is read,
        convert it to GRAY to reduce amount of data sent.

        Args:
            queue (Queue): [description]
            event (Event): [description]

        Returns:
            NoReturn: [description]
        """
        while not event.is_set() and self.connected:
            try:
                cv2.waitKey(100)
                _, self.frame = self.cap.read()
                frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                data = pickle.dumps(frame)
                self.socket.sendall(struct.pack("L", len(data)) + data)
            except Exception as e:
                self.logger.exception(f"[ERROR] Closing.. {e}")
                event.set()
                break

    def handle_read(self, queue: Queue, event: Event) -> NoReturn:
        """
        The thread gets called to loop here continously unless 
        flagged not to. Its only purpose is to read and process data
        that comes in from the server. The CMDs received from the 
        server comes in form of aswdqe or 'stop'. After received, the
        msg is processed and passed into the if-statements to check
        what direction/move the robot should do next.

        Args:
            queue (Queue): [description]
            event (Event): [description]
        """
        while not event.is_set():
            
            
            try:
                data = self.socket.recv(self.HEADER)
                msg = pickle.loads(data)
                # ---------- Debugging ----------
                logging.info(f"Server sent data: {msg}")
                logging.debug(f"data: {data}")
                logging.debug(f"msg: {msg}")
                # -------------------------------
                if msg == 'w':
                    logging.debug(f"Sending command to MOCO. |{msg}| ")
                    self.rc.ForwardM1(0x80, self.SPEED)
                    self.rc.ForwardM1(0x81, self.SPEED)
                    self.rc.ForwardM2(0x80, self.SPEED)
                    self.rc.ForwardM2(0x81, self.SPEED)
                    logging.debug(f"Sent command to MOCO. |{msg}| ")
                elif msg == 'a':
                    logging.debug(f"Sending command to MOCO. |{msg}| ")
                    self.rc.BackwardM2(0x80, self.SPEED)
                    self.rc.ForwardM1(0x80, self.SPEED)
                    self.rc.ForwardM1(0x81, self.SPEED)
                    self.rc.BackwardM2(0x81, self.SPEED)
                    logging.debug(f"Sent command to MOCO. |{msg}| ")
                elif msg == 's':
                    logging.debug(f"Sending command to MOCO. |{msg}| ")
                    self.rc.BackwardM1(0x80, self.SPEED)
                    self.rc.BackwardM1(0x81, self.SPEED)
                    self.rc.BackwardM2(0x80, self.SPEED)
                    self.rc.BackwardM2(0x81, self.SPEED)
                    logging.debug(f"Sent command to MOCO. |{msg}| ")
                elif msg == 'd':
                    logging.debug(f"Sending command to MOCO. |{msg}| ")
                    self.rc.BackwardM1(0x80, self.SPEED)
                    self.rc.ForwardM2(0x80, self.SPEED)
                    self.rc.ForwardM2(0x81, self.SPEED)
                    self.rc.BackwardM1(0x81, self.SPEED)
                    logging.debug(f"Sent command to MOCO. |{msg}| ")
                elif msg == 'wd':
                    logging.debug(f"Sending command to MOCO. |{msg}| ")
                    self.rc.ForwardM2(0x80, self.SPEED)
                    self.rc.ForwardM2(0x81, self.SPEED)
                elif msg == 'wa':
                    logging.debug(f"Sending command to MOCO. |{msg}| ")
                    self.rc.ForwardM1(0x80, self.SPEED)
                    self.rc.ForwardM1(0x81, self.SPEED)
                elif msg == 'sd':
                    logging.debug(f"Sending command to MOCO. |{msg}| ")
                    self.rc.BackwardM1(0x80, self.SPEED)
                    self.rc.BackwardM1(0x81, self.SPEED)
                elif msg == 'sa':
                    logging.debug(f"Sending command to MOCO. |{msg}| ")
                    self.rc.BackwardM2(0x80, self.SPEED)
                    self.rc.BackwardM2(0x81, self.SPEED)
                elif msg == 'q':
                    logging.debug(f"Sending command to MOCO. |{msg}| ")
                    self.rc.BackwardM2(0x80, self.SPEED)
                    self.rc.ForwardM1(0x80, self.SPEED)
                    self.rc.ForwardM2(0x81, self.SPEED)
                    self.rc.BackwardM1(0x81, self.SPEED)
                elif msg == 'e':
                    logging.debug(f"Sending command to MOCO. |{msg}| ")
                    self.rc.BackwardM1(0x80, self.SPEED)
                    self.rc.ForwardM2(0x80, self.SPEED)
                    self.rc.ForwardM1(0x81, self.SPEED)
                    self.rc.BackwardM2(0x81, self.SPEED)
                elif msg == 'stop':
                    logging.debug(f"Sending command to MOCO. |{msg}| ")
                    self.rc.ForwardM1(0x80, 0)
                    self.rc.ForwardM2(0x80, 0)
                    self.rc.BackwardM1(0x80, 0)
                    self.rc.BackwardM2(0x80, 0)
                    self.rc.ForwardM1(0x81, 0)
                    self.rc.ForwardM2(0x81, 0)
                    self.rc.BackwardM1(0x81, 0)
                    self.rc.BackwardM2(0x81, 0)
                    logging.debug(f"Sent command to MOCO. |{msg}| ")
                if 'speed' == msg[0]:
                    logging.debug(f"Changing robotspeed. |{msg}| ")
                    self.SPEED = msg[1]
                # TODO: Test this method.
                elif msg == '!DISCONNECT':
                    logging.debug(f"Disconnecting..")
                    # event.set()
                    self.disconnect()
            except Exception as e:
                logging.debug(f"Exception occured: {e}")
                event.set()


# ---------- MAIN LOOP ----------
if __name__ == '__main__':
    # Set basic logging configuration.
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG)
    logging.debug("Started program")
    # Initialize the client object.
    client = Client()
    logging.debug("Created Client")
    client.start()
    logging.debug("Started Client")

    # Set up the threading environment with threadPoolExecutor.
    pipeline = queue.Queue(maxsize=5)
    event = threading.Event()
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     executor.submit(client.handle_read, pipeline, event)
    #     executor.submit(client.handle_send, pipeline, event)
    thread1 = threading.Thread(target=client.handle_read, args=(queue, event))
    thread2 = threading.Thread(target=client.handle_send, args=(queue, event))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
