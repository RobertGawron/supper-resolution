#!/usr/bin/env python
import Image


original_file = 'original.tif'
o = Image.open(original_file)

hps = [0.2, 1.0, 0.2, 1.0, 3.0, 1.0, 0.2, 1.0, 0.2]
f = 4

for x in range(1, o.size[0]-1):
    for y in range(1, o.size[1]-1):
        p0 = o.getpixel((x, y))

        p1 = o.getpixel((x-1, y-1))
        p2 = o.getpixel((x, y-1))
        p3 = o.getpixel((x+1, y-1))

        p4 = o.getpixel((x-1, y))
        p5 = o.getpixel((x+1, y))

        p6 = o.getpixel((x-1, y+1))
        p7 = o.getpixel((x, y+1))
        p8 = o.getpixel((x+1, y+1))

        out = [0.0, 0.0, 0.0]
        pixels = [p1, p2, p3, p4, p0, p5, p6, p7, p8]
        for i in range(0, len(hps)):
            out[0] += hps[i]*pixels[i][0]
            out[1] += hps[i]*pixels[i][1]
            out[2] += hps[i]*pixels[i][2]

        out[0] /= 9
        out[1] /= 9
        out[2] /= 9

        o.putpixel((x, y), (out[0], out[1], out[2]))



o = o.resize((o.size[0]/f, o.size[1]/f), Image.LINEAR)
o.save('gen_0_0.tif')





o = Image.open(original_file)

for x in range(2, o.size[0]-1):
    for y in range(1, o.size[1]-1):
        p0 = o.getpixel((x, y))

        p1 = o.getpixel((x-1, y-1))
        p2 = o.getpixel((x, y-1))
        p3 = o.getpixel((x+1, y-1))

        p4 = o.getpixel((x-1, y))
        p5 = o.getpixel((x+1, y))

        p6 = o.getpixel((x-1, y+1))
        p7 = o.getpixel((x, y+1))
        p8 = o.getpixel((x+1, y+1))

        out = [0.0, 0.0, 0.0]
        pixels = [p1, p2, p3, p4, p0, p5, p6, p7, p8]
        for i in range(0, len(hps)):
            out[0] += hps[i]*pixels[i][0]
            out[1] += hps[i]*pixels[i][1]
            out[2] += hps[i]*pixels[i][2]

        out[0] /= 9
        out[1] /= 9
        out[2] /= 9

        o.putpixel((x-1, y), (out[0], out[1], out[2]))

o = o.resize((o.size[0]/f, o.size[1]/f), Image.LINEAR)
o.save('gen_1_0.tif')

