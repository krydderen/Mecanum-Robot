import pickle, socket, struct, time, cv2, logging
from threading import Thread
from WebcamVideoStream import CameraStream



class Client(object):
    def __init__(self):
        self.HEADER  = 4086
        self.PORT    = 8080
        self.FORMAT  = 'utf-8'
        self.SERVER  = '192.168.43.18'
        self.ADDR    = (self.SERVER,self.PORT)
        self.socket  = None
        self.connected = False
        
    
def startcam(self):
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info("Starting camera...")
    self.cap = CameraStream().start()
    # time.sleep(1)
        
def connect(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.connect(self.ADDR)
    self.connected = True
    logging.info(f"Successfully connected to {self.ADDR}")

def disconnect(self):
    self.socket.close()
    self.cap.stop()
    logging.info(f"Successfully disconnected from {self.ADDR}")

def handle_send(self):
    try:
        self.socket.settimeout(5)
        frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        data = pickle.dumps(frame)
        self.socket.sendall(struct.pack("i", len(data)) + data)
    except Exception as e:
        logging.exception(f"[ERROR] Closing.. {e}")
        
def handle_read(self):
    data = self.recv(self.HEADER)
    if not data:
        return



    
    