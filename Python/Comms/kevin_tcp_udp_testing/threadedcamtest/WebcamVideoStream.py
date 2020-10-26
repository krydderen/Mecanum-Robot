from threading import Thread
from imutils.video import VideoStream

class WebcamVideoStream:
    def __init__(self,usePiCamera=True, resolution=(640,480), framerate=24):
        # Initialize the video camera stream and read the first frame
        # from the stream.
        self.picamera = VideoStream(usePiCamera, resolution, framerate)
        (self.grabbed, self.frame) = self.picamera.read()
        
        # Initialize the variable used to indicate if the thread should be stopped.
        self.stopped = False
        
    def start(self):
        # Start the thread to read frames from the VideoStream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Keep the loop infinitly untill the thread is stopped        
        while True:
            # If the thread indicator variable is set, stop the frame
            if self.stopped:
                break
        # Otherwise, read the next frame from the stream
        (self.grabbed, self.frame) = self.picamera.read()
        
    def read(self):
        # Return the frame most recently read
        return self.frame
    
    def stop(self):
        # Indicate that the thread should be stopped.
        self.stopped = True
        