#!/usr/bin/env python3
__version__ =  '2.1'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import sys
import os
import math
from PIL import Image
import numpy

import myconfig
import Camera
from MotionEstimator import MotionEstimator

import string
import codecs


def clipto_0(val): 
    return val if val>0 else 0

def clipto_255(val): 
    return val if val<255 else 255

def clip(val): 
    return clipto_0(clipto_255(val))

cliparray = numpy.frompyfunc(clip, 1, 1)

# upsample an array with zeros
def upsample(arr, n):
    z = numpy.zeros(len(arr)) # upsample with values
    for i in range(int(int(n-1)/2)): #TODO 
        arr = numpy.dstack((z,arr))
    for i in range(int(int( n )/2)):#TODO 
        arr = numpy.dstack((arr,z))
    return arr.reshape((1,-1))[0]


def SRRestore(camera, origImg, samples, upscale, iter):
    error = 0

    high_res_new = numpy.asarray(origImg).astype(numpy.float32)

    # for every LR with known pixel-offset
    for (offset, captured) in samples:

        (dx,dy) = offset

        # make LR of HR given current pixel-offset
        simulated = camera.take_a_photo(origImg, offset, 1.0/upscale)

        # convert captured and simulated to numpy arrays (mind the data type!)
        cap_arr = numpy.asarray(captured).astype(numpy.float32)
        sim_arr = numpy.asarray(simulated).astype(numpy.float32)

        # get delta-image/array: captured - simulated
        delta = (cap_arr - sim_arr) / len(samples)

        # Sum of Absolute Difference Error
        error += numpy.sum(numpy.abs(delta))

        # upsample delta to HR size (with zeros)
        delta_hr_R = numpy.apply_along_axis(
                    lambda row: upsample(row,upscale),
                    1, 
                    numpy.apply_along_axis(
                        lambda col: upsample(col,upscale),
                        0, 
                        delta[:,:,0]))

        delta_hr_G = numpy.apply_along_axis(
                    lambda row: upsample(row,upscale),
                    1, 
                    numpy.apply_along_axis(
                        lambda col: upsample(col,upscale),
                        0, 
                        delta[:,:,1]))

        delta_hr_B = numpy.apply_along_axis(
                    lambda row: upsample(row,upscale),
                    1, 
                    numpy.apply_along_axis(
                        lambda col: upsample(col,upscale),
                        0, delta[:,:,2]))

        # apply the offset to the delta
        delta_hr_R = camera.doOffset(delta_hr_R, (-dx,-dy))
        delta_hr_G = camera.doOffset(delta_hr_G, (-dx,-dy))
        delta_hr_B = camera.doOffset(delta_hr_B, (-dx,-dy))

        # Blur the (upsampled) delta with PSF
        delta_hr_R = camera.Convolve(delta_hr_R)
        delta_hr_G = camera.Convolve(delta_hr_G)
        delta_hr_B = camera.Convolve(delta_hr_B)

        # and update high_res image with filter result
        high_res_new += numpy.dstack((delta_hr_R,
                                      delta_hr_G,
                                      delta_hr_B))

    # normalize image array again (0-255)
    high_res_new = cliparray(high_res_new)

    return Image.fromarray(numpy.uint8(high_res_new)), error


def showHelp():
    print("usage: python %s directory_with_input_images" % sys.argv[0])
    print("usage: python3 [script name] INPUT_DIRCTORY")
    print("\twhere:")
    print("\t\tINPUT_DIRCTORY - directory with samples");
    print("")
    print("Note: be sure to run the script with Python3 interpreter.") 



def loadSamples(directory):
   samples = []
  
   for sampleFileName in (os.listdir(directory)):
        sampleExtension = sampleFileName[-4:] 
        if sampleExtension != '.tif':
            #print("" % (fileExtension))
            continue

        sample = Image.open(directory + '/' + sampleFileName)
        if not samples:
            samples.append(((0, 0), sample))
        else:
            estimator = MotionEstimator(samples[0][1], sample)
            (x, y) = map(int, estimator.offset())
            print ("%s: (%d, %d)" % (sampleFileName, x, y))
            samples.append(((x, y), sample))

   return samples

if __name__=="__main__":
    if len(sys.argv) != 2:
        showHelp()
        sys.exit(0)

    sampleDirectory = sys.argv[1]

    print ("Estimate Motion Between Sample And Original Image")
    samples = loadSamples(sampleDirectory)

    print ("Restore SR Image")
    camera = Camera.Camera(myconfig.config['psf'])
   
    scale = myconfig.config['scale'] 
    origSizeX = samples[0][1].size[1] * scale 
    origSizeY = samples[0][1].size[0] * scale
    origImage = numpy.zeros([origSizeX, origSizeY, 3]).astype(numpy.float32)
    print("Size Of Estimated Original: %dx%d" % (origSizeX, origSizeY))

    for ((dx, dy), sample) in samples:
        sampleOrigSize = sample.resize((origSizeX, origSizeY), Image.ANTIALIAS)
        sampleAsArr = numpy.asarray(sampleOrigSize)

    """    origImage += numpy.dstack((
                                camera.doOffset(sampleAsArr[:,:,0],(-dx,-dy)),
                                camera.doOffset(sampleAsArr[:,:,1],(-dx,-dy)),
                                camera.doOffset(sampleAsArr[:,:,2],(-dx,-dy))))
    """
    origImage = origImage / len(samples) # take average value
    origImage = Image.fromarray(numpy.uint8(origImage))

    # TODO move this to a separate class
    for i in range(myconfig.config['iterations']):
        origImage, estimDiff = SRRestore(camera, origImage, samples, scale, i)
        #estimDiff = 5
        estimDiff /=  float(origSizeX * origSizeY)
        print ('%2d: estimation error: %3f' % (i, estimDiff))
    origImage.save('super_resolution.tif')

