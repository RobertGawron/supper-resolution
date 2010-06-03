#!/usr/bin/env python
__author__ =  'Robert Gawron - http://rgawron.megiteam.pl'
__version__ =  '1.0'
__licence__ = 'BSD licence'

import math
import logging
import Image
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



def update_estimation(high_res_image, low_res_images, low_res_move, hps, k, f):
    assert k > 0

    error = 0
    make_simulated_image = lambda offset: take_a_photo(high_res_image, offset, hps, f)
    low_res_simulated = map(make_simulated_image, low_res_move) 

    for (simulated, original) in zip(low_res_simulated, low_res_images):
        ((dx, dy), original) = original # unpack it, post-perl freak here :)
        diff = Image.new('RGB', simulated.size)

        for x in range(0, simulated.size[0]):
            for y in range(0, simulated.size[1]):
                (ro, go, bo) = original.getpixel((x, y))
                (rs, gs, bs) = simulated.getpixel((x, y))

                error += abs(ro - rs)

                ro = ((ro - rs)/2 ) + 120
                go = ((go - gs)/2 ) + 120
                bo = ((bo - bs)/2 ) + 120

                diff.putpixel((x, y), (ro, go, bo))
 

        diff = diff.resize((diff.size[0]*f, diff.size[1]*f), Image.LINEAR)

        # robie hpsa
        #hpsowane = Image.new('RGB', diff.size)
        ss = 2
        for x in range(ss, diff.size[0]-ss):
            for y in range(ss, diff.size[1]-ss):
                    hpsx = [4.5, 12.0, 4.5, 12.0, 33.0, 12.0, 4.5, 12.0, 4.5]


                    """p = (diff.getpixel((x, y))[0] - 120)/(9*9*9*k)


                    z = p*hps[0] + high_res_image.getpixel((x - dx-1, y - dy-1))[0]
                    high_res_image.putpixel((x - dx-1, y - dy-1), (z,z,z))

                    z = p*hps[1] + high_res_image.getpixel((x - dx, y - dy-1))[0]
                    high_res_image.putpixel((x - dx, y - dy-1), (z,z,z))

                    z = p*hps[2] + high_res_image.getpixel((x - dx+1, y -dy-1))[0]
                    high_res_image.putpixel((x - dx+1, y - dy-1), (z,z,z))



                    z = p*hps[3] + high_res_image.getpixel((x - dx-1, y -dy))[0]
                    high_res_image.putpixel((x - dx-1, y - dy), (z,z,z))

                    z = p*hps[4] + high_res_image.getpixel((x - dx, y - dy))[0]
                    high_res_image.putpixel((x - dx, y - dy), (z,z,z))

                    z = p*hps[5] + high_res_image.getpixel((x - dx+1, y -dy))[0]
                    high_res_image.putpixel((x - dx+1, y - dy), (z,z,z))




                    z = p*hps[6] + high_res_image.getpixel((x - dx-1, y - dy+1))[0]
                    high_res_image.putpixel((x - dx-1, y - dy+1), (z,z,z))

                    z = p*hps[7] + high_res_image.getpixel((x - dx, y -dy+1))[0]
                    high_res_image.putpixel((x - dx, y - dy+1), (z,z,z))

                    z = p*hps[8] + high_res_image.getpixel((x - dx+1, y -dy+1))[0]
                    high_res_image.putpixel((x - dx+1, y - dy+1), (z,z,z))"""




                    p0 = diff.getpixel((x - 1, y - 1))
                    p1 = diff.getpixel((x,     y - 1))
                    p2 = diff.getpixel((x + 1, y - 1))
                             
                    p3 = diff.getpixel((x - 1, y))
                    p4 = diff.getpixel((x,     y))
                    p5 = diff.getpixel((x + 1, y))

                    p6 = diff.getpixel((x - 1, y + 1))
                    p7 = diff.getpixel((x,     y + 1))
                    p8 = diff.getpixel((x + 1, y + 1))

                    r  = (p0[0]-120)*hpsx[0] + (p1[0]-120)*hpsx[1] + (p2[0]-120)*hpsx[2]
                    r += (p3[0]-120)*hpsx[3] + (p4[0]-120)*hpsx[4] + (p5[0]-120)*hpsx[5]
                    r += (p6[0]-120)*hpsx[6] + (p7[0]-120)*hpsx[7] + (p8[0]-120)*hpsx[8]

                    #r /= 9#*9
                    #r = 0.5* ( p4[0]-120 )


                    (a1,a2,a3) = high_res_image.getpixel((x - dx, y - dy))
                    a1 += r/k
                    
                    high_res_image.putpixel((x - dx, y - dy), (a1,a1,a1))


    return (error, high_res_image)



def main():
    low_res_move = ( (-1, -1), (0, -1), (1, -1),
                     (-1,  0), (0,  0), (1,  0),
                     (-1,  1), (0,  1), (1,  1) )

    iterations = 100
    f = 2
    output_folder = 'input_samples'

    high_res_file = 'estimated.tif'

    hps = ( 0.5, 1.0, 0.5, 
            1.0, 3.0, 1.0,
            0.5, 1.0, 0.5 )

    logging.debug(hps)

    get_image = lambda (x,y): ((x,y), Image.open('%s/@%d_%d.tif' % (output_folder, x, y)))
    low_res_images = map(get_image, low_res_move)

    base_for_estimation = low_res_images[0][1]
    high_res_size = (base_for_estimation.size[0]*f, base_for_estimation.size[1]*f)
    high_res_image = base_for_estimation.resize(high_res_size, Image.ANTIALIAS)

    k = len(low_res_images)

    for iteration in range(0, iterations):
        (error, high_res_image) = update_estimation(high_res_image, low_res_images, low_res_move, hps, k, f)
        high_res_image.save('@%d.tif' % iteration)
        logging.info('iteration #%2d done, estimation error: %6d' % (iteration, error))

    high_res_image.save(high_res_file)



if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    main()
