# -*- coding: utf-8 -*-
import os

__author__ = 'gregory'


from detect_rectangle_on_image import ContoursRecognition
from change_resolution import * #resize_picture_dir, save_picture_orientation
from binarization import Binarization
from rotation import *

from perspective_trnsfrm import *
import lines_and_tesseract
from receipt import Receipt
from objectview import objectview
import yaml


def read_config():

    #print os.path.dirname(os.path.realpath(__file__))

    test = os.path.dirname(os.path.realpath(__file__))

    stream = open(os.path.join(test, "config.yml"), "r")
    docs = yaml.safe_load(stream)
    return objectview(docs)



# TODO: dir reference to imge file

def procces_receipt_image(ref_img_path):
    """Applying all stages of proccesing of receipt photo.
    returns: instance of class Receipt (It can be with empty fields if it can't be parsed)
             or None
    """
    CONTOURS_SIZE = 1006.0
    ROTATE_SIZE = 300.0
    inp_file = ref_img_path
    image = save_picture_orientation(inp_file)
    image_contour = resize_picture_dir(inp_file, " ", CONTOURS_SIZE)
    cr = ContoursRecognition(image_contour)
    square = cr.find_bill_contour()
    if square.size:
        cv2.drawContours(image_contour, [square], -1, (0, 255, 0), 2)
        k = max(image.shape) / CONTOURS_SIZE
        explicit_square = np.array([map(int, k * np.array(elem[0], dtype="float32")) for elem in square])
        cut_img = four_point_transform(image, explicit_square)
        img_for_angle = resize_cv_picture(cut_img, ROTATE_SIZE)
        angle = get_rotation_angle(img_for_angle)
        cut_rotated_img = rotate_on_angle(angle, cut_img)
        cut_rotated_img = Binarization.binarize_big(cut_rotated_img)
        cut_rotated_img = lines_and_tesseract.letters_eroding(cut_rotated_img)
        backtorgb = cv2.cvtColor(cut_rotated_img, cv2.COLOR_GRAY2RGB)
        #cv2.imwrite(out_file, backtorgb)
        text = lines_and_tesseract.get_txt(backtorgb)
        # text_file = open(out_file + ".txt", "w")
        # for i in xrange(len(text)):
        #      text_file.write(text[i] + '\n')
        # text_file.close()
        # print text
        receipt = Receipt(read_config(), text)
        # print(receipt.place, receipt.service, receipt.date, receipt.sum)


    elif(not square and not cr.is_white):
    # TODO: loging on server (without square and probably not white)
        #print file_name, "without square and probably not white"
        receipt = None
    elif(not square and cr.is_white):
    # TODO: loging on server (without square and probably white)
        img_for_angle = Binarization.binarize_big(image)
        img_for_angle = resize_cv_picture(img_for_angle, ROTATE_SIZE)
        angle = get_rotation_angle(img_for_angle)
        rotated_img = rotate_on_angle(angle, image)
        # cv2.imwrite(debug_out_file, img_for_angle)
        bin_rotated_img = Binarization.binarize_big(rotated_img)
        bin_rotated_img = lines_and_tesseract.letters_eroding(bin_rotated_img)
        backtorgb = cv2.cvtColor(bin_rotated_img, cv2.COLOR_GRAY2RGB)
        #cv2.imwrite(out_file, backtorgb)
        text = lines_and_tesseract.get_txt(backtorgb)
        # text_file = open(out_file + ".txt", "w")
        # for i in xrange(len(text)):
        #     text_file.write(text[i] + '\n')
        # text_file.close()
        receipt = Receipt(read_config(), text)

    return receipt


# def fun_to_apply(inp_dir, file_name, out_dir):
#     """Debug processing for each image (applying for all images) in certain dir.
#     Class CertainFunctionExecutor.
#     """
#     CONTOURS_SIZE = 1006.0
#     ROTATE_SIZE = 300.0
#     # constant for resizing the image
#     inp_file = '/'.join([inp_dir, file_name])
#     # the way for input file
#     new_file_name = "proccessed_" + file_name
#     debug_file_name = "debug_contour_" + file_name
#     # file_name for debug
#     out_file = '/'.join([out_dir, new_file_name])
#     # the way for output file
#     debug_out_file = '/'.join([out_dir, debug_file_name])
#     # the way where write debug file
#     image = save_picture_orientation(inp_file)
#     image_contour = resize_picture_dir(inp_file, out_file, CONTOURS_SIZE)
#     #binrztn = Binarization()
#     #bin_image = binrztn.process_with_one_resizing_best(inp_file, out_file)
#     # bin_image = Binarization.binarize_big(image)
#     cr = ContoursRecognition(image_contour)
#     square = cr.find_bill_contour()
#     if square.size:
#         cv2.drawContours(image_contour, [square], -1, (0, 255, 0), 2)
#         k = max(image.shape) / CONTOURS_SIZE
#         explicit_square = np.array([map(int, k * np.array(elem[0], dtype="float32")) for elem in square])
#         cut_img = four_point_transform(image, explicit_square)
#         img_for_angle = resize_cv_picture(cut_img, ROTATE_SIZE)
#         angle = get_rotation_angle(img_for_angle)
#         cut_rotated_img = rotate_on_angle(angle, cut_img)
#         cut_rotated_img = Binarization.binarize_big(cut_rotated_img)
#         cut_rotated_img = lines_and_tesseract.letters_eroding(cut_rotated_img)
#         backtorgb = cv2.cvtColor(cut_rotated_img, cv2.COLOR_GRAY2RGB)
#         cv2.imwrite(out_file, backtorgb)
#         text = lines_and_tesseract.get_txt(backtorgb)
#         text_file = open(out_file + ".txt", "w")
#         for i in xrange(len(text)):
#              text_file.write(text[i] + '\n')
#         text_file.close()
#         print text
#         receipt = Receipt(read_config(), text)
#         print(receipt.place, receipt.service, receipt.date, receipt.sum)
#
#
#     elif(not square and not cr.is_white):
#     # TODO: loging on server (without square and probably not white)
#         print file_name, "without square and probably not white"
#         receipt = None
#     elif(not square and cr.is_white):
#     # TODO: loging on server (without square and probably white)
#         img_for_angle = Binarization.binarize_big(image)
#         img_for_angle = resize_cv_picture(img_for_angle, ROTATE_SIZE)
#         angle = get_rotation_angle(img_for_angle)
#         rotated_img = rotate_on_angle(angle, image)
#         # cv2.imwrite(debug_out_file, img_for_angle)
#         bin_rotated_img = Binarization.binarize_big(rotated_img)
#         bin_rotated_img = lines_and_tesseract.letters_eroding(bin_rotated_img)
#         backtorgb = cv2.cvtColor(bin_rotated_img, cv2.COLOR_GRAY2RGB)
#         cv2.imwrite(out_file, backtorgb)
#         text = lines_and_tesseract.get_txt(backtorgb)
#         text_file = open(out_file + ".txt", "w")
#         for i in xrange(len(text)):
#             text_file.write(text[i] + '\n')
#         text_file.close()
#         receipt = Receipt(read_config(), text)



if __name__ == '__main__':
    receipt = procces_receipt_image("im2.jpg") # specify path with file name to receipt