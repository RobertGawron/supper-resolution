#!/usr/bin/env python
__version__ =  '1.1'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import math
import logging
import Image
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
        return photo.resize(downsize, Image.ANTIALIAS)



class SuperResolutionImage:
    def __init__(self, hps):
        self.hps = hps
        self.mask = ((-1, -1), (0, -1), (1, -1),
                     (-1,  0), (0,  0), (1,  0),
                     (-1,  1), (0,  1), (1,  1))

    def restore(self, camera, high_res, images, upsize):
        error = 0
        captured_images = images
        k = len(captured_images) # TDOO why is this here?

       
        for ((dx,dy), captured) in captured_images:
            simulated = camera.take_a_photo(high_res, (dx, dy), upsize)
            simulated = simulated.resize(high_res.size, Image.ANTIALIAS)
            captured = captured.resize(high_res.size, Image.ANTIALIAS)

            for x in range(2, simulated.size[0]-2):
                for y in range(2, simulated.size[1]-2):
                    rc, gc, bc = captured.getpixel((x, y))
                    rs, gs, bs = simulated.getpixel((x, y))

                    error += abs(rc - rs) + abs(gc - gs) + abs(bc - bs)

                    for (pfs_index, (dx, dy)) in zip(range(9), self.mask):
                        (rh, gh, bh) = high_res.getpixel((x - dx, y - dy))                       
                        rh += int(self.hps[pfs_index] * (rc - rs) / k)
                        gh += int(self.hps[pfs_index] * (gc - gs) / k)
                        bh += int(self.hps[pfs_index] * (bc - bs) / k)
                        high_res.putpixel((x - dx, y - dy), (rh, gh, bh))
    
        return high_res, error


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)

    default_config_file = 'config.yaml'
    default_scale_value = 2

    parser = OptionParser()
    parser.add_option('-s', '--scale', dest='scale', 
                        help='scale factor, natural number, greater from zero')
    parser.add_option('-c', '--config', dest='config', 
                        help='configuration file where constants are')

    (opt, args) = parser.parse_args()

    if not opt.scale:
        opt.scale = default_scale_value
 
    if not opt.config:
        opt.config = default_config_file 

    scale, config_file = int(opt.scale), opt.config

    config = open(config_file, 'r')
    config = yaml.load(config)
    logging.debug(config)

    sr_restorator = SuperResolutionImage(config['psf'])
 
    input_images = []
    
    for (dx, dy) in config['offsets_of_captured_imgs']:
        image = Image.open('%s/%d_%d.tif' % (config['samples_folder'], dx, dy))
        input_images.append(((dx, dy), image))

    # TODO this is broken, use some data structure or class 
    high_res_size = input_images[0][1].size[0] * scale, input_images[0][1].size[1] * scale
    high_res_image = input_images[0][1].resize(high_res_size, Image.ANTIALIAS)

    camera = Camera(config['psf'])

    # TODO move this to separate class, that will check error of estimation
    for i in range(config['iterations']):
        high_res_image, error = sr_restorator.restore(camera, high_res_image, input_images, scale)
        high_res_image.save('iteration_%d.tif' % i)
        k_todo = 9
        error /=  float(k_todo * high_res_image.size[0] * high_res_image.size[1])
        logging.info('iteration: %2d, estimation error: %3f' % (i, error))

