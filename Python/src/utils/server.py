import cv2, pickle, socket, struct, sys, logging
from threading import Thread

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
        self.server.bind(self.ADDR)
        self.connected = False
        self.payload_size = struct.calcsize("L")
        self.conn = ''
        self.addr = ''
        
    def handle_client(self, conn, addr):
        self.logger.info(f"[NEW CONNECTION] {addr} connected.")
        data = b''
        while True:
            try:
                conn.settimeout(10)
                while len(data) < self.payload_size:
                    data += conn.recv(self.HEADER)
                packed_msg_size = data[:self.payload_size]

                data = data[self.payload_size:]
                msg_size = struct.unpack("L", packed_msg_size)[0]
                logging.debug(f"recieved: {msg_size}")

                while len(data) < msg_size:
                    data += conn.recv(self.HEADER)
                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame=pickle.loads(frame_data)
                logging.debug(frame.size)
                cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
                cv2.resizeWindow('frame', 640,480)
                cv2.imshow('frame', frame)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    conn.close()
                    break
                
            except Exception as e:
                self.logger.info(f"[ERROR] Closing.. {e}")
                self.logger.debug(f"[DEBUG] {e.with_traceback()}")
                break    
        conn.close()     
        
    def start(self, queue, event):
        while not event.is_set():
            self.server.listen(10)
            self.logger.info(f"Server is listening on {self.ADDR}")
            self.conn, self.addr = self.server.accept()
            logging.debug("connection accepted.")
            self.connected = True
            logging.debug("self.connected = True.")
            self.handle_client(self.conn, self.addr)
            # try:
            #     self.thread = Thread(target=self.handle_client, args=(conn, addr), daemon=True)
            #     self.thread.name = "Handle Client Thread"
            #     # self.thread = Thread(target=self.send, args=(conn, addr), daemon=True)
            #     self.thread.start()
            #     self.logger.debug("Handle Client thread started.")
            #     # self.logger.debug("Sendthread started.")
            #     # self.logger.info(f"[ACTIVE CONNECTIONS] {self.threading.active_count() - 1}")
            # except Exception as e:
            #     self.logger.exception("Exception occured.")
            #     self.close()
            #     break
    

    def close(self):
        self.thread.join()
        self.connected = False
        self.server.close()
    
    def isconnected(self):
        return self.connected
    
    def send(self, message):
        try:
            # self.socket.settimeout(5)
            senddata = pickle.dump(message)
            self.conn.sendall(senddata)
            logging.info(f"Sent {message} to client.")
        except Exception as e:
            logging.exception(f"[ERROR] Failed to send message to client. \n {e}")
            # self.close()
            
            
            