from time import sleep
import cv2
import numpy as np
from numpy.core.numeric import cross
from tqdm import tqdm_notebook
import matplotlib.pyplot as plt
from threading import Event
from queue import Queue


# TODO implement it into the main program for the robot!
# TODO It should override the user input to avoid collisions with objects


class ObstacleDetection:
    def __init__(self):
        self.canny = np.array([0])


    def CannyEdge(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        cannyImage = cv2.Canny(blur, 50, 150)
        return cannyImage


    def region_of_interest(self, image, resolution, percent) -> any:
        polygon = np.array([[0, resolution[1]], [0, int(resolution[1]/percent)],
                            [int(resolution[0]/2), int(resolution[1]/percent)], [int(resolution[0]/2), resolution[1]]])
        mask = np.zeros_like(image)
        cv2.fillConvexPoly(mask, polygon, 255)
        masked_image = cv2.bitwise_and(image, mask)
        return masked_image


    def region_of_interest2(self, image, resolution, percent) -> any:
        polygon = np.array([[int(resolution[0]/2), resolution[1]], [int(resolution[0]/2), int(resolution[1]/percent)],
                            [resolution[0], int(resolution[1]/percent)], [resolution[0], resolution[1]]])
        mask = np.zeros_like(image)
        cv2.fillConvexPoly(mask, polygon, 255)
        masked_image = cv2.bitwise_and(image, mask)
        return masked_image


    def check_roi(self, image) -> bool:
        if image.any() > 0:
            return True
        else:
            return False

    def set_canny(self, canny):
        self.canny = canny

    def start(self, queue: Queue, event: Event):
        resolution = (256, 144)
        percent = 1.2
        while not event.is_set():
            sleep(1)
            if self.canny.any() > 0:
                cropped_image = self.region_of_interest(self.canny, resolution, percent)
                cropped_image2 = self.region_of_interest2(self.canny, resolution, percent)
                combo_image = cropped_image + cropped_image2
                
                # cv2.imshow("Feed", self.canny)
                # cv2.imshow("ROI", combo_image)
                
                # Checking activity in the roi's
                if self.check_roi(cropped_image) and self.check_roi(cropped_image2):
                    print('Back up bitch')
                    # TODO call on the commands of the controller to turn around 90 degrees
                elif self.check_roi(cropped_image):
                    print('On you left')
                    # TODO Turn about 45 degrees to the right
                elif self.check_roi(cropped_image2):
                    print('Spin me right round baby')
                    # TODO Turn about 45 degrees to the left
                else:
                    print('Dont you say it')
                    # TODO Nothing detected, do nothing


"""if __name__ == "__main__":
    resolution = (640, 480)
    cap = cv2.VideoCapture(0)
    cap.set(3, resolution[0])
    cap.set(4, resolution[1])
    percent = 1.2
    while True:
        _, frame = cap.read()

        canny = CannyEdge(frame)
        cropped_image = region_of_interest(canny, resolution, percent)
        cropped_image2 = region_of_interest2(canny, resolution, percent)
        combo_image = cropped_image + cropped_image2
        #roi = region_of_interest(frame, resolution, 2)

        cv2.imshow("Feed", frame)
        cv2.imshow("ROI", combo_image)
        #cv2.imshow("ROI2", cropped_image2)

        # Checking activity in the roi's
        if check_roi(cropped_image) and check_roi(cropped_image2):
            print('Back up bitch')
            # TODO call on the commands of the controller to turn around 90 degrees
        elif check_roi(cropped_image):
            print('On you left')
            # TODO Turn about 45 degrees to the right
        elif check_roi(cropped_image2):
            print('Spin me right round baby')
            # TODO Turn about 45 degrees to the left
        else:
            print('Dont you say it')
            # TODO Nothing detected, do nothing

        # Killswitch
        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows
            break

    cap.release()"""
