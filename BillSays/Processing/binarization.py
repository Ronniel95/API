import numpy as np
import cv2
from matplotlib import pyplot as plt
from change_resolution import resize_picture_dir, resize_picture_file, save_picture_orientation
from PIL import Image
from time import clock


class Binarization:
    _BIG_SIZE = 2012.0
    _SMALL_SIZE = 1006.0

    def __init__(self):
        self.bin_img = None

    def process_with_one_resizing_best(self, input_file, output_file):
        """Processing image:
        1. little resizing for speed
        2. binarization
        3. resizing for other parts of the pipeline
        """
        #img = resize_picture_dir(input_file, output_file, self._BIG_SIZE)
        img = save_picture_orientation(input_file)
        bin = self.binarize_big(img)
        pil_im = Image.fromarray(bin)
        pil_im = resize_picture_file(pil_im, self._SMALL_SIZE)
        self.bin_img = pil_im
        return self.bin_img

    def process_with_one_resizing(self, input_file, output_file):
        """Processing image:
        1. Big resizing for speed
        2. binarization
        """
        #img = resize_picture_dir(input_file, output_file, self._SMALL_SIZE)
        img = cv2.imread(input_file)
        bin = self.binarize_small(img)
        self.bin_img = bin
        return self.bin_img


    @staticmethod
    def binarize_big(img):
        """Performs transforming of the colored image to image with only white and black color."""
        # convert to grayscale
        # convert to grayscale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # add blur
        img = cv2.GaussianBlur(img, (5, 5), 1)
        img = cv2.blur(img, (5, 5), 1)
        # add bilateral filter
        img = cv2.bilateralFilter(img, 9, 75, 75)
        # adaptive thresholding
        # thresh6 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        thresh7 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        # Otsu's thresholding
        #ret2, thresh8 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # cv2.imwrite("tested.jpg", thresh7)
        return thresh7

    @staticmethod
    def binarize_small(img):
        """Performs transforming of the colored image to image with only white and black color."""
        # img = cv2.imread(input_file)
        # convert to grayscale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # add blur
        #img = cv2.GaussianBlur(img, (5, 5), 0.6)
        #img = cv2.blur(img, (3, 3), 0.3)
        # add bilateral filter
        img = cv2.bilateralFilter(img, 9, 75, 75)
        # adaptive thresholding
        # thresh6 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        thresh7 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 9, 3)
        # Otsu's thresholding
        # ret2, thresh8 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # cv2.imwrite(output_file, thresh7)
        return thresh7


if __name__ == '__main__':
    # input_file = "resized_test3.jpg"
    # output_file = "binarized/binarized_" + input_file
    # binarize_small(input_file, output_file)
    st = clock()
    input_file = "test3.jpg"
    output_file = "bin_by_class_1" + input_file
    binrztn = Binarization()
    binrztn.process_with_one_resizing_best(input_file, output_file)
    print clock() - st

    #binarize_big(input_file, output_file)
