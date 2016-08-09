# -*- coding: utf-8 -*-
__author__ = 'gregory'

"""
Stages of processing are described in fun_to_apply.
"""

from change_resolution import resize_picture_dir
from binarization import Binarization
from rotation import rotate
from os import listdir, path
import time

class CertainFunctionExecutor:
    """Instances of this class search for image in directory and apply user function for each.
    Idea as in the BRIDGE pattern.
    """
    def __init__(self, inp_dir, out_dir):
        """Initialization of internals
        inp_dir - where images to process are
        out_dir - where the processed images to write
        """
        self.apply_to_image = None
        self.file_names = None
        self.inp_dir = inp_dir
        self.out_dir = out_dir
        self.file_names = [f for f in listdir(self.inp_dir)]

    def apply_your_fun(self, fun):
        for f in self.file_names:
            fun(self.inp_dir, f, self.out_dir)

        # (fun(self.inp_dir, f, self.out_dir) for f in self.file_names)


def fun_to_apply(inp_dir, file_name, out_dir):
    """Applying stages for image in pipeline proccesing
    1. resing 2. binarization 3. rotation.
    Parameters:
    inp_dir - path where you have images to process
    file_name - the file name of current image
    out_dir - path where you keep processed images
    """

    inp_file = '/'.join([inp_dir, file_name])
    new_file_name = "resiz_" + file_name
    out_file = '/'.join([out_dir, new_file_name])
    #resize_picture(inp_file, out_file)

    inp_file = '/'.join([out_dir, new_file_name])
    new_file_name = "binar_" + new_file_name
    out_file = '/'.join([out_dir, new_file_name])
    #binarize(inp_file, out_file)

    inp_file = '/'.join([out_dir, new_file_name])
    new_file_name = "rotat_" + new_file_name
    out_file = '/'.join([out_dir, new_file_name])
    rotate(inp_file, out_file)

    # inp_file = '/'.join([out_dir, new_file_name])
    # new_file_name = "binar_" + new_file_name
    # out_file = '/'.join([out_dir, new_file_name])
    # binarize(inp_file, out_file)


if __name__ == '__main__':
    st = time.clock()
    cfe = CertainFunctionExecutor("bill_database", "rotated_binarized")
    cfe.apply_your_fun(fun_to_apply)
    print time.clock() - st
