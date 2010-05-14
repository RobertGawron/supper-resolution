#!/usr/bin/env python
import Image
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

            out = map(lambda u: int(u/10), out) # fuck
            lo.putpixel((x+move[0], y+move[1]), (out[0], out[1], out[2]))


    return lo.resize((hi_res.size[0]/f, hi_res.size[1]/f), Image.LINEAR)



def main():
    original_file = 'original.tif'
    hps = [1.0, 1.0, 1.0, 1.0]
    f = 4

    real_img = Image.open(original_file)

    i0 = take_a_photo(real_img, (0,0), hps, f)
    i1 = take_a_photo(real_img, (1,0), hps, f)

    i0.save('gen_0_0.tif')
    i1.save('gen_1_0.tif')


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    main()
