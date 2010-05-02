#!/usr/bin/env python
import Image


files = ['ksiezyc1.JPG', 'ksiezyc2.JPG']
images = []
output_fname = 'output.JPG'
zoom = 2

for f in files:
    images.append(Image.open(f))

""" create estimated image """
estimation = Image.open(files[0])
bigger_size = (images[0].size[0]*zoom, images[0].size[1]*zoom)
estimation = estimation.resize(bigger_size, Image.ANTIALIAS)


""" aplay in iteration changes """
for i in images:
    """ very image may add sth to output """
    for x in range(0, i.size[0]-30):
        for y in range(0, i.size[1]-30):
            (re,ge,be) = i.getpixel((x,y))
            (ri,gi,bi) = estimated.getpixel((x*zoom,y*zoom))
            #estimation.putpixel((x, y), (hi, hi, hi))


estimation.save(output_fname)


