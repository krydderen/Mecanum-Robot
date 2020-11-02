
import numpy as np
from matplotlib import pyplot as pit
import cv2

# Cropping the image to the top part
img = cv2.imread("OpenCVPython/Fig0707(a)(Original).tif")
cv2.imshow("Figure",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

crop_img = img[30:130, 50:500]
cv2.imshow("Cropped",crop_img)
cv2.waitKey(0)
cv2.destroyAllWindows()