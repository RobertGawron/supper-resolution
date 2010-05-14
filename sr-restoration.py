#!/usr/bin/env python
import Image
import math
import logging

def take_a_photo(hi_res, move, hps, f):
    lo = Image.new('RGB',hi_res.size)

    for x in range(1, lo.size[0]-1):
        for y in range(1, lo.size[1]-1):
            p0 = hi_res.getpixel((x, y))

            p1 = hi_res.getpixel((x-1, y-1))
            p2 = hi_res.getpixel((x, y-1))
            p3 = hi_res.getpixel((x+1, y-1))

            p4 = hi_res.getpixel((x-1, y))
            p5 = hi_res.getpixel((x+1, y))

            p6 = hi_res.getpixel((x-1, y+1))
            p7 = hi_res.getpixel((x, y+1))
            p8 = hi_res.getpixel((x+1, y+1))

            out = [0.0, 0.0, 0.0]
            pixels = [p1, p2, p3, p4, p0, p5, p6, p7, p8]

            for i in range(0, len(hps)):
                out[0] += hps[i]*pixels[i][0]
                out[1] += hps[i]*pixels[i][1]
                out[2] += hps[i]*pixels[i][2]

            out = map(lambda u: int(u/30), out)
            lo.putpixel((x-move[0], y+move[1]), (out[0], out[1], out[2]))


    return lo.resize((hi_res.size[0]/f, hi_res.size[1]/f), Image.LINEAR)


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
    hps = [0.2, 1.0, 0.2, 1.0, 3.0, 1.0, 0.2, 1.0, 0.2]
    hps = [1.080, 3.400, 1.080, 3.400, 11.000, 3.400, 1.080, 3.400, 1.080]
    logging.debug(hps)

    f = 4

    low_res_imgs = map(lambda (f,v):  (Image.open(f),v), low_res_files)
    base_for_estimation = low_res_imgs[0][0]
    estimation = base_for_estimation.resize((base_for_estimation.size[0]*f, base_for_estimation.size[1]*f), Image.LINEAR)

    for iter in range(0, 3):
        logging.info('iteration #%d' % iter)

        # symulujemy robienie zdjecia
        i0 = take_a_photo(estimation, (0,0), hps, f)
        i1 = take_a_photo(estimation, (1,0), hps, f)

        # szukamy bledu miedzy estymacja a zdjeciem LR
        i0 = make_diff(i0, low_res_imgs[0][0])
        i1 = make_diff(i1, low_res_imgs[1][0])
 
        # robi resiza by dopasowac rozmiar LR do SR przed nanoszeniem diffow  
        i0 = i0.resize((i0.size[0]*f, i0.size[1]*f), Image.LINEAR)
        i1 = i1.resize((i1.size[0]*f, i1.size[1]*f), Image.LINEAR)

        i0.save('dupa1.tif')
        i1.save('dupa2.tif')

        c =  0.25

        for x in range(0, i0.size[0]-1):
            for y in range(0, i0.size[1]):
                (r, g, b) = estimation.getpixel((x, y))
                (r1, g1, b1) = i0.getpixel((x, y))
                (r2, g2, b2) = i1.getpixel((x+1, y))

                r += int((r1+r2) * c)
                g += int((g1+g2) * c)
                b += int((b1+b2) * c)

                estimation.putpixel((x,y), (r,g,b))


    estimation.save(output_file)




if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    main()
