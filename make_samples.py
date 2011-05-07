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
        self.mask = ((-1, -1), (0, -1), (1, -1),
                     (-1,  0), (0,  0), (1,  0),
                     (-1,  1), (0,  1), (1,  1))

    def take_a_photo(self, image, offset, downsize):
        photo = Image.new('RGB', image.size)

        # apply hps and image movement
        w = 3 # TODO compute this!
        for x in range(w, image.size[0]-w):
            for y in range(w, image.size[1]-w):
                # compute weighted (by hps) mean of pixels, that contribute
                involved_pixels = map(lambda (i, j): image.getpixel((x+i, y+j)), self.mask)
                r, g, b = 0, 0, 0
                
                for ((ra, ga, ba), weight) in zip(involved_pixels, self.hps):
                    r, g, b = r + ra * weight, g + ga * weight, b + ba * weight

                scale = len(involved_pixels) # TODO this is broken!
                pixel = int(r / scale), int(g / scale), int(b / scale)
                photo.putpixel((x + offset[0], y + offset[1]), pixel)
       
        # apply downsize factor
        downsize = image.size[0] / downsize, image.size[1] / downsize
        return photo.resize(downsize)


def parse_config_file(config_path):
    config = open(config_path, 'r')
    config = yaml.load(config)
    logging.debug(config)
    return config

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
    os.mkdir(config['samples_folder'])
    camera = Camera(config['psf'])

    for (x, y) in config['offsets_of_captured_imgs']:
        low_res_file = '%s/%d_%d.tif' % (config['samples_folder'], x, y)
        camera.take_a_photo(input_image, (x, y), opt.scale).save(low_res_file)
        logging.info('saved: %s' % low_res_file)

