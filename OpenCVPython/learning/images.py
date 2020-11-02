import cv2
import numpy as np

img = cv2.imread("OpenCVPython/lena.png")
kernel = np.ones((5,5),np.uint8)
# grayscale conversion
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# Blur
imgBlur = cv2.GaussianBlur(imgGray,(7,7),0)
# Edgedetection
imgCanny = cv2.Canny(img,150,200)
# Dialation
imgDialation = cv2.dilate(imgCanny, kernel, iterations=1)
# Erotion
imgEroded = cv2.erode(imgDialation,kernel,iterations=1)
# Stack images together in a window. Number of dimensions must be the same
imgHor = np.hstack((img,img))
imgVer = np.vstack((img,img))

# Shows the image
cv2.imshow("Output", img)
cv2.imshow("Gray Image", imgGray)
cv2.imshow("Blur Image",imgBlur)
cv2.imshow("Canny Image", imgCanny)
cv2.imshow("Dialation Image", imgDialation)
cv2.imshow("Eroded Image", imgEroded)
cv2.imshow("Vertical",imgVer)
cv2.imshow("Horizontal", imgHor)
cv2.waitKey(0)