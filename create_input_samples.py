#!/usr/bin/env python

__author__ =  'Robert Gawron - http://robertgawron.blogspot.com/'
__version__ =  '1.0'
__licence__ = 'BSD licence'

import os
import Image
import logging
from optparse import OptionParser
import yaml

def take_a_photo(hi_res, offset, hps, f):
    size = hi_res.size
    lo = Image.new('RGB', size)

    mask = ((-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1))

    for x in range(1, hi_res.size[0]-1):
        for y in range(1, hi_res.size[1]-1):
            used_pixels = map(lambda (i, j): hi_res.getpixel((x+i, y+j)), mask)
 
            (r, g, b) = (0, 0, 0)
            for (pixel, weight) in zip(used_pixels, hps):
                (r, g, b) = (r + pixel[0] * weight, g + pixel[1] * weight, b + pixel[2] * weight) 
                
            scale = len(used_pixels)
            (r, g, b) = (r/scale, g/scale, b/scale)

            lo.putpixel((x+offset[0], y+offset[1]), (r, g, b))
           

    return lo.resize((hi_res.size[0]/f, hi_res.size[1]/f), Image.ANTIALIAS)



if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)

    default_config_file = 'config.yaml'
    default_scale_value = 3

    parser = OptionParser('have a nice day')
    parser.add_option('-i', '--image', dest='from_image', 
                        help='input file, in TIF format')
    parser.add_option('-s', '--scale', dest='scale', 
                        help='scale factor, natural number, greater from zero')
    parser.add_option('-c', '--config', dest='config', 
                        help='configuration file where constants are')

    (opt, args) = parser.parse_args()
    
    if not opt.scale:
        opt.scale = default_scale_value
 
    if not opt.config:
        opt.config = default_config_file 

    scale, input_img, config_file = int(opt.scale), opt.from_image, opt.config

    config = open(config_file, 'r')
    config = yaml.load(config)
    logging.debug(config)

    try:
        os.mkdir(config['samples_folder'])
    except OSError:
        logging.debug('tried to create samples folder')

    input_image = Image.open(input_img)

    for (x, y) in config['offsets_of_captured_imgs']:
        low_res_file = '%s/%d_%d.tif' % (config['samples_folder'], x, y)
        image = take_a_photo(input_image, (x, y), config['psf'], scale)
        image.save(low_res_file)
        logging.info('%15s saved' % low_res_file)

