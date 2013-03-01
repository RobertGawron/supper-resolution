#!/usr/bin/env python
__version__ =  '2.0'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import sys
import os
import math
import Image
import numpy

import myconfig
import Camera
from MotionEstimator import MotionEstimator

import string
import codecs


def clipto_0(val): return val if val>0 else 0
def clipto_255(val): return val if val<255 else 255
def clip(val): return clipto_0(clipto_255(val))
cliparray = numpy.frompyfunc(clip, 1, 1)

# upsample an array with zeros
def upsample(arr, n):
    z = numpy.zeros((len(arr))) # upsample with values
    for i in range(int(n-1)/2): arr = numpy.dstack((z,arr))
    for i in range(int( n )/2): arr = numpy.dstack((arr,z))
    return arr.reshape((1,-1))[0]


def SRRestore(camera, high_res, images, upscale, iter):
    error = 0
    captured_images = images

    c = len(captured_images)

    high_res_new = numpy.asarray(high_res).astype(numpy.float32)

    # for every LR with known pixel-offset
    for (offset, captured) in captured_images:

        (dx,dy) = offset

        # make LR of HR given current pixel-offset
        simulated = camera.take_a_photo(high_res, offset, 1.0/upscale)

        # convert captured and simulated to numpy arrays (mind the data type!)
        cap_arr = numpy.asarray(captured).astype(numpy.float32)
        sim_arr = numpy.asarray(simulated).astype(numpy.float32)

        # get delta-image/array: captured - simulated
        delta = (cap_arr - sim_arr) / c

        # Sum of Absolute Difference Error
        error += numpy.sum(numpy.abs(delta))

        # upsample delta to HR size (with zeros)
        delta_hr_R = numpy.apply_along_axis(lambda row: upsample(row,upscale),
                                            1, numpy.apply_along_axis(lambda col: upsample(col,upscale),
                                                                      0, delta[:,:,0]))

        delta_hr_G = numpy.apply_along_axis(lambda row: upsample(row,upscale),
                                            1, numpy.apply_along_axis(lambda col: upsample(col,upscale),
                                                                      0, delta[:,:,1]))

        delta_hr_B = numpy.apply_along_axis(lambda row: upsample(row,upscale),
                                            1, numpy.apply_along_axis(lambda col: upsample(col,upscale),
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



if __name__=="__main__":
    if len(sys.argv) != 2:
        print "usage: python %s directory_with_input_images" % sys.argv[0]
        sys.exit(0)

    samples_folder = sys.argv[1]
    config = myconfig.config

    input_images = []
    for file in (os.listdir(samples_folder)):
        if file[-4:] != '.tif':
            continue

        image = Image.open(samples_folder + '/' + file)
        if not input_images:
            input_images.append(((0, 0), image))
        else:
            estimator = MotionEstimator(input_images[0][1], image)
            (x, y) = map(int, estimator.offset())
            print file, x, y
            input_images.append(((x, y), image))

    scale = config['scale']
    camera = Camera.Camera(config['psf'])


    # start value = sum(upsampled + shifted LR)
    high_res_size  = [int(input_images[0][1].size[1] * scale), int(input_images[0][1].size[0] * scale), 3]
    high_res_image = numpy.zeros(high_res_size).astype(numpy.float32)
    for (offset, LR_img) in input_images:
        dx, dy = offset
        HR_arr = numpy.asarray(LR_img.resize((high_res_size[1],high_res_size[0]), Image.ANTIALIAS))
        high_res_image += numpy.dstack((camera.doOffset(HR_arr[:,:,0],(-dx,-dy)),
                                        camera.doOffset(HR_arr[:,:,1],(-dx,-dy)),
                                        camera.doOffset(HR_arr[:,:,2],(-dx,-dy))))
    high_res_image = high_res_image / len(input_images) # take average value
    high_res_image = Image.fromarray(numpy.uint8(high_res_image))

    # TODO move this to separate class
    for i in range(config['iterations']):
        high_res_image, error = SRRestore(camera, high_res_image, input_images, scale, i)
        error /=  float(high_res_image.size[0] * high_res_image.size[1])
        print 'iteration: %2d, estimation error: %3f' % (i, error)

    high_res_image.save('super_resolution.tif')

