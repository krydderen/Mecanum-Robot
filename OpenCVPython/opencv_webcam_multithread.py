from threading import Thread, Lock
import cv2
face_Cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                     'haarcascade_frontalface_default.xml')
eye_Cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                    'haarcascade_eye.xml')


class WebCamVideoStream:
    def __init__(self, src=0, width=320, height=240):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, width)
        self.stream.set(4, height)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self):
        if self.started:
            print("Allready started!!")
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


if __name__ == "__main__":

    vs = WebCamVideoStream().start()
    while True:
        _, frame = vs.read()

        """
        Start of facial detection
        """
        # TODO Try with facial detection in its own thread? Even faster?

        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_Cascade.detectMultiScale(frameGray, 1.1, 4)
        eyes = eye_Cascade.detectMultiScale(frameGray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 2)
        """
        End of facial detection
        """

        cv2.imshow('webcam', frame)
        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows
            break

    vs.stop()
