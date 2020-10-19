# Importing package
import pickle
import socket
import struct
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time


class Server:
    """This class is a TCP server.
    """
    
    capture = None
    camera = None
    rawCapture = None
    
    def __init__(self, host="0.0.0.0", port=8000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
        self.addr = None
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size =(640,480))
        time.sleep(0.1)

if __name__ == '__main__':
    
    server = Server()
    
    # capture frames from the camera
    for frame in server.camera.capture_continuous(server.rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        # show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        server.rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        
        