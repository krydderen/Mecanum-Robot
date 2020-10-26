"""UDP client communication protocol"""
import socket
import threading
import pickle

HEADER = 4096
PORT = 20001
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.43.18'
ADDR = (SERVER,PORT)

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
try:
    UDPClientSocket.settimeout(10.0)
    # Send to server using created UPD socket
    bytestosend = "Hello UDP SERVER!"
    UDPClientSocket.sendto(bytestosend.encode(FORMAT), ADDR)

    # Recieve response from server
    msgFromServer = UDPClientSocket.recvfrom(HEADER)
    print(f"[SERVER] {msgFromServer}")

    input('Press enter to disconnect.')

    # Send to server using created UPD socket
    bytestosend = "!DISCONNECT"
    UDPClientSocket.sendto(bytestosend.encode(FORMAT), ADDR)
    
except Exception as e:
    UDPClientSocket.close()
