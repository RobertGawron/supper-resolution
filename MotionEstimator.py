#!/usr/bin/env python
__version__ =  '1.0'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'
import sys
import Image
import math
import random

def get_offset(a, b):
 
    offsets = ((-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
               (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
               (-2,  0), (-1,  0), (0,  0), (1,  0), (2,  0),
               (-2,  1), (-1,  1), (0,  1), (1,  1), (2,  1),
               (-2, -2), (-1,  2), (0,  2), (1,  2), (2,  2))

    width, height = a.size
    frame = 10 # TODO is it needed?
    x_start = random.randrange(frame, width - frame)
    y_start = random.randrange(frame, height - frame)

    best_fit = 0, 0
    first_check = True
    smallest_difference = (0, 0)

    for (x_delta, y_delta) in offsets:
        p1 = a.getpixel((x_start, y_start))
        p2 = b.getpixel((x_start + x_delta, y_start + y_delta))
        difference = abs(p1[0] - p2[0]) # TODO RGB
 
        if first_check or smallest_difference >= difference:
            first_check = False
            smallest_difference = difference
            best_fit = x_delta, y_delta

    #print best_fit
    return best_fit

if __name__=="__main__":

    assert(len(sys.argv) == 3)
    files = sys.argv[1], sys.argv[2]

    images = map(Image.open, files)
    assert(images[0].size == images[1].size)

    width, height = images[0].size
    images[0] = images[0].resize((width*2, height*2)) 
    images[1] = images[1].resize((width*2, height*2)) 

    # the estimated movement is an average of many single checks
    samples_amount = 200# TODO magic number
    x, y = 0, 0
    for i in range(samples_amount):
        xn, yn = get_offset(images[0], images[1])
        x, y = x + xn, y + yn
        #print xn,yn

    #print "--"
    #print x,y
    x, y = (x / samples_amount), (y / samples_amount)

    print "the offset between %s and %s is (%2d, %2d)" % (files[0], files[1], x, y)
