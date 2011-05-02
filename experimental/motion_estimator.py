#!/usr/bin/env python
__author__ =  'Robert Gawron - http://robertgawron.blogspot.com/'
__version__ =  '0.1'
__licence__ = 'FreeBSD License'
import Image
import math
import random


class KnownInputEstimationTester:
    """Take as input.."""
    pass

class UnknownInputEstimationTester:
    pass


class MotionEstimator:
    def __init__(self, iteraions_per_check=9):
        self.iteraions_per_check = iteraions_per_check
        self.mask = ((0, 0), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
 

    def compute_offset(self, a, b, start_point):
        width, height = a.size
        x_start, y_start = start_point
        x, y = x_start, y_start 

        p1, p2 = a.getpixel((x, y)), b.getpixel((x, y))
        difference = abs(p1[0] - p2[0])
        smalest_difference = difference

        for i in range(self.iteraions_per_check):
            p = i % len(self.mask)
            x_checked, y_checked = x + self.mask[p][0], y + self.mask[p][1]
            p1, p2 = a.getpixel((x, y)), b.getpixel((x_checked, y_checked))
            difference = abs(p1[0] - p2[0])

            if difference < smalest_difference:
                smalest_difference = difference
                x, y = x_checked, y_checked

        return x - x_start, y - y_start


    def estimate(self, a, b):
        iterations=100

        width, height = a.size
        a = a.resize((width*2, height*2)) 
        b = b.resize((width*2, height*2)) 

        width, height = a.size
        w = 4
        x, y = 0, 0

        for i in range(iterations):
            p = random.randrange(w, width-w), random.randrange(w, height-w)
            xn, yn = self.compute_offset(a, b, p)
            x, y = x + xn, y + yn

        return x / iterations, y / iterations

if __name__=="__main__":

    files = ['input_images/0_0.tif', 'input_images/0_-1.tif', 'input_images/1_0.tif', 'input_images/-1_-1.tif', 'input_images/1_1.tif']
    offsets = [(0,0), (0,-1), (1,0), (-1,-1), (1,1)]

    images = map(Image.open, files)
    #images = map(lambda x: x.resize((images[0].size[0]*2, images[1].size[0]*2)), images)
    
    estimator = MotionEstimator()

    sum_of_errors = 0 
    for i in range(1, len(files)):
        x, y = estimator.estimate(images[0], images[i])
        error = abs(x - offsets[i][0]) + abs(y - offsets[i][1])
        sum_of_errors += error
        print "(%2d %2d) -> (%2d, %2d) %d" % (offsets[i][0], offsets[i][1], x, y, error)
  
    print "total: %d" % sum_of_errors 
