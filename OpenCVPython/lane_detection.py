import cv2
import numpy as np
import matplotlib.pyplot as plt

# TODO Something here doesn't work. There might be an error with conversion at some point.
# TODO Come back to this if you have time or can't find another solution

""" The cannny function calculates derivative in x and y directions, and according to that,
    we can see the changes in intensity value. Larger derivatives equal to High intensity(sharp changes),
    Smaller derivatives equal to Low intensity(shallow changes)
"""


def canny_edge_detector(image):

    # Convert the image color to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Reduce noise from the image
    blur = cv2.GaussianBlur(gray_image, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


""" Masking the canny image after finding the region of interest"""


def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([
                        [(200, height), (1100, height), (550, 250)]
                        ])
    mask = np.zeros_like(image)

    # Fill poly_function deals with multiple polygon
    image = cv2.fillPoly(mask, polygons, 255)

    # Bitwise operation between canny image and mask image
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


""" Find coordinates of the road lanes"""


def create_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3/5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


""" Differentiating left and right road lanes with the hellp of positivve and negative slopes
    respectively and appending them into the lists. If the slope is negative then the road lange 
    belongs to the left-hand side of the vehicle, and if the slope is positive then the road lane
    belongs to the right-hand side of the vehicle.
"""


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)

        # It will fit the polynomal and the intercept and slope
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = create_coordinates(image, left_fit_average)
    right_line = create_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])


"""
    Fitting the coordinates into the actual image and then return returning the image with the
    detected line(road with the detected lade):
"""


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
        return line_image


"""Firstly, the video file is read and decoded into frames and using Houghline method the straight line
    which is going through the image is detected. Then we call all the functions.
"""

# Path of tdataset directory
cap = cv2.VideoCapture('OpenCVPython/test2.mp4')
while True:
    _, frame = cap.read()
    canny_image = canny_edge_detector(frame)
    cropped_image = region_of_interest(canny_image)

    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]),
                            minLineLength=40, maxLineGap=5)

    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow("Results", combo_image)

    # When the below two will be true and will press the "q" on
    # our keyboard, we will break from the loop

    # wait 0 will wait for idefinetely between each frames.
    # 1ms will wait for the specified time only between each frames
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# close the video file
cap.release()

# destroy all the windows that is currently on
cv2.destroyAllWindows()
