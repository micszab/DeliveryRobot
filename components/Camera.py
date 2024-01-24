import cv2
import numpy as np

class Camera:
    def __init__(self, width=1024, height=768, fps=10):
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None

    def initialize_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 1)
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    def unwrap_fisheye(self, frame):
        h, w = frame.shape[:2]
        K = np.array([[330.91, 0.0, w / 2], [0.0, 330.91, h / 2], [0.0, 0.0, 1.0]])
        D = np.array([-0.21172, 0.123595, -0.00086417, -0.0004165])
        undistorted_frame = cv2.fisheye.undistortImage(frame, K, D, Knew=K)
        return undistorted_frame
    
    def moving_average(self, data, window_size):
        cumsum = np.cumsum(np.insert(data, 0, 0))
        return (cumsum[window_size:] - cumsum[:-window_size]) / float(window_size)

    def color_sidewalk(self, image):
        self.width = image.shape[1]
        self.height = image.shape[0]
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        #cv2.imshow('hsv_image', hsv_image)
        blurred = cv2.GaussianBlur(hsv_image, (7, 7), 0)
        #cv2.imshow('gaussian_blur', blurred)
        lower_threshold = np.array([50, 10, 95], dtype=np.uint8)
        upper_threshold = np.array([130, 40, 255], dtype=np.uint8)
        mask = cv2.inRange(blurred, lower_threshold, upper_threshold)
        #cv2.imshow('mask', mask)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        contour_image = np.zeros_like(image)
        #cv2.drawContours(contour_image, contours, -1, (0, 0, 150), cv2.FILLED)
        #cv2.imshow('contours', contour_image)

        max_value = float('-inf')
        min_value = float('inf')
        sidewalk_contours = []
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            if perimeter > 1000 and len(contour) > 800:
                x_values, y_values = contour[:, 0, 0], contour[:, 0, 1]

                for idx, y in enumerate(y_values):
                    if self.height - 30 <= y <= self.height - 10:
                        max_value = max(max_value, x_values[idx])
                        min_value = min(min_value, x_values[idx])

                smoothed_x = self.moving_average(x_values, window_size=10)
                smoothed_y = self.moving_average(y_values, window_size=10)
                smoothed_contour = np.column_stack((smoothed_x, smoothed_y))
                smoothed_contour = smoothed_contour.round().astype(int)
                sidewalk_contours.append(smoothed_contour)

        colored_image = np.zeros_like(image)
        if len(sidewalk_contours) > 0:
            cv2.drawContours(colored_image, sidewalk_contours, -1, (0, 0, 150), cv2.FILLED)

        sidewalk_gray = cv2.cvtColor(colored_image, cv2.COLOR_BGR2GRAY)
        _, sidewalk_mask = cv2.threshold(sidewalk_gray, 10, 150, cv2.THRESH_BINARY)
        non_sidewalk_mask = cv2.bitwise_not(sidewalk_mask)
        non_sidewalk_mask = cv2.cvtColor(non_sidewalk_mask, cv2.COLOR_GRAY2BGR)
        result = cv2.bitwise_or(cv2.bitwise_and(image, non_sidewalk_mask), colored_image)
        return result, min_value, max_value

    def run(self):
        image_path_1 = '../chodnik5.jpg'
        
        frame_1 = cv2.imread(image_path_1)
        sidewalk_frame_1, left_value, right_value = self.color_sidewalk(frame_1)
        print(f'left: {left_value}, right: {right_value}')

        cv2.imshow('org_1', frame_1)
        cv2.imshow('Sidewalk_1', sidewalk_frame_1)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def release_resources(self):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    camera = Camera()
    camera.run()
