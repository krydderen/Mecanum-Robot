import cv2
import numpy as np


class LaneDetection:
    def __init__(self):
        pass

    def make_points(self, image, line_parameters):
        try:
            slope, intercept = line_parameters
        except TypeError:
            slope, intercept = 0.001, 0
        y1 = image.shape[0]
        y2 = int(y1*3/5)
        x1 = int((y1 - intercept)/slope)
        x2 = int((y2 - intercept)/slope)
        return np.array([x1, y1, x2, y2])

    def average_slope_intercept(self, image, lines):
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
        left_line = self.make_points(image, left_fit_average)
        right_line = self.make_points(image, right_fit_average)
        return np.array((left_line, right_line))

    def CannyEdge(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        cannyImage = cv2.Canny(blur, 50, 150)
        return cannyImage

    def region_of_interest(self, image):
        height = image.shape[0]
        triangle = np.array(
            [[(50, height), (550, 250), (1100, height), ]])  # Adjust variabels for better line detection
        #polygon = np.array([[50, 270], [220, 160], [360, 160], [480, 270]])
        mask = np.zeros_like(image)
        cv2.fillPoly(mask, triangle, 255)
        # cv2.fillPoly(mask, polygon, 255)
        masked_image = cv2.bitwise_and(image, mask)
        return masked_image

    def display_lines(self, image, lines):
        line_image = np.zeros_like((image))
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                try:
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)
                except:
                    pass
        return line_image


if __name__ == "__main__":

    # cap = WebCamVideoStream().start()
    LD = LaneDetection()
    cap = cv2.VideoCapture(0)
    cv2.waitKey(1000)
    while True:
        _, frame = cap.read()

        canny = LD.CannyEdge(frame)
        cropped_image = LD.region_of_interest(canny)
        rho = 2
        theta = np.pi/180
        threshold = 100
        lines = cv2.HoughLinesP(cropped_image, rho, theta, threshold, np.array(
            []), minLineLength=40, maxLineGap=5)
        average_lines = LD.average_slope_intercept(frame, lines)
        line_image = LD.display_lines(frame, average_lines)
        combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

        cv2.imshow("Image", combo_image)
        cv2.imshow("ROI", cropped_image)
        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows
            break

    cap.release()
