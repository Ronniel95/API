__author__ = 'gregory'

from detect_rectangle_on_image import ContoursRecognition
from comp_bin_rot_pipeline import CertainFunctionExecutor
from change_resolution import resize_picture_dir
from binarization import Binarization
from rotation import rotate_img
from find_words import findwords, drawRect
import cv2
import time
import numpy as np
from words_to_line import write_txt_bill_recognition


def fun_to_apply(inp_dir, file_name, out_dir):
    """Applying rectangle detection for one image in pipeline proccesing in
    Class CertainFunctionExecutor.
    """
    SIZE = 1006.0
    # constant for resizing the image
    inp_file = '/'.join([inp_dir, file_name])
    # the way for input file
    new_file_name = "proccessed_" + file_name
    debug_file_name = "debug_rotation_" + file_name
    # file_name for debug
    out_file = '/'.join([out_dir, new_file_name])
    # the way for output file
    debug_out_file = '/'.join([out_dir, debug_file_name])
    # the way where write debug file
    binrztn = Binarization()
    image = resize_picture_dir(inp_file, out_file, SIZE)
    bin_image = binrztn.process_with_one_resizing_best(inp_file, out_file)
    cr = ContoursRecognition(image)
    square = cr.find_bill_contour()
    if square.size:
        cv2.drawContours(image, [square], -1, (0, 255, 0), 2)
        cut_contoured_img = cr.cut_img_by_contour(bin_image)
        cut_contoured_img = rotate_img(cut_contoured_img)
        # cv2.imwrite(debug_out_file, cut_contoured_img)
        words, words_lists_per_line = findwords(cut_contoured_img)
        if words:
            drawRect(cut_contoured_img, words, out_file, (255, 0, 0))
            write_txt_bill_recognition(out_file + '.txt', words_lists_per_line)
        else:
            print file_name, "without contours"
        #cv2.imwrite(out_file, cut_contoured_img)
    elif(not square and not cr.is_white):
    # TODO: loging on server
        print file_name, "without square and probably not white"
    elif(not square and cr.is_white):
    # TODO: loging on server
        words, words_lists_per_line = findwords(bin_image)
        if words:
            drawRect(bin_image, words, out_file, (255, 0, 0))
            write_txt_bill_recognition(out_file + '.txt', words_lists_per_line)
        else:
            print file_name, "without contours"
        print file_name, "without square and probably white"


if __name__ == '__main__':
    st = time.clock()
    # !!! please specify your dir
    cfe = CertainFunctionExecutor("bill_database", "Rectangled")
    # instant which applies your fun to each dir
    cfe.apply_your_fun(fun_to_apply)
    print time.clock() - st

