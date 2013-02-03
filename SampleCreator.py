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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    input_image = Image.open(sys.argv[1])
    logging.info('Input image size: %dx%d' % (input_image.size[0],input_image.size[1]))
    
    if not os.path.exists(myconfig.config['samples_folder']):
        os.mkdir(myconfig.config['samples_folder'])

    camera = Camera.Camera(myconfig.config['psf'])
    downscale = 1.0 / myconfig.config['scale']

    for (x, y) in myconfig.config['offsets_of_captured_imgs']:
        low_res_file = '%s/S_%d_%d.tif' % (myconfig.config['samples_folder'], x, y)
        camera.take_a_photo(input_image, (x, y), downscale).save(low_res_file)
        logging.info('Saved output image: %s' % low_res_file)


