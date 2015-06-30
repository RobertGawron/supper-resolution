#!/usr/bin/env python3
__version__ =  '2.1'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

from PIL import Image
import Camera

"""
    Abstraction of an image, later it will a wrapper for C module.
"""
class SRImage:
    def __init__(self):
        pass

    def openFromFile(self, filename):
        self.image = Image.open(filename)

    def openFromLibImg(self, image):
        self.image = image

    def openFromArray(self, array):
        assert(False)

    def save(self, filename):
        self.image.save(filename) 

    #tmp fix
    def toLibImgType(self):
        return self.image

    @property
    def w(self):
        return self.image.size[0]

    @property
    def h(self):
        return self.image.size[1]


