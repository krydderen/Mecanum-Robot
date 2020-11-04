#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""[summary]
SERVER DOCSTRING
- - S C R I P T  D O C S T R I N G  W I P - -
Reference:
    https://realpython.com/documenting-python-code/
"""

from queue import Queue
from threading import Event
import threading
import cv2, pickle, socket, struct, sys, logging, numpy, pygame
from typing import NoReturn

class DisconnectMsg(Exception):
    """Warning. Disconnecting client and shutting down."""

class Server(object):
    def __init__(self):
        self.HEADER  = 4086
        self.PORT    = 8080
        self.FORMAT  = 'utf-8'
        self.SERVER  = socket.gethostbyname(socket.gethostname())
        self.ADDR    = (self.SERVER,self.PORT)
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.info("[SERVER] Socket created.")
        self.server.settimeout(30)
        self.server.bind(self.ADDR)
        self.connected = False
        self.payload_size = struct.calcsize("L")
        self.conn = ''
        self.addr = ''
        self.frame= None
    
    def close(self) -> NoReturn:
        self.server.close()
        self.thread.join()
        self.connected = False
    
    def get_frame(self, resolution):
        frame = pygame.transform.scale(self.frame, resolution)
        return frame
    
    def start(self, queue: Queue, event: Event) -> None:
        while not event.is_set():
            try: 
                self.server.listen()
                self.logger.info(f"Server is listening on {self.ADDR}")
                self.conn, self.addr = self.server.accept()
                logging.debug("connection accepted.")
                self.connected = True
                logging.debug("self.connected = True.")
                logging.info(f"[NEW CONNECTION] {self.addr} connected.")
                data = b''
            except self.server.timeout:
                self.close()
            while True:
                try:
                    self.conn.settimeout(10)
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

                    frame=pickle.loads(frame_data)
                    frame=cv2.flip(frame, 0)
                    frame=cv2.flip(frame, 1)
                    frame = numpy.rot90(frame)
                    frame = frame[::-1]
                    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    frame = pygame.surfarray.make_surface(frame)
                    self.frame = frame
                    
                except Exception as e:
                    self.logger.info(f"[ERROR] Closing.. {e}")
                    self.logger.debug(f"[DEBUG] {e.with_traceback()}")
        return
    
    def isconnected(self) -> bool:
        return self.connected
    
    def send(self, message: str) -> NoReturn:
        try:
            # self.socket.settimeout(5)
            if message == "!DISCONNECT":
                raise DisconnectMsg()
            senddata = pickle.dumps(message)
            self.conn.send(senddata)
            logging.info(f"Sent {message} to client.")
        except DisconnectMsg as e: # TODO: Test this method.
            logging.info(e.__doc__)
            self.close()
            # self.close()
        except Exception as e:
            logging.exception(f"[ERROR] Failed to send message to client. \n {e}")
            # self.close()
            
            
            