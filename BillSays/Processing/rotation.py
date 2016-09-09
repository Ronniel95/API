# -*- coding: utf-8 -*-
"""
Automatically detect rotation and line spacing of an image of text using
Radon transform

If image is rotated by the inverse of the output, the lines will be
horizontal (though they may be upside-down depending on the original image)

It doesn't work with black borders
"""

from __future__ import division, print_function
from skimage.transform import radon
from PIL import Image
from numpy import asarray, mean, array, blackman
import numpy
from numpy.fft import rfft
import matplotlib.pyplot as plt
from matplotlib.mlab import rms_flat
import cv2
import time

try:
    # More accurate peak finding from
    # https://gist.github.com/endolith/255291#file-parabolic-py
    from parabolic import parabolic

    def argmax(x):
        return parabolic(x, numpy.argmax(x))[0]
except ImportError:
    from numpy import argmax

def get_rotation_angle(cv2_image):
    # rotation constraint: after perspective transform with correct bill contours
    # rotation cannot be more than 20 degrees
    # these is just a restriction not to make a rotation along sometimes drawn thin vertical stripes

    _ROT_CONSTRAINT = 20
    pil_im = Image.fromarray(cv2_image)
    I = pil_im.convert('L')
    I = I - mean(I)  # Demean; make the brightness extend above and below zero
    # plt.subplot(2, 2, 1)
    # plt.imshow(I)
    # Do the radon transform and display the result
    # st = time.clock()
    sinogram = radon(I)
    # fn = time.clock()
    # print("radon transform time", fn - st)
    #plt.subplot(2, 2, 2)
    #plt.imshow(sinogram.T, aspect='auto')
    #plt.gray()
    # Find the RMS value of each row and find "busiest" rotation,
    # where the transform is lined up perfectly with the alternating dark
    # text and white lines
    r = array(map(rms_flat, sinogram.transpose()))
    rotation = argmax(r)
    rot_angle = 90 - rotation
    if abs(rot_angle) < _ROT_CONSTRAINT:
        return rot_angle
    return 0


def rotate_on_angle(angle, cv2_image):
    if angle:
        rows = cv2_image.shape[0]
        cols = cv2_image.shape[1]
        M = cv2.getRotationMatrix2D((cols/2,rows/2), angle, 1)
        if len(cv2_image.shape) == 3:
            dst = cv2.warpAffine(cv2_image, M,(cols,rows), borderValue=(255, 255, 255))
        else:
            dst = cv2.warpAffine(cv2_image, M,(cols,rows), borderValue=255)
        return dst
    return cv2_image



def rotate_img(cv2_image):
    # rotation constraint: after perspective transform with correct bill contours
    # rotation cannot be more than 20 degrees
    # these is just a restriction not to make a rotation along sometimes drawen thin vertical stripes
    _ROT_CONSTRAINT = 20
    pil_im = Image.fromarray(cv2_image)
    I = pil_im.convert('L')
    I = I - mean(I)  # Demean; make the brightness extend above and below zero
    # plt.subplot(2, 2, 1)
    # plt.imshow(I)
    # Do the radon transform and display the result
    # st = time.clock()
    sinogram = radon(I)
    # fn = time.clock()

    # print("radon transform time", fn - st)

    #plt.subplot(2, 2, 2)
    #plt.imshow(sinogram.T, aspect='auto')
    #plt.gray()

    # Find the RMS value of each row and find "busiest" rotation,
    # where the transform is lined up perfectly with the alternating dark
    # text and white lines
    r = array(map(rms_flat, sinogram.transpose()))
    rotation = argmax(r)

    rot_angle = 90 - rotation
    #print(rotation)
    #print('Rotation: {:.2f} degrees'.format(90 - rotation))
    # plt.axhline(rotation, color='r')

    # rotation by affine transform
    if abs(rot_angle) < _ROT_CONSTRAINT:
        rows, cols = cv2_image.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2), rot_angle, 1)
        dst = cv2.warpAffine(cv2_image, M,(cols,rows), borderValue=255)
        #fn_g = time.clock()
        # print("time_global", fn_g - st_g)
        # cv2.imwrite(output_file, dst)
        return dst
    return cv2_image




def rotate(input_file, output_file):
    """36/40 of the time is eaten by Radon Transform!!!.
    """
    st_g = time.clock()
    filename = input_file
    # skew-linedetection
    # Load file, converting to grayscale
    I = asarray(Image.open(filename).convert('L'))
    I = I - mean(I)  # Demean; make the brightness extend above and below zero
   # plt.subplot(2, 2, 1)
   # plt.imshow(I)
    # Do the radon transform and display the result
    st = time.clock()
    sinogram = radon(I)
    fn = time.clock()

    # print("radon transform time", fn - st)

    #plt.subplot(2, 2, 2)
    #plt.imshow(sinogram.T, aspect='auto')
    #plt.gray()

    # Find the RMS value of each row and find "busiest" rotation,
    # where the transform is lined up perfectly with the alternating dark
    # text and white lines
    r = array([rms_flat(line) for line in sinogram.transpose()])
    rotation = argmax(r)
    # print('Rotation: {:.2f} degrees'.format(90 - rotation))
    # plt.axhline(rotation, color='r')

    # rotation by affine transform
    img = cv2.imread(filename, 0)
    rows,cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2), 90 - rotation, 1)
    dst = cv2.warpAffine(img, M,(cols,rows), borderValue=255)
    fn_g = time.clock()
    # print("time_global", fn_g - st_g)

    cv2.imwrite(output_file, dst)

    # Plot the busy row
    # row = sinogram[:, rotation]
    # N = len(row)
    # plt.subplot(2, 2, 3)
    # plt.plot(row)

    # Take spectrum of busy row and find line spacing
    # TODO: i will understand what's going on here later
    # now just comment
    # window = blackman(N)
    # spectrum = rfft(row * window)
    # plt.plot(row * window)
    # frequency = argmax(abs(spectrum))
    # line_spacing = N / frequency  # pixels
    # print('Line spacing: {:.2f} pixels'.format(line_spacing))
    #
    # plt.subplot(2, 2, 4)
    # plt.plot(abs(spectrum))
    # plt.axvline(frequency, color='r')
    # plt.yscale('log')
    # plt.show()

if __name__ == '__main__':
    input_file = "IMG_3975.JPG"
    output_file = "rotated_" + input_file
    rotate(input_file, output_file)
