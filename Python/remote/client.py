import pickle, socket, struct, time, logging, threading, queue
import numpy as np
import cv2
from WebcamVideoStream import CameraStream
from concurrent.futures import ThreadPoolExecutor
from functools import wraps



class Client(object):
    def __init__(self):
        self.HEADER  = 4086
        self.PORT    = 8080
        self.FORMAT  = 'utf-8'
        self.SERVER  = '192.168.43.18'
        # self.SERVER  = socket.gethostbyname(socket.gethostname())
        self.ADDR    = (self.SERVER,self.PORT)
        self.socket  = None
        self.connected = False
        
    
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    def start(self):
        self.logger.info("Starting camera...")
        self.logger.debug(f"SERVER - {self.ADDR}")
        # self.cap = CameraStream().start()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 256)
        self.cap.set(4, 144)
        _,self.frame=self.cap.read()
        time.sleep(1)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.ADDR)
        self.connected = True
        self.logger.info(f"Successfully connected to {self.ADDR}")

    def disconnect(self):
        self.connected = False
        self.socket.close()
        self.cap.stop()
        self.logger.info(f"Successfully disconnected from {self.ADDR}")

    def handle_send(self, queue, event):
        while not event.is_set():
            while self.connected:
                try:
                    # self.socket.settimeout(5)
                    logging.debug("Reading frame..")
                    cv2.waitKey(100) #delay
                    _,self.frame = self.cap.read()
                    frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    data = pickle.dumps(frame)
                    self.socket.sendall(struct.pack("L", len(data)) + data)
                    logging.debug(f"sent: {len(data)}")
                except Exception as e:
                    self.logger.exception(f"[ERROR] Closing.. {e}")
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
                data = self.socket.recv(self.HEADER) # ! Wait for this?
                msg = pickle.loads(data)
                logging.info(f"Server sent data: {msg}")
                
                # if not data:
                    # return
                
                # return data
        


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.INFO)
    logging.debug("Started program")
    client = Client()
    logging.debug("Created Client")
    client.start()
    logging.debug("Started Client")
    
    pipeline    = queue.Queue(maxsize = 5)
    event       = threading.Event()
    with ThreadPoolExecutor(max_workers = 2) as executor:
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
