#!/usr/bin/env python
__version__ =  '1.1'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import math
import logging
import Image
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



def update_estimation(high_res_image, captured_images, hps, k, s):
    error = 0
    mask = ((-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1))

    for ((dx,dy), captured) in captured_images:
        simulated = take_a_photo(high_res_image, (dx, dy), hps, s)
        simulated = simulated.resize(high_res_image.size, Image.ANTIALIAS)
        captured = captured.resize(high_res_image.size, Image.ANTIALIAS)

        for x in range(2, simulated.size[0]-2):
            for y in range(2, simulated.size[1]-2):
                (rc, gc, bc) = captured.getpixel((x, y))
                (rs, gs, bs) = simulated.getpixel((x, y))

                error += abs(rc - rs) + abs(gc - gs) + abs(bc - bs)

                for (pfs_index, (dx, dy)) in zip(range(9), mask):
                    (rh, gh, bh) = high_res_image.getpixel((x-dx-1, y-dy-1))
                    rh += hps[pfs_index] * (rc - rs) / (k)
                    gh += hps[pfs_index] * (gc - gs) / (k)
                    bh += hps[pfs_index] * (bc - bs) / (k)
                    high_res_image.putpixel((x-dx-1, y-dy-1), (rh, gh, bh))
    
    return (error, high_res_image)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)

    default_config_file = 'config.yaml'
    default_scale_value = 2

    parser = OptionParser('have a nice day')
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

    load_image = lambda (x,y): ((x,y), Image.open('%s/%d_%d.tif' % (config['samples_folder'], x, y)))
    captured_images = map(load_image, config['offsets_of_captured_imgs'])
    k = len(captured_images)

    base_for_estimation = captured_images[0][1]
    high_res_size = (base_for_estimation.size[0]*scale, base_for_estimation.size[1]*scale)
    high_res_image = base_for_estimation.resize(high_res_size, Image.ANTIALIAS)

    for iteration in range(0, config['iterations']):
        (error, high_res_image) = update_estimation(high_res_image, captured_images, config['psf'], k, scale)
        high_res_image.save('iteration.%d.tif' % iteration)
        error /=  float(k * high_res_image.size[0] * high_res_image.size[1])
        logging.info('iteration: %2d, estimation error: %3f' % (iteration, error))

