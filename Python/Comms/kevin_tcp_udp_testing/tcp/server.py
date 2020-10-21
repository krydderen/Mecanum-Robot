import socket
import threading
import pickle

HEADER = 4096
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        try:
            conn.settimeout(10.0)
            msg_lenght = conn.recv(HEADER)
            if msg_lenght:
                msg_pickle = pickle.loads(msg_lenght)

                if msg_pickle == DISCONNECT_MESSAGE:
                    connected = False
                    
                print(f"[{addr}] {msg_pickle}")
                send_pickle_msg = pickle.dumps("[SERVER] Msg recieved.")
                conn.send(send_pickle_msg)
        except Exception as e:
            print(f"[SERVER] [SOCKET - {addr[1]}] [ERROR] {e}. Closing socket.")
            connected = False
        finally:
            pass
    # print(f"[SERVER] [SOCKET - {addr[1]}] Closing socket..")    
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        try:
            server.settimeout(20.0)
            conn, addr = server.accept()
            server.settimeout(None)
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        except socket.timeout:
            print(f"[SERVER] [ERROR] No connections found. Closing server..")
            break
    server.close()
        
print("[STARTING] Server is starting...")
start()