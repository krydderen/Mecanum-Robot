from threading import Thread, Lock
from imutils.video import VideoStream

import cv2


class CameraStream(object):
    def __init__(self, src=0):
        # self.stream = cv2.VideoCapture(src)
        # self.stream.set(3, 640)
        # self.stream.set(4, 480)
        
        self.picamera = VideoStream(usePiCamera=True, resolution=(640,480),framerate=32).start()
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self):
        if self.started:
            print("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self):
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()