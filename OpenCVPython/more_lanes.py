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


def region_of_interest(image):

    return masked_image


cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()

    cv2.imshow("Feed", frame)
    #cv2.imshow("mask", mask)

    if cv2.waitKey(1) == ord("q"):
        cv2.destroyAllWindows
        break

cap.release()
