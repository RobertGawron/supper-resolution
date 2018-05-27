#!/usr/bin/env python3
__version__ =  '2.1'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import sys
import os
from PIL import Image
from srconfig import cfg
import Camera
from SRImage import SRImage

def createSamples(image, outDirectory, scale):
    camera = Camera.Camera(cfg['psf'])
    downscale = 1.0 / scale

    # TODO move it somewhere
    offsets = [[0,0], [1,0], [2,0],
               [0,1], [1,1], [2,1],
               [0,2], [1,2], [2,2]]

    for (x, y) in offsets:
        sampleFileName = '%s/S_%d_%d.tif' % (outDirectory, x, y)
        sample = SRImage()
        sample.openFromLibImg(camera.take(image.toLibImgType(), (x, y), downscale))
        sample.save(sampleFileName)
        print('Sample created: %s' % sampleFileName)


def mkdirOutput(directory):
        os.makedirs(directory, exist_ok = True)

def main(inImageFileName, outDirName, scale):
    inImage = SRImage()
    inImage.openFromFile(inImageFileName)
    inImageSize = inImage.w, inImage.h
    print('Input image size: %dx%d' % inImageSize)

    mkdirOutput(outDirName)
    createSamples(inImage, outDirName, scale)