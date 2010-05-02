#!/usr/bin/env python
import Image
# this code is full of shit

files = ['moon1.JPG', 'moon2.JPG']
images = []
output_fname = 'output.JPG'
zoom = 2
c = 2.2

for f in files:
    images.append(Image.open(f))

""" create estimated image """
estimated = Image.open(files[0])
bigger_size = (images[0].size[0]*zoom, images[0].size[1]*zoom)
estimated = estimated.resize(bigger_size, Image.ANTIALIAS)


for i in images:
    """ every image may add sth to the output """


    z = i.resize(bigger_size, Image.ANTIALIAS) 
   
    for x in range(0, estimated.size[0]-30):
        for y in range(0, estimated.size[1]-30):
            (fo,_,_) = estimated.getpixel((x,y))
            (fi,_,_) = z.getpixel((x,y)) 

            v = int((fo-fi)*c)
            estimated.putpixel((x, y), (fo+v, fo+v, fo+v))


estimated.save(output_fname)

