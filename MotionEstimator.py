#!/usr/bin/env python
__version__ =  '1.1'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'
import sys
import Image
import math
import random


class MotionEstimator:
    def __init__(self, a, b):
        assert(a.size == b.size)

        width, height = a.size
        a = a.resize((width*2, height*2), Image.ANTIALIAS) 
        b = b.resize((width*2, height*2), Image.ANTIALIAS) 

        a = a.convert('P', palette=Image.ADAPTIVE, colors=2)
        b = b.convert('P', palette=Image.ADAPTIVE, colors=2)
 
        self.a = a
        self.b = b

    def offset(self):
        frame = 20+ 3 # (number of collumns - 1) / 2
        width, height = self.a.size

        checked = 0
        x_e, y_e = 0, 0

        for offset in [1,2,3,4,5,6]:
            for i in range(3+offset, width-3):
                for j in range(3, height - 3):

                    if i < width-3 and i < height-3:
                        reference = 0
                        for (x, y) in self.offsets:
                            reference += self.a.getpixel((i + x, j + y))

                        if reference < 8 and reference > 3:
                            local_best_fit = self._get_pixel_offset(i, j)
                            if local_best_fit:
                                checked +=1
                                x_e += local_best_fit[0]
                                y_e += local_best_fit[1]

                    else:
                        break 

        print checked, x_e*4.0/checked, y_e*4.0/checked

        if checked == 0:
            return 0, 0
        return (x_e*4.0)/checked, (y_e*4.0)/checked



    def _get_pixel_offset(self, i, j):
        # todo move to a separate method
        best_fit = (0,0) 
        first_check = True
        smallest_difference = (123, 0)

        for (x_delta, y_delta) in self.offsets:
            p1 = self.a.getpixel((i, j))
            p2 = self.b.getpixel((i   + x_delta, j   + y_delta))

            p3 = self.a.getpixel((i+1, j+1))
            p4 = self.b.getpixel((i+1 + x_delta, j+1 + y_delta))

            p5 = self.a.getpixel((i-1, j-1))
            p6 = self.b.getpixel((i-1 + x_delta, j-1 + y_delta))

            p7 = self.a.getpixel((i-1, j+1))
            p8 = self.b.getpixel((i-1 + x_delta, j+1 + y_delta))

            p9 = self.a.getpixel((i+1, j-1))
            p10 = self.b.getpixel((i+1 + x_delta, j-1 + y_delta))

            p11 = self.a.getpixel((i, j-1))
            p12 = self.b.getpixel((i + x_delta, j-1 + y_delta))

            p13 = self.a.getpixel((i+1, j))
            p14 = self.b.getpixel((i+1 + x_delta, j + y_delta))


            difference = abs(p1 - p2) + abs(p3 - p4) + abs(p5-p6) + abs(p7-p8) + abs(p9-p10)  + abs(p11-p12) + abs(p13-p14) # TODO RGB

            if first_check or smallest_difference > difference:
                first_check = False
                smallest_difference = difference
                if not first_check:
                    best_fit = (x_delta, y_delta)

        return best_fit

    """offsets = ((-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
               (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
               (-2,  0), (-1,  0), (0,  0), (1,  0), (2,  0),
               (-2,  1), (-1,  1), (0,  1), (1,  1), (2,  1),
               (-2, -2), (-1,  2), (0,  2), (1,  2), (2,  2))"""

    offsets = ((0,  0), (1,  0), (2,  0),
                  (0,  1), (1,  1), (2,  1),
                  (0,  2), (1,  2), (2,  2))



if __name__=="__main__":

    assert(len(sys.argv) == 3)
    files = sys.argv[1], sys.argv[2]

    images = map(Image.open, files)

    estimator = MotionEstimator(images[0], images[1])
    (x, y) = estimator.offset()
    print "the offset between %s and %s is (%2d, %2d)" % (files[0], files[1], x, y)

