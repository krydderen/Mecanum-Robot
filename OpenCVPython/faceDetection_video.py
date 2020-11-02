import cv2

face_Cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                     'haarcascade_frontalface_default.xml')
eye_Cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                    'haarcascade_eye.xml')


# Camera capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

while True:
    success, img = cap.read()
    capGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_Cascade.detectMultiScale(capGray, 1.1, 4)
    eyes = eye_Cascade.detectMultiScale(capGray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    for (x, y, w, h) in eyes:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)
    cv2.imshow("Capture", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break


# cv2.imshow("Result", img)
# cv2.waitKey(0)
