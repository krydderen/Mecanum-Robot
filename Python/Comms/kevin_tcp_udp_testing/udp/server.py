"""UDP server communication protocol"""
import socket
import threading
import pickle

HEADER = 4096
PORT = 20001
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

TESTMSG = "Hello UDP Client"
bytesToSend = str.encode(TESTMSG)

# Create a datagram socket 

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Brind to address and IP 

UDPServerSocket.bind(ADDR)

print(f"[UDP!SERVER] Server is listening on {SERVER}")

# Initialize address and message 
address = None
message = None

# Listen for incoming datagrams
listening = True
while(listening):
    try:
        UDPServerSocket.settimeout(10.0)
        bytesAddressPair = UDPServerSocket.recvfrom(HEADER)

        message = bytesAddressPair[0]

        address = bytesAddressPair[1]
    
        if message == b"!DISCONNECT":
            print(f"[CLIENT - {address}] Disconnected.")

        else:
            print(f"[CLIENT - {address}] {message.decode(FORMAT)}")
            # Sending a reply to client
            UDPServerSocket.sendto(bytesToSend, address)
        
        
    except Exception as e:
        print(f"[SERVER] [SOCKET - {address}] [ERROR] {e}. Closing socket.")
        listening = False
        
UDPServerSocket.close()
print(f"[SERVER] Closed.")