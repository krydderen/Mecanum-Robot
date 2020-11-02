from threading import Thread
import cv2


class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object with a dedicated thread
    """

    def __init__(self, src=0):
        self.steam = cv2.VideoCapture(src)
        (self.grapped, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        while not self.stopped:
            if not self.grapped:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True
