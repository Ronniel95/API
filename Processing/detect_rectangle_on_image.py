__author__ = 'gregory'
import cv2
import numpy as np
import math
import time


class ContoursRecognition:
    """Defines contours of the bill on image.
    Doesn't work if the bill color and background color is black.
    """
    _MEDIAN_BLUR_SIZE = 15
    _ADAPTIVE_THRESHOLD_SIZE = 9
    _ADAPTIVE_THRESHOLD_CONST = 3
    _WHITE_THRESHOLD = 173.45390

    def __init__(self, image):
        """Internal initialization.
        image - what image to process
        """
        self.big_countor = np.array([])
        self.img_area_max = 0.95 * image.shape[0] * image.shape[1]
        self.img_area_min = 0.25 * self.img_area_max
        self.blurred = image
        self.is_background_white = False
        self.is_white = False

    def check_white_background(self):
        gray = cv2.cvtColor(self.blurred, cv2.COLOR_BGR2GRAY)
        average = self.blurred.mean()
        self.is_white = average > self._WHITE_THRESHOLD
        return average

    def cut_img_by_contour(self, binary_img):
        """Cutting the bill by contour on binarized image.
        binary_img - image on which binarization has been performed
        returns binary image in this contour
        """

        if self.big_countor.size:
            x, y, w, h = cv2.boundingRect(self.big_countor)
            contour = np.array([[[elem[0][0] - x, elem[0][1] - y]] for elem in self.big_countor])
            mask = np.zeros((h, w), np.uint8)
            # CV_FILLED fills the connected components found
            cv2.drawContours(mask, [contour], -1, 255, cv2.cv.CV_FILLED)
            bool_mask = np.array(mask, dtype=bool)
            crop = np.zeros((h, w), np.uint8)
            # set background to white
            crop.fill(255)
            #// and copy the magic apple
            np.copyto(crop, binary_img[y:y + h, x:x + w], where=bool_mask)
            return crop


            # // normalize so imwrite(...)/imshow(...) shows the mask correctly!
            # normalize(mask.clone(), mask, 0.0, 255.0, CV_MINMAX, CV_8UC1);



    def find_bill_contour(self):
        """Main function, it tries to find contours of the bill."""
        self.extract_contour_by_channels()
        if not self.big_countor.size:
            self.extract_contour_by_gray()
        if not self.big_countor.size:
            self.check_white_background()
        return self.big_countor


    def is_chosen_best_contour(self, gray_image):
        """Defines if contour is extracted succesfully on pre-filtered image.
        Mutual function for two methods of contour extraction.
        gray_image - image in gray scale
        """

        thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                       self._ADAPTIVE_THRESHOLD_SIZE, self._ADAPTIVE_THRESHOLD_CONST)  # 9 3
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(opening.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        is_founded = False
        for contour in contours:
            if is_founded: break  # approximate contour with accuracy proportional
            # to the contour perimeter
            approx = cv2.approxPolyDP(contour, cv2.arcLength(contour, True) * 0.02, True)
            # Note: absolute value of an area is used because
            # area may be positive or negative - in accordance with the
            # contour orientation
            contour_area = abs(cv2.contourArea(approx))
            if len(approx) == 4 and self.img_area_min < contour_area < self.img_area_max and cv2.isContourConvex(
                    approx):
                maxCosine = 0
                for j in range(2, 5):
                    cosine = abs(self.angle(approx[j % 4][0], approx[j - 2][0], approx[j - 1][0]))
                    if cosine > maxCosine:
                        maxCosine = cosine
                if maxCosine < 0.5:
                    self.big_countor = approx
                    is_founded = True
        return is_founded

    def extract_contour_by_gray(self):
        """Converting to grayscale and searching for contour
        """
        self.blurred = cv2.medianBlur(self.blurred.copy(), 9)
        gray = cv2.cvtColor(self.blurred, cv2.COLOR_BGR2GRAY)
        self.is_chosen_best_contour(gray)


    def extract_contour_by_channels(self):
        """Searching for contour by each channel.
        """
        self.blurred = cv2.medianBlur(self.blurred.copy(), 15)
        channels = cv2.split(self.blurred)
        for gray in channels:
            if self.is_chosen_best_contour(gray): break

    def angle(self, pt1, pt2, pt0):
        dx1 = pt1[0] - pt0[0]
        dy1 = pt1[1] - pt0[1]
        dx2 = pt2[0] - pt0[0]
        dy2 = pt2[1] - pt0[1]
        vec1 = [dx1 / math.sqrt(dx1 * dx1 + dy1 * dy1), dy1 / math.sqrt(dx1 * dx1 + dy1 * dy1)]
        vec2 = [dx2 / math.sqrt(dx2 * dx2 + dy2 * dy2), dy2 / math.sqrt(dx2 * dx2 + dy2 * dy2)]
        return vec1[0] * vec2[0] + vec1[1] * vec2[1]



if __name__ == '__main__':
    start = time.clock()
    input_file = "resized_test6.jpg"
    bin_input = "bin_by_class_test3.jpg"
    bin_image = cv2.imread(bin_input, cv2.IMREAD_GRAYSCALE)
    image = cv2.imread(input_file)
    copy_img = image.copy()
    output_file = "countored_" + input_file
    output_bin_file = "bin_" + output_file
    cr = ContoursRecognition(image)
    square = cr.find_bill_contour()
    if square.size:
        cv2.drawContours(copy_img, [square], -1, (0, 255, 0), 2)
        cv2.imwrite(output_file, copy_img)
        #cut_contoured_img = cr.cut_img_by_contour(bin_image)
        #cv2.imwrite(output_bin_file, cut_contoured_img)
    else:
        print output_file, "without square"
    print time.clock() - start

    # cut image by contours
    # http://bytefish.de/blog/extracting_contours_with_opencv/

    # used code for detecting
    # http://stackoverflow.com/questions/23059900/detecting-squares-in-an-image
    # http://stackoverflow.com/questions/8667818/opencv-c-obj-c-detecting-a-sheet-of-paper-square-detection/8863060#8863060
    # http://stackoverflow.com/questions/13523837/find-corner-of-papers/13532779#13532779
"""
def find_biggest_square(image):
    # blur will enhance edge detection
    big_countor = np.array([])
    max_countor_area = 0
    img_area_max = 0.95 * image.shape[0] * image.shape[1]
    img_area_min = 0.25 * img_area_max
    blurred = cv2.medianBlur(image, 15)
    channels = cv2.split(blurred)
    is_founded = False
    for bin_image in channels:
        if is_founded: break
        thresh = cv2.adaptiveThreshold(bin_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 3)  # 9 3
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(opening.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if is_founded: break
            # approximate contour with accuracy proportional
            # to the contour perimeter
            approx = cv2.approxPolyDP(contour, cv2.arcLength(contour, True) * 0.02, True)
            # Note: absolute value of an area is used because
            # area may be positive or negative - in accordance with the
            # contour orientation
            contour_area = abs(cv2.contourArea(approx))
            if len(approx) == 4 and img_area_min < contour_area < img_area_max and cv2.isContourConvex(approx):
                maxCosine = 0
                for j in range(2, 5):
                    cosine = abs(self.angle(approx[j % 4][0], approx[j - 2][0], approx[j - 1][0]))
                    if cosine > maxCosine:
                        maxCosine = cosine
                if maxCosine < 0.5 and contour_area > max_countor_area:
                    if contour_area > max_countor_area:
                        max_countor_area = contour_area
                        big_countor = approx
                        is_founded = True
    return big_countor
"""

'''
def find_square_other(image):
    big_countor = np.array([])
    max_countor_area = 0
    img_area_max = 0.95 * image.shape[0] * image.shape[1]
    img_area_min = 0.25 * img_area_max
    filtered = cv2.GaussianBlur(image, (9, 9), 3)
    filtered = cv2.medianBlur(filtered, 9)
    filtered = cv2.medianBlur(filtered, 9)
    if len(filtered.shape) == 3:
        bin_image = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    else:
        bin_image = filtered
    bitmap = cv.CreateImageHeader((bin_image.shape[1], bin_image.shape[0]), cv.IPL_DEPTH_8U, 1)
    cv.SetData(bitmap, bin_image.tostring(), bin_image.dtype.itemsize * 1 * bin_image.shape[1])
    cv.InRangeS(bitmap, (20), (100), bitmap)
    img = np.asarray(bitmap[:, :])
    contours, _ = cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


    for contour in contours:
        # approximate contour with accuracy proportional
        # to the contour perimeter
        approx = cv2.approxPolyDP(contour, cv2.arcLength(contour, True) * 0.02, True)
        # print abs(cv2.contourArea(contour))
        # Note: absolute value of an area is used because
        # area may be positive or negative - in accordance with the
        # contour orientation
        contour_area = abs(cv2.contourArea(approx))
        if len(approx) == 4 and img_area_min < contour_area < img_area_max and cv2.isContourConvex(approx):
            maxCosine = 0
            for j in range(2, 5):
                cosine = abs(angle(approx[j % 4][0], approx[j - 2][0], approx[j - 1][0]))
                if cosine > maxCosine:
                    maxCosine = cosine
            if maxCosine < 0.3 and contour_area > max_countor_area:
                if contour_area > max_countor_area:
                    max_countor_area = contour_area
                    big_countor = approx
    return big_countor
'''

