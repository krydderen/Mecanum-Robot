#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This class initializes and behaves like a server.
Its sole purpose is to handle the read and send 
functions. The send function sends a CMD to the client,
whereas the read method ( start )  handles the incoming
data as an image array, converts it to proper format.
The main module can then access the frame whenever it
is accessible.

Reference:
    https://realpython.com/documenting-python-code/
"""

from queue import Queue
from threading import Event
import threading
import cv2
import pickle
import socket
import struct
import sys
import logging
import numpy
import pygame
import numpy as np
from typing import NoReturn

# Initialize custom exception class


class DisconnectMsg(Exception):
    """Warning. Disconnecting client and shutting down."""


class Server(object):
    """
    A class used to represent a Server.
    The server will be initialized through ThreadPoolExecutor
    and runned as daemon. This means that as soon as the job is done, 
    the thread will terminate itself completely.
    Args:
        object ([type]): Socket Object which acts as an server.
    """

    def __init__(self):
        self.HEADER: int = 4086
        self.PORT: int = 8080
        self.FORMAT: str = 'utf-8'
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR: tuple = (self.SERVER, self.PORT)
        # - - - - Set basic logging config - - - - - - - -
        logging.basicConfig(format='%(asctime)s - %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        # - - - - Initialize socket and bind - - - - - - - -
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.info("[SERVER] Socket created.")
        self.server.settimeout(30)
        self.server.bind(self.ADDR)
        self.connected = False
        self.payload_size = struct.calcsize("L")
        self.conn = ''
        self.addr = ''
        self.frame = None
        self.canny = np.array([0])
        self.stop = False

    def stop(self):
        self.stop = True
        return
    
    def isconnected(self) -> bool:
        return self.connected
    
    def close(self) -> NoReturn:
        """
        Shuts the server down.
        """
        self.server.close()
        self.connected = False
        
    def get_canny(self) -> any:
            """
            Transforms the frame to suit the format
            of the GUI.
            Args:
                resolution (tuple): The set resolution we want
                the frame to be.

            Returns:
                any: The formatted frame.
            """
            if self.canny.any():
                return self.canny
            else:
                return np.array([0])
    def get_frame(self, resolution) -> any:
        """
        Transforms the frame to suit the format
        of the GUI.
        Args:
            resolution (tuple): The set resolution we want
            the frame to be.

        Returns:
            any: The formatted frame.
        """
        if self.frame != None:
            frame = pygame.transform.scale(self.frame, resolution)
            return frame
        else:
            return

    def start(self, queue: Queue, event: Event) -> None:
        """
        The method starts by listening for a client to connect.
        When a client connects, start receiving data from said client.
        After data is received, unpacks it and formats it to suit
        the GUI format. This also includes reversing the received array,
        rotating it, flipping it and sets it as the current given frame.

        Args:
            queue (Queue): [description]
            event (Event): [description]
        """
        self.server.listen()
        self.logger.info(f"Server is listening on {self.ADDR}")
        while not event.is_set() and not self.stop:
            data = b''
            try:
                self.conn, self.addr = self.server.accept()
                logging.debug("connection accepted.")
                self.connected = True
                logging.debug("self.connected = True.")
                logging.info(f"[NEW CONNECTION] {self.addr} connected.")
                
                #! dont use pickle over network
                while not event.is_set() and not self.stop:
                    self.conn.settimeout(2)
                    while len(data) < self.payload_size:
                        data += self.conn.recv(self.HEADER)
                    packed_msg_size = data[:self.payload_size]

                    data = data[self.payload_size:]
                    msg_size = struct.unpack("L", packed_msg_size)[0]
                    # logging.debug(f"recieved: {msg_size}")

                    while len(data) < msg_size:
                        data += self.conn.recv(self.HEADER)
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    pickledframe = pickle.loads(frame_data)
                    frame = cv2.flip(pickledframe, 0)
                    frame = cv2.flip(frame, 1)
                    frame = numpy.rot90(frame)
                    frame = frame[::-1]
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = pygame.surfarray.make_surface(frame)
                    
                    canny = cv2.flip(pickledframe, 0)
                    canny = cv2.flip(canny, 1)
                    # canny = numpy.rot90(canny)
                    canny = cv2.cvtColor(canny, cv2.COLOR_BGR2RGB)
                    blur  = cv2.GaussianBlur(canny, (5,5),1)
                    canny = cv2.Canny(blur,50,150)
                    
                    self.canny = canny
                    self.frame = frame
            except socket.timeout:
                print("deadlmao")
                event.set()
                
            self.close()

    def send(self, message: any) -> NoReturn:
        """
        Formats and sends the given CMD to the client. 

        Args:
            message (str): CMD, given in a format of
            'wasdqe' or 'stop'.

        Raises:
            DisconnectMsg: Raises custom exception if 
            a disconnect message is received.
        """
        try:
            senddata = pickle.dumps(message) # ! REWORK REMOVE PICKLE
            self.conn.send(senddata)
            logging.info(f"Sent {message} to client.")
        except DisconnectMsg as e:
            logging.info(e.__doc__)
            self.close()
        except Exception as e:
            logging.exception(
                f"[ERROR] Failed to send message to client. \n {e}")
