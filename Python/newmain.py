# Importing package
import socket
from threading import Thread
import time

class Client(Thread):
    """Client class
    Client communicatin with Server through socket connection.

    Args:
        Thread ([type]): [description]
    """
    def __init__(self, host= 'localhost', port = 8000, rate = 0.5):
        Thread.__init__(self)
        self.addr = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = True
        self.rate = rate
        self.terminate = False
        
    def connect(self):
        """Establish a secure connection to server.
        """
        try: 
            self.socket.connect(self.addr)
        except OSError:
            pass
        finally:
            self.is_connected = True
            
    def disconnect(self):
        """Close connection.
        """
        self.terminate = True
        Thread.join(self)
        self.socket.close()
        