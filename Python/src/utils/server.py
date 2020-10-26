import cv2, pickle, socket, struct, sys, logging
from threading import Thread

class Server(object):
    def __init__(self):
        self.HEADER  = 4086
        self.PORT    = 8080
        self.FORMAT  = 'utf-8'
        self.SERVER  = socket.gethostbyname(socket.gethostname())
        self.ADDR    = (self.SERVER,self.PORT)
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        self.logger = logging.getLogger(__name__)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        self.logger.info("[SERVER] Socket created.")    
        self.server.bind(self.ADDR)

        self.data = b''
        self.payload_size = struct.calcsize("i")
        
    def handle_client(self, conn, addr):
        self.logger.info(f"[NEW CONNECTION] {addr} connected.")
        
        while True:
            try:
                conn.settimeout(5)
                while len(self.data) < self.payload_size:
                    self.data += conn.recv(self.HEADER)
                packed_msg_size = self.data[:self.payload_size]

                data = self.data[self.payload_size:]
                msg_size = struct.unpack("i", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += conn.recv(self.HEADER)
                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame=pickle.loads(frame_data)
                print(frame.size)
                cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
                cv2.resizeWindow('frame', 640,480)
                cv2.imshow('frame', frame)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
                
            except Exception as e:
                self.logger.info(f"[ERROR] Closing.. {e}")
                break    
        conn.close()     
        
    def start(self):
        self.server.listen(10)
        self.logger.info(f"Server is listening on {self.ADDR}")
        while True:
            try:
                conn, addr = self.server.accept()
                self.thread = Thread(target=self.handle_client, args=(conn, addr))
                self.thread.start()
                self.logger.info(f"[ACTIVE CONNECTIONS] {self.thread.active_count() - 1}")
            except Exception as e:
                self.logger.exception("Exception occured.")
                break
        self.server.close()

    def close(self):
        self.server.close()