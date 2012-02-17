#!/usr/bin/env python
__version__ =  '2.0'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import sys
import os
import Image
import logging
import myconfig
import Camera


def stub(input_image):
    logging.basicConfig(level=logging.INFO)
    
    config = myconfig.config
    
    if not os.path.exists(config['samples_folder']):
        os.mkdir(config['samples_folder'])

    camera = Camera.Camera(config['psf'])
    downscale = 1.0/config['scale']

    for (x, y) in config['offsets_of_captured_imgs']:
        low_res_file = '%s/S_%d_%d.tif' % (config['samples_folder'], x, y)
        camera.take_a_photo(input_image, (x, y), downscale).save(low_res_file)
        logging.info('saved: %s' % low_res_file)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    input_image = Image.open(sys.argv[1])
    logging.info('Input Image: %s' % sys.argv[1])
    logging.info('Image size: %dx%d' % (input_image.size[0],input_image.size[1]))
    stub(input_image)

