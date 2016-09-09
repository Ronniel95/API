# -*- coding: utf-8 -*-
__author__ = 'gregory'

from PIL import Image, ExifTags
import timeit
import numpy as np



def resize_picture_dir(input_file, output_file, SIZE_CONST):
    """Performs proportional compressing if max(length, width) in pixels is more than 1000 pixels
    input_file - input picture name
    output_file - new picture with output_file name
    """
    COMPRESSING_CONSTANT = SIZE_CONST
    foo = Image.open(input_file)
    max_size = max(foo.size)
    if max_size > COMPRESSING_CONSTANT:   # if image has biggest size more than 1000
        k = COMPRESSING_CONSTANT / max_size
    else:
        k = 1
    # ---------- save the orientation of original foto
    for orientation in ExifTags.TAGS.keys() :
        if ExifTags.TAGS[orientation]=='Orientation' : break
    try:
        exif=dict(foo._getexif().items())
        if exif[orientation] == 3:
           foo=foo.rotate(180, expand=True)
        elif exif[orientation] == 6:
           foo=foo.rotate(270, expand=True)
        elif exif[orientation] == 8:
           foo=foo.rotate(90, expand=True)
    # ----------END of BLOCK save the orientation of original foto
    except:
        pass
    foo = foo.resize((int(foo.size[0] * k), int(foo.size[1] * k)), Image.ANTIALIAS)
    # foo.save(output_file, optimize=True, quality=95)
    open_cv_image = np.array(foo)
    # Convert RGB to BGR
    if len(open_cv_image.shape) == 3:
        open_cv_image = open_cv_image[:, :, ::-1].copy()
    # cv2.imwrite(output_file, open_cv_image)
    return open_cv_image

def save_picture_orientation(input_file):
    foo = Image.open(input_file)
    for orientation in ExifTags.TAGS.keys() :
        if ExifTags.TAGS[orientation]=='Orientation' : break
    try:
        exif=dict(foo._getexif().items())
        if exif[orientation] == 3:
           foo=foo.rotate(180, expand=True)
        elif exif[orientation] == 6:
           foo=foo.rotate(270, expand=True)
        elif exif[orientation] == 8:
           foo=foo.rotate(90, expand=True)
    # ----------END of BLOCK save the orientation of original foto
    except:
        pass
    open_cv_image = np.array(foo)
    # Convert RGB to BGR
    if len(open_cv_image.shape) == 3:
        open_cv_image = open_cv_image[:, :, ::-1].copy()
    # cv2.imwrite(output_file, open_cv_image)
    return open_cv_image

def resize_cv_picture(image, SIZE_CONST):
    foo = Image.fromarray(image)
    COMPRESSING_CONSTANT = SIZE_CONST
    max_size = max(foo.size)
    if max_size > COMPRESSING_CONSTANT:   # if image has biggest size more than 1000
        k = COMPRESSING_CONSTANT / max_size
    else:
        k = 1
    # ---------- save the orientation of original foto
    # for orientation in ExifTags.TAGS.keys() :
    #     if ExifTags.TAGS[orientation]=='Orientation' : break
    # try:
    #     exif=dict(foo._getexif().items())
    #     if exif[orientation] == 3:
    #        foo=foo.rotate(180, expand=True)
    #     elif exif[orientation] == 6:
    #        foo=foo.rotate(270, expand=True)
    #     elif exif[orientation] == 8:
    #        foo=foo.rotate(90, expand=True)
    # # ----------END of BLOCK save the orientation of original foto
    # except:
    #     pass
    foo = foo.resize((int(foo.size[0] * k), int(foo.size[1] * k)), Image.ANTIALIAS)
    # foo.save(output_file, optimize=True, quality=95)
    open_cv_image = np.array(foo)
    # Convert RGB to BGR
    if len(open_cv_image.shape) == 3:
        open_cv_image = open_cv_image[:, :, ::-1].copy()
    #cv2.imwrite(output_file, open_cv_image)
    return open_cv_image




def resize_picture_file(img, SIZE_CONST):
    """Performs proportional compressing if max(length, width) in pixels is more than 1000 pixels
    input_file - input picture name
    output_file - new picture with output_file name
    """
    COMPRESSING_CONSTANT = SIZE_CONST
    foo = img.copy()
    max_size = max(foo.size)
    if max_size > COMPRESSING_CONSTANT:   # if image has biggest size more than 1000
        k = COMPRESSING_CONSTANT / max_size
    else:
        k = 1
    # ---------- save the orientation of original foto
    for orientation in ExifTags.TAGS.keys() :
        if ExifTags.TAGS[orientation]=='Orientation' : break
    try:
        exif=dict(foo._getexif().items())
        if exif[orientation] == 3:
           foo=foo.rotate(180, expand=True)
        elif exif[orientation] == 6:
           foo=foo.rotate(270, expand=True)
        elif exif[orientation] == 8:
           foo=foo.rotate(90, expand=True)
    # ----------END of BLOCK save the orientation of original foto
    except:
        pass
    foo = foo.resize((int(foo.size[0] * k), int(foo.size[1] * k)), Image.ANTIALIAS)
    # foo.save(output_file, optimize=True, quality=95)
    open_cv_image = np.array(foo)
    # Convert RGB to BGR
    if len(open_cv_image.shape) == 3:
        open_cv_image = open_cv_image[:, :, ::-1].copy()
    #cv2.imwrite(output_file, open_cv_image)
    return open_cv_image


if __name__ == '__main__':
    start = timeit.timeit()
    input_file = "test6.jpg"
    output_file = "resized_test6.jpg"
    resize_picture_dir(input_file, output_file, 1006.0)
    print timeit.timeit() - start
