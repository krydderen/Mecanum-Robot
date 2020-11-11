import numpy as np
import cv2

# Capture frames from camera
cap = cv2.VideoCapture(0)

# loop runs if cap has been initialized
while (1):
    # Reads frames from a camera
    ret, frame = cap.read()
    # Converting BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define range of red color in HSV
    lower_red = np.array([30, 150, 50])
    upper_red = np.array([255, 255, 180])
    # Create a red HSV colour boundary and threshold HSV image
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Display an original image
    cv2.imshow('Original', frame)

    edges = cv2.Canny(frame, 100, 200)

    cv2.imshow('Edges', edges)
    if cv2.waitKey(1) == ord("q"):
        cv2.destroyAllWindows
        break

cap.release()

cv2.destroyAllWindows()

# TODO make use of threading, expand so there are triggers when edges are detected
