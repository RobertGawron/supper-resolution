#!/usr/bin/env python
import Image
import logging

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
    original_file = 'original.tif'
    hps = (0.5, 1.0, 0.5, 
           1.0, 3.0, 1.0,
           0.5, 1.0, 0.5)
    f = 3

    real_img = Image.open(original_file)

    i0 = take_a_photo(real_img, (0,0), hps, f)
    i1 = take_a_photo(real_img, (0,1), hps, f)
    i2 = take_a_photo(real_img, (1,0), hps, f)
    i3 = take_a_photo(real_img, (1,1), hps, f)

    i0.save('gen_0_0.tif')
    i1.save('gen_0_1.tif')
    i2.save('gen_1_0.tif')
    i3.save('gen_1_1.tif')


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    main()
