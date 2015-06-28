#!/usr/bin/env python3
__version__ =  '2.1'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import sys
import os
from PIL import Image
from srconfig import cfg
import Camera


class SRImage:
    def __init__(self):
        pass

    def openFromFile(self, filename):
        self.image = Image.open(filename)

    def openFromArray(array):
        assert(False)

    def save(filename):
        assert(False)

    #tmp fix
    def toLibImgType(self):
        return self.image

    @property
    def w(self):
        return self.image.size[0]

    @property
    def h(self):
        return self.image.size[1]


