import cv2
# Image
print("package imported bitch")

img = cv2.imread("OpenCVPython/lena.png")
# grayscale conversion
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# Blur
imgBlur = cv2.GaussianBlur(imgGray,(7,7),0)
# Edgedetection
imgCanny = cv2.Canny(img,100,100)
# Shows the image
cv2.imshow("Output", img)
cv2.imshow("Gray Image", imgGray)
cv2.imshow("Blur Image",imgBlur)
cv2.imshow("Canny Image", imgCanny)
cv2.waitKey(0)


# Video
cap = cv2.VideoCapture("OpenCVPython/tes_video.mp4")

while True:
    success, img2 = cap.read()
    cv2.imshow("Video", img2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Camera capture
cap2 = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)

while True:
    success, img3 = cap2.read()
    cv2.imshow("Capture", img3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
