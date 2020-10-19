import socket
import threading
import pickle

HEADER = 4096
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '10.0.0.111'
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    pickled_msg = pickle.dumps(msg)
    client.send(pickled_msg)
    
send("Hello World")

print(f'{pickle.loads(client.recv(HEADER))}')

input()

send(DISCONNECT_MESSAGE)
client.close()