import os
import re
import cv2
import numpy as np
from tqdm import tqdm_notebook
import matplotlib.pyplot as plt


def CannyEdge(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    cannyImage = cv2.Canny(blur, 50, 150)
    return cannyImage


def region_of_interest(image, resolution, percent):

    polygon = np.array([[0, resolution[1]], [0, int(resolution[1]/percent)],
                        [resolution[0], int(resolution[1]/percent)], [resolution[0], resolution[1]]])
    mask = np.zeros_like(image)
    cv2.fillConvexPoly(mask, polygon, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


resolution = (640, 480)
cap = cv2.VideoCapture(0)
cap.set(3, resolution[0])
cap.set(4, resolution[1])
percent = 1.2
while True:
    _, frame = cap.read()

    canny = CannyEdge(frame)
    cropped_image = region_of_interest(canny, resolution, percent)
    roi = region_of_interest(frame, resolution, 2)

    cv2.imshow("Feed", frame)
    cv2.imshow("ROI", cropped_image)

    if cv2.waitKey(1) == ord("q"):
        cv2.destroyAllWindows
        break

cap.release()
