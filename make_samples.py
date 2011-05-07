#!/usr/bin/env python
__version__ =  '1.11'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import sys
import os
import Image
import logging
from optparse import OptionParser
import yaml


class Camera:
    def __init__(self, hps):
        self.hps = hps
        mask = ((-1, -1), (0, -1), (1, -1),
                (-1,  0), (0,  0), (1,  0),
                (-1,  1), (0,  1), (1,  1))

    def take_a_photo(self, image, offset, downsize):
        #low_res_size = image.size[0] / downsize, image.size[0] / downsize
        photo = Image.new('RGB', image.size)

        # apply hps and image movement
        for x in range(0, image.size[0]):
            for y in range(0, image.size[1]):
                involved_pixels = map(lambda (i, j): image.getpixel((x+i, y+j)), mask)
                r, g, b = 0, 0, 0
                for (pixel, weight) in zip(used_pixels, hps):
                    r, g, b = r + pixel[0] * weight, g + pixel[1] * weight, b + pixel[2] * weight

                scale = len(used_pixels)
                pixel = r / scale, g / scale, b / scale
                print pixel
                lo.putpixel((x + offset[0], y + offset[1]), pixel)
       
        # apply downsize factor        
        return photo

    """size = hi_res.size
    lo = Image.new('RGB', size)

    mask = ((-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1))

    def put_pixel(x, y):
        used_pixels = map(lambda (i, j): hi_res.getpixel((x+i, y+j)), mask)
        r, g, b = 0, 0, 0
        for (pixel, weight) in zip(used_pixels, hps):
            r, g, b = r + pixel[0] * weight, g + pixel[1] * weight, b + pixel[2] * weight
        scale = len(used_pixels)
        pixel = map(lambda u: int(u / scale), [r, g, b])#r / scale, g / scale, b / scale
        print pixel
        lo.putpixel((x + offset[0], y + offset[1]), pixel)
 
    for x in range(1, hi_res.size[0]-1):
        for y in range(1, hi_res.size[1]-1):
            put_pixel(x, y)  

    return lo.resize((hi_res.size[0]/f, hi_res.size[1]/f))#, Image.ANTIALIAS)"""

def parse_config_file(config_path):
    config = open(config_path, 'r')
    config = yaml.load(config)
    logging.debug(config)
    return config

def silent_mkdir(file_path):
    """it's like mkdir(), but it does nothing if directory exists"""
    try:
        os.mkdir(file_path)
    except OSError:
        logging.debug('unable to create directory for samples')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    default_config_path = 'config.yaml'
    default_scale_factor = 3
    
    parser = OptionParser('script_name image_path [...]')
    parser.add_option('-s', '--scale', dest='scale', 
                        help='[OPTIONAL] scale factor, natural number, greater from zero')
    parser.add_option('-c', '--config', dest='config', 
                        help='[OPTIONAL] path to configuration file')

    (opt, args) = parser.parse_args()

    if not opt.scale:
        opt.scale = default_scale_factor
    else:
        opt.scale = int(opt.scale)
 
    if not opt.config:
        opt.config = default_config_path

    if len(sys.argv) < 2:
        logging.info('No path to image was specified')
        sys.exit(0)

    input_image = Image.open(sys.argv[1])
    config = parse_config_file(opt.config)
    silent_mkdir(config['samples_folder'])
    camera = Camera(config['psf'])

    for (x, y) in config['offsets_of_captured_imgs']:
        low_res_file = '%s/%d_%d.tif' % (config['samples_folder'], x, y)
        camera.take_a_photo(input_image, (x, y), opt.scale).save(low_res_file)
        #image = take_a_photo(input_image, (x, y), config['psf'], opt.scale)
        #image.save(low_res_file)
        logging.info('%s saved' % low_res_file)

