#!/usr/bin/env python
__version__ =  '2.0'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import sys
import os
import math
import Image
import numpy


## helper function for matrix padding
def do_padding(matrix, pwidth, pval=0):
    _pad = numpy.ones(pwidth) * pval
    return  numpy.apply_along_axis(lambda col:numpy.concatenate((_pad,col,_pad)), 0,
                                   numpy.apply_along_axis(lambda row:numpy.concatenate((_pad,row,_pad)), 1, matrix))

class Camera:
    def __init__(self, hps):
        print 'Creating Camera Model'

        # hps converted to 1D list
        self.hps  = numpy.array(hps).reshape(-1).tolist()
        self.hps = self.hps / numpy.sum(numpy.abs(self.hps)) # do normalization

        # size: pixels north of center
        self.size = int((numpy.sqrt(len(self.hps))-1) / 2)

        # psf: hps converted to 2D array
        self.psf  = numpy.array(self.hps).reshape((2*self.size + 1,2*self.size + 1))

        # square of PSF = BP
        self.psf2 = self.psf * self.psf

        # px_area : list of coordinates for area around center (=(0,0))
        mg = numpy.mgrid[-self.size:self.size+1, -self.size:self.size+1]
        self.pxarea = zip(list(mg[0].reshape(-1).tolist()),list(mg[1].reshape(-1).tolist()))


    def take_a_photo(self, image, offset, scale):

        # convert to numpy array
        odata  = numpy.asarray(image).astype(numpy.int32)

        # apply offset to HR image
        odata[:,:,0] = self.doOffset(odata[:,:,0], offset)
        odata[:,:,1] = self.doOffset(odata[:,:,1], offset)
        odata[:,:,2] = self.doOffset(odata[:,:,2], offset)

        # filter with the PSF (one color at the time)
        odata[:,:,0] = self.Convolve(odata[:,:,0])
        odata[:,:,1] = self.Convolve(odata[:,:,1])
        odata[:,:,2] = self.Convolve(odata[:,:,2])            

        # convert back to image format
        photo = Image.fromarray(numpy.uint8(odata))

        # apply scale factor
        new_img_sz = int(image.size[0] * scale), int(image.size[1] * scale)
        return photo.resize(new_img_sz, Image.ANTIALIAS)


    def doOffset(self, data, offset, val=255):
        # apply offset (via slicing, vertical and horizontal separately)
        if offset[1]>0: data = numpy.concatenate((numpy.ones((offset[1],data.shape[1]))*val, data[0:-offset[1],:]), axis=0)
        if offset[1]<0: data = numpy.concatenate((data[-offset[1]:,:], numpy.ones((-offset[1],data.shape[1]))*val), axis=0)
        if offset[0]>0: data = numpy.concatenate((numpy.ones((data.shape[0],offset[0]))*val, data[:,0:-offset[0]]), axis=1)
        if offset[0]<0: data = numpy.concatenate((data[:,-offset[0]:], numpy.ones((data.shape[0],-offset[0]))*val), axis=1)
        return data
    

    """
    def Convolve(self, data):
        ### FFT-iFFT approach : does not converge to solution
        fft  = numpy.fft.fft2(data) * numpy.fft.fft2(self.psf, data.shape)
        conv = numpy.fft.ifft2(fft).real
        return conv
    """

    """
    def Convolve(self, data):
        ### nested for-loops implementation : very slow !!!
        conv = data
        w = self.size
        for x in range(w, data.shape[0]-w):
            for y in range(w, data.shape[1]-w):
                conv[x,y] = numpy.sum(data[x-w:x+w+1,y-w:y+w+1] * self.psf)
        return conv
    """

    def Convolve(self, data):
        ### python magic implementation
        w = 2*self.size
        # need some (zero) padding first
        data = do_padding(data,self.size)
        # now stack row shifts
        b = data[:,0:-w]
        for r in range(1,w): b = numpy.dstack((b,data[:,r:r-w]))
        b = numpy.dstack((b,data[:,w:]))
        data = b
        # next stack col shifts
        b = data[0:-w,:]
        for c in range(1,w): b = numpy.dstack((b,data[c:c-w,:]))
        b = numpy.dstack((b,data[w:,:]))
        data = b
        # now apply filtering
        conv = numpy.sum(data * numpy.tile(self.hps, (data.shape[0],data.shape[1],1)), axis=2)

        return conv


    def Convolve2(self, data):
        ### python magic implementation
        w = 2*self.size
        # need some (zero) padding first
        data = do_padding(data,self.size)
        # now stack row shifts
        b = data[:,0:-w]
        for r in range(1,w): b = numpy.dstack((b,data[:,r:r-w]))
        b = numpy.dstack((b,data[:,w:]))
        data = b
        # next stack col shifts
        b = data[0:-w,:]
        for c in range(1,w): b = numpy.dstack((b,data[c:c-w,:]))
        b = numpy.dstack((b,data[w:,:]))
        data = b
        # now apply filtering
        conv = numpy.sum(data * numpy.tile((self.hps * self.hps), (data.shape[0],data.shape[1],1)), axis=2)

        return conv

