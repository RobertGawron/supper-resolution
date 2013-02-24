#!/usr/bin/env python
__version__ =  '1.0'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'
import sys
import Image
import math
import random

def get_offset(a, b):
 
    """offsets = ((-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
               (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
               (-2,  0), (-1,  0), (0,  0), (1,  0), (2,  0),
               (-2,  1), (-1,  1), (0,  1), (1,  1), (2,  1),
               (-2, -2), (-1,  2), (0,  2), (1,  2), (2,  2))"""

    offsets = ((0,  0), (1,  0), (2,  0),
                  (0,  1), (1,  1), (2,  1),
                  (0,  2), (1,  2), (2,  2))

    frame = 20+ 3 # (number of collumns - 1) / 2
    width, height = a.size
    step = 1

    checked = 0
    x_e, y_e = 0, 0

    for x_start in range(frame, width - frame, step):
        for y_start in range(frame, height - frame, step):
            best_fit = []
            first_check = True
            smallest_difference = (123, 0)

            for (x_delta, y_delta) in offsets:
                p1 = a.getpixel((x_start, y_start))
                p2 = b.getpixel((x_start + x_delta, y_start + y_delta))
                difference = abs(p1[0] - p2[0]) # TODO RGB
 
                if first_check or smallest_difference >= difference:
                    first_check = False
                    smallest_difference = difference
                    if not first_check:
                        best_fit.append( (x_delta, y_delta) )

            #print len(best_fit)
            if len(best_fit) == 2: # 2? wtf?
                checked += 1
                x_e += best_fit[1][0]
                y_e += best_fit[1][1]
                #checked += 1

    print checked, x_e, y_e
    #checked = -70
    if checked == 0:
        return 0, 0
    return x_e/checked, y_e/checked
    

if __name__=="__main__":

    assert(len(sys.argv) == 3)
    files = sys.argv[1], sys.argv[2]

    images = map(Image.open, files)
    assert(images[0].size == images[1].size)

    width, height = images[0].size
    images[0] = images[0].resize((width*2, height*2), Image.ANTIALIAS) 
    images[1] = images[1].resize((width*2, height*2), Image.ANTIALIAS) 
    x, y = get_offset(images[0], images[1])
    print "the offset between %s and %s is (%2d, %2d)" % (files[0], files[1], x, y)
