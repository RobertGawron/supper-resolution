#!/usr/bin/env python
__version__ =  '2.0'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import sys
import os
import Image
import myconfig
import Camera

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: python %s output_folder input_file" % sys.argv[0]
        sys.exit(0)

    output_folder, input_file = sys.argv[1], sys.argv[2]

    offsets = [[0,0], [1,0], [2,0],
               [0,1], [1,1], [2,1],
               [0,2], [1,2], [2,2]]

    input_image = Image.open(input_file)
    print 'Input image size: %dx%d' % (input_image.size[0],input_image.size[1])
    
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    camera = Camera.Camera(myconfig.config['psf'])
    downscale = 1.0 / myconfig.config['scale']

    for (x, y) in offsets:
        low_res_file = '%s/S_%d_%d.tif' % (output_folder, x, y)
        camera.take_a_photo(input_image, (x, y), downscale).save(low_res_file)
        print 'Saved output image: %s' % low_res_file


