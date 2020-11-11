import cv2
import numpy as np


def __init__(self):
    self.make_points = (0, 0)
    self.average_slope_intercept = (0, 0)
    self.CannyEdge = None
    self.region_of_interest = None
    self.display_lines = None


def make_points(image, line_parameters):
    try:
        slope, intercept = line_parameters
    except TypeError:
        slope, intercept = 0.001, 0
    y1 = image.shape[0]
    y2 = int(y1*3/5)
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    if lines is None:
        return None
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_points(image, left_fit_average)
    right_line = make_points(image, right_fit_average)
    return np.array((left_line, right_line))


def CannyEdge(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    cannyImage = cv2.Canny(blur, 50, 150)
    return cannyImage


def region_of_interest(image):
    height = image.shape[0]
    triangle = np.array(
        [[(200, height), (550, 250), (1100, height), ]])  # Adjust variabels for better line detection
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, triangle, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)
    return line_image


#cap = WebCamVideoStream().start()
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()

    canny = CannyEdge(frame)
    cropped_image = region_of_interest(canny)
    rho = 2
    theta = np.pi/180
    threshold = 100
    lines = cv2.HoughLinesP(cropped_image, rho, theta, threshold, np.array(
        []), minLineLength=40, maxLineGap=5)
    average_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, average_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

    cv2.imshow("Image", combo_image)
    if cv2.waitKey(1) == ord("q"):
        cv2.destroyAllWindows
        break

cap.stop()
