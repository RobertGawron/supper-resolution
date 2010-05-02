#!/usr/bin/env python
import Image


files = ['moon1.JPG', 'moon2.JPG']
images = []
output_fname = 'output.JPG'
zoom = 2
c = 3

for f in files:
    images.append(Image.open(f))

""" create estimated image """
estimated = Image.open(files[0])
bigger_size = (images[0].size[0]*zoom, images[0].size[1]*zoom)
estimated = estimated.resize(bigger_size, Image.ANTIALIAS)


for i in images:
    """ every image may add sth to the output """
    for x in range(0, i.size[0]-30):
        for y in range(0, i.size[1]-30):
            (re,ge,be) = i.getpixel((x,y))
            (ri,gi,bi) = estimated.getpixel((x*zoom,y*zoom))

            r = (re - ri)*c
            """the are all black and white so whatever"""
            estimated.putpixel((x*zoom*1.0, y*zoom*1.0), (r, r, r))


estimated.save(output_fname)

