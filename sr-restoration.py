#!/usr/bin/env python
import Image
import math
import logging

def take_a_photo(hi_res, move, hps, f):
    lo = Image.new('RGB',hi_res.size)

    for x in range(1, lo.size[0]-1):
        for y in range(1, lo.size[1]-1):
            p0 = hi_res.getpixel((x, y))
            p1 = hi_res.getpixel((x+1, y))
            p2 = hi_res.getpixel((x, y+1))
            p3 = hi_res.getpixel((x+1, y+1))

            out = [0.0, 0.0, 0.0]
            pixels = [p0, p1, p2, p3]

            for i in range(0, len(hps)):
                out[0] += hps[i]*pixels[i][0]
                out[1] += hps[i]*pixels[i][1]
                out[2] += hps[i]*pixels[i][2]

            out = map(lambda u: int(u/30), out)
            lo.putpixel((x+move[0], y+move[1]), (out[0], out[1], out[2]))


    return lo.resize((hi_res.size[0]/f, hi_res.size[1]/f), Image.BICUBIC)


def make_diff(base, mask):
    for x in range(1, base.size[0]-1):
        for y in range(1, base.size[1]-1):
            (r, g, b) = base.getpixel((x, y))
            (r0, g0, b0) = mask.getpixel((x, y))
            r -= r0
            g -= g0
            b -= b0
            base.putpixel((x,y), (r,g,b))
    return base



def main():
    low_res_files = [('gen_0_0.tif', (0,0)), ('gen_1_0.tif', (1,0))]
    output_file = 'output.tif'
    hps = [1.0, 1.0, 1.0, 1.0]
    hps = [4.0, 4.0, 4.0, 4.0]

    logging.debug(hps)

    f = 4

    low_res_imgs = map(lambda (f,v):  (Image.open(f),v), low_res_files)
    base_for_estimation = low_res_imgs[0][0]
    estimation = base_for_estimation.resize((base_for_estimation.size[0]*f, base_for_estimation.size[1]*f), Image.LINEAR)

    for iter in range(0, 7):
        total_error = 0

        # symulujemy robienie zdjecia
        i0 = take_a_photo(estimation, (0,0), hps, f)
        i1 = take_a_photo(estimation, (1,0), hps, f)

        # szukamy bledu miedzy estymacja a zdjeciem LR
        i0 = make_diff(low_res_imgs[0][0], i0)
        i1 = make_diff(low_res_imgs[1][0], i1)
 
        # robi resiza by dopasowac rozmiar LR do SR przed nanoszeniem diffow  
        i0 = i0.resize((i0.size[0]*f, i0.size[1]*f), Image.BICUBIC)
        i1 = i1.resize((i1.size[0]*f, i1.size[1]*f), Image.BICUBIC)

        c =  0.8

        for x in range(0, i0.size[0]-1):
            for y in range(0, i0.size[1]):
                for observed in (i0, i1):
                    (r, g, b) = estimation.getpixel((x, y))
                    (ro, go, bo) = observed.getpixel((x, y))
                    total_error += ro

                    
                    if ro > 0:
                        ro = 1
                    elif ro < 0:
                        ro = 0
                    #r += int(ro * c)
                    #g += int(go * c)
                    #b += int(bo * c)

                    g = r
                    b = r
                    estimation.putpixel((x,y), (r,g,b))

        logging.info('iteration #%2d done, estimation error: %10d' % (iter, total_error))

    estimation.save(output_file)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    main()
