import pickle, socket, struct, time, logging, asyncio
import cv2
from threading import Thread
from WebcamVideoStream import CameraStream
from concurrent.futures import ThreadPoolExecutor
from functools import wraps



class Client(object):
    def __init__(self):
        self.HEADER  = 4086
        self.PORT    = 8080
        self.FORMAT  = 'utf-8'
        self.SERVER  = '192.168.43.18'
        self.SERVER  = socket.gethostbyname(socket.gethostname())
        self.ADDR    = (self.SERVER,self.PORT)
        self.socket  = None
        self.connected = False
    
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    def start(self):
        self.logger.info("Starting camera...")
        self.logger.debug(f"SERVER - {self.ADDR}")
        # self.cap = CameraStream().start()
        time.sleep(1)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.ADDR)
        self.connected = True
        self.logger.info(f"Successfully connected to {self.ADDR}")

    def disconnect(self):
        self.socket.close()
        self.cap.stop()
        self.logger.info(f"Successfully disconnected from {self.ADDR}")

    def handle_send(self):
        try:
            self.socket.settimeout(5)
            frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            data = pickle.dumps(frame)
            self.socket.sendall(struct.pack("i", len(data)) + data)
        except Exception as e:
            self.logger.exception(f"[ERROR] Closing.. {e}")

    def handle_read(self):
        """ 
        TODO: Handle how the client reads the response from server.
        ? Should the server only send the response as example w a s d? 
        ? Should the server format the response as JSON? Tuple? 
        TODO: Set up the protocol for the response handling.
        """
        data = self.socket.recv(self.HEADER) # ! Wait for this?
        
        
        if not data:
            return
        
        return data
        


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
    logging.debug("Started program")
    client = Client()
    logging.debug("Crated Client")
    client.start()
    logging.debug("Started Client")
    # sendthread = Thread(target=client.handle_send, args=(), daemon=True)
    readthread = Thread(target=client.handle_read, args=(), daemon=True)
    # sendthread.start()
    readthread.start()
    
    run = True
    while run:
        if readthread.join() != None:
            print(readthread.join())
