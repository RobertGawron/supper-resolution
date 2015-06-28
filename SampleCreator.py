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

def showHelp():
    print("usage: python3 [script name] SAMPLE OUTPUT_DIRCTORY")
    print("\twhere:")
    print("\t\tSAMPLE - an image from which the samples will be created");
    print("\t\tOUTPUT_DIRCTORY - place where the samples will be created");
    print("\t\t\tdefault: sampleDirectory in srconfig.py")
    print("")
    print("Note: be sure to run the script with Python3 interpreter.") 

def parseCmdArgs(arguments, config):
    inImageFileName = arguments[1]
    outDirName = config['inputImageDirectory']

    if (len(arguments) == 3):
        outDirName = arguments[2]

    return inImageFileName, outDirName  

def mkdirOutput(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def createSamples(image, outDirectory):
    camera = Camera.Camera(cfg['psf'])
    downscale = 1.0 / cfg['scale']

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


if __name__ == "__main__":
    if 2 > len(sys.argv) > 3:
        showHelp();
        sys.exit(0)

    inImageFileName, outDirName = parseCmdArgs(sys.argv, cfg)

    inImage = SRImage()
    inImage.openFromFile(inImageFileName)
    inImageSize = inImage.w, inImage.h
    print('Input image size: %dx%d' % inImageSize)
    
    mkdirOutput(outDirName)

    createSamples(inImage, outDirName)

