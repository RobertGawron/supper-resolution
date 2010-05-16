#!/usr/bin/env python
import Image
import math
import logging

def take_a_photo(hi_res, offset, hps, f):
    size = hi_res.size
    lo = Image.new('RGB', size)

    mask = ((-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1))

    for x in range(1+offset[0], hi_res.size[0]-1-offset[0]):
        for y in range(1+offset[1], hi_res.size[1]-1-offset[1]):
            used_pixels = map(lambda (i,j): hi_res.getpixel((x+i, y+j)), mask)    
            
            (r, g, b) = (0, 0, 0)
            for (pixel, weight) in zip(used_pixels, hps):
                (r, g, b) = (r + pixel[0] * weight, g + pixel[1] * weight, b + pixel[2] * weight) 
                
            scale = len(used_pixels)
            (r, g, b) = (r/scale, g/scale, b/scale)

            lo.putpixel((x+offset[0], y+offset[1]), (r, g, b))

    return lo.resize((hi_res.size[0]/f, hi_res.size[1]/f), Image.BICUBIC)


def make_diff(base, mask):
    for x in range(1, base.size[0]-1):
        for y in range(1, base.size[1]-1):
            (r, g, b) = base.getpixel((x, y))
            (r0, g0, b0) = mask.getpixel((x, y))
            r = r - r0 + 100
            g = g - g0 + 100
            b = b - b0 + 100
            base.putpixel((x,y), (r,g,b))
    return base



def main():
    low_res_files = [('gen_0_0.tif', (0,0)), 
                     ('gen_0_1.tif', (0,1)), 
                     ('gen_1_0.tif', (1,0)), 
                     ('gen_1_1.tif', (1,1))]
    output_file = 'output.tif'
    hps = (0.5, 1.0, 0.5, 
           1.0, 3.0, 1.0,
           0.5, 1.0, 0.5)

    logging.debug(hps)

    f = 3

    low_res_imgs = map(lambda (f,v):  (Image.open(f),v), low_res_files)
    base_for_estimation = low_res_imgs[0][0]
    estimation = base_for_estimation.resize((base_for_estimation.size[0]*f, base_for_estimation.size[1]*f), Image.LINEAR)

    for iter in range(0, 1):
        total_error = 0

        # symulujemy robienie zdjecia
        i0 = take_a_photo(estimation, (0,0), hps, f)
        i1 = take_a_photo(estimation, (0,1), hps, f)
        i2 = take_a_photo(estimation, (1,0), hps, f)
        i3 = take_a_photo(estimation, (1,1), hps, f)

        # szukamy bledu miedzy estymacja a zdjeciem LR
        i0 = make_diff(low_res_imgs[0][0], i0)
        i1 = make_diff(low_res_imgs[1][0], i1)
        i2 = make_diff(low_res_imgs[2][0], i2)
        i3 = make_diff(low_res_imgs[3][0], i3)

 
        # robi resiza by dopasowac rozmiar LR do SR przed nanoszeniem diffow  
        i0 = i0.resize((i0.size[0]*f, i0.size[1]*f), Image.BICUBIC)
        i1 = i1.resize((i1.size[0]*f, i1.size[1]*f), Image.BICUBIC)
        i2 = i2.resize((i2.size[0]*f, i2.size[1]*f), Image.BICUBIC)
        i3 = i3.resize((i3.size[0]*f, i3.size[1]*f), Image.BICUBIC)

        c =  0.8

        for x in range(2, i0.size[0]-2):
            for y in range(2, i0.size[1]-2):
                for (observed, (i,j)) in ((i0,(0,0)), (i1,(0,1)), (i2,(1,0)), (i3,(1,1))):
                    (r, g, b) = estimation.getpixel((x, y))
                    (ro, go, bo) = observed.getpixel((x+i, y+j))
                    (ro, go, bo) =  (ro-100, go-100, bo-100) 

                    total_error += ro
                    
                    r += int(ro * c)
                    g += int(go * c)
                    b += int(bo * c)

                    estimation.putpixel((x,y), (r,g,b))

        logging.info('iteration #%2d done, estimation error: %10d' % (iter, total_error))

    estimation.save(output_file)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    main()
