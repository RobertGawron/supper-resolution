#!/usr/bin/env python
import math
import logging
import Image



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

    return lo.resize((hi_res.size[0]/f, hi_res.size[1]/f), Image.ANTIALIAS)




def main():
    low_res_files = [('gen_0_0.tif', (0,0)), 
                     ('gen_0_1.tif', (0,1)), 
                     ('gen_1_0.tif', (1,0)), 
                     ('gen_1_1.tif', (1,1))]

    output_file = 'gen_estimation.tif'

    hps = (0.5, 1.0, 0.5, 
           1.0, 3.0, 1.0,
           0.5, 1.0, 0.5)

    logging.debug(hps)

    f = 3

    low_res_imgs = map(lambda (f,v):  (Image.open(f),v), low_res_files)
    base_for_estimation = low_res_imgs[0][0]
    estimation = base_for_estimation.resize((base_for_estimation.size[0]*f, base_for_estimation.size[1]*f), Image.ANTIALIAS)

    K = len(low_res_imgs)

    for iter in range(0, 30):
        total_error = 0

        # symulujemy robienie zdjecia
        i0 = take_a_photo(estimation, (0,0), hps, f)
        i1 = take_a_photo(estimation, (0,1), hps, f)
        i2 = take_a_photo(estimation, (1,0), hps, f)
        i3 = take_a_photo(estimation, (1,1), hps, f)

        # robie diffa na LR, rzutuje hsp na HR
        for (key, lr_estimated, (iz,jz)) in ((0, i0,(0,0)), (1, i1,(0,1)), (2, i2,(1,0)), (3, i3,(1,1))):
            diff = Image.new('RGB', i0.size)

            for x in range(0, lr_estimated.size[0]):
                for y in range(0, lr_estimated.size[1]):
                    (r, g, b) = low_res_imgs[key][0].getpixel((x, y))
                    (r0, g0, b0) = lr_estimated.getpixel((x, y))

                    total_error += abs(r - r0)

                    r = ((r - r0)/2 ) + 120
                    g = ((g - g0)/2 ) + 120
                    b = ((b - b0)/2 ) + 120

                    diff.putpixel((x, y), (r, g, b))
                    
                    
            # diff
            diff = diff.resize((diff.size[0]*f, diff.size[1]*f), Image.ANTIALIAS)


            # robie hpsa
            hpsowane = Image.new('RGB', diff.size)
            for x in range(1, hpsowane.size[0]-1):
                for y in range(1, hpsowane.size[1]-1):


                    hpsx = [4.5, 12.0, 4.5, 12.0, 33.0, 12.0, 4.5, 12.0, 4.5]


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

                    r /= 9*9


                    (a1,a2,a3) = estimation.getpixel((x-iz,y-jz))
                    a1 += r/K
                    
                    estimation.putpixel((x-iz,y-jz), (a1,a1,a1))

        estimation.save('_'+str(iter)+output_file)
        logging.info('iteration #%2d done, estimation error: %6d' % (iter, total_error/K))

    estimation.save(output_file)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    main()
