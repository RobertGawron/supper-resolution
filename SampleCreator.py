#!/usr/bin/env python3
__version__ =  '2.1'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import sys
import os
from PIL import Image
import myconfig
import Camera


def showHelp():
    print("usage: python3 [script name] SAMPLE OUTPUT_DIRCTORY")
    print("\twhere:")
    print("\t\tSAMPLE - an image from which the samples will be created");
    print("\t\tOUTPUT_DIRCTORY - place where the samples will be created");
    print("")
    print("Note: be sure to run the script with Python3 interpreter.") 

def mkdirOutput(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def createSamples(image, outDirectory):
    camera = Camera.Camera(myconfig.config['psf'])
    downscale = 1.0 / myconfig.config['scale']

    # TODO move it somewhere
    offsets = [[0,0], [1,0], [2,0],
               [0,1], [1,1], [2,1],
               [0,2], [1,2], [2,2]]

    for (x, y) in offsets:
        sampleFileName = '%s/S_%d_%d.tif' % (outDirectory, x, y)
        camera.take_a_photo(image, (x, y), downscale).save(sampleFileName)
        print('Sample created: %s' % sampleFileName)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        showHelp();
        sys.exit(0)

    inImageFileName, outDirName = sys.argv[1], sys.argv[2]

    inImage = Image.open(inImageFileName)
    inImageSize = inImage.size[0], inImage.size[1]
    print('Input image size: %dx%d' % inImageSize)
    
    mkdirOutput(outDirName)

    createSamples(inImage, outDirName)

