#!/usr/bin/env python

__author__ =  'Robert Gawron - http://rgawron.megiteam.pl'
__version__ =  '1.0'
__licence__ = 'BSD licence'

import os
import Image
import logging
from optparse import OptionParser


def take_a_photo(hi_res, offset, hps, f):
    size = hi_res.size
    lo = Image.new('RGB', size)

    mask = ((-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1))

    for x in range(1, hi_res.size[0]-1):
        for y in range(1, hi_res.size[1]-1):
            used_pixels = map(lambda (i,j): hi_res.getpixel((x+i, y+j)), mask)    
            
            (r, g, b) = (0, 0, 0)
            for (pixel, weight) in zip(used_pixels, hps):
                (r, g, b) = (r + pixel[0] * weight, g + pixel[1] * weight, b + pixel[2] * weight) 
                
            scale = len(used_pixels)
            (r, g, b) = (r/scale, g/scale, b/scale)

            lo.putpixel((x+offset[0], y+offset[1]), (r, g, b))

    return lo.resize((hi_res.size[0]/f, hi_res.size[1]/f), Image.LINEAR)



if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)

    parser = OptionParser('have a nice day')
    parser.add_option('-z', '--zoom', dest='zoom', 
                        help='zoom factor, natural number, greater from zero')
    parser.add_option('-i', '--image', dest='from_image', 
                        help='input file, in TIF format')

    (opt, args) = parser.parse_args()

    if not opt.zoom:
        opt.zoom = 3 # default value if not provided from command line

    (s, high_res_file) = (int(opt.zoom), opt.from_image)

    low_res_move = ( (-1, -1), (0, -1), (1, -1),
                     (-1,  0), (0,  0), (1,  0),
                     (-1,  1), (0,  1), (1,  1) )
                    
    hps = ( 0.5, 1.0, 0.5, 
            1.0, 3.0, 1.0,
            0.5, 1.0, 0.5 )

    output_folder = 'low_res_samples'

    high_res_image = Image.open(high_res_file)

    try:
        os.mkdir(output_folder)
    except OSError:
        pass

    for (x, y) in low_res_move:
        low_res_file_name = '%s/@%d_%d.tif' % (output_folder, x, y)
        image = take_a_photo(high_res_image, (x, y), hps, s)
        image.save(low_res_file_name)
        logging.info('%15s saved' % low_res_file_name)

