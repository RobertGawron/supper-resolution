#!/usr/bin/env python
import Image
# poor code based on theory from:
# M. Irani and S. Peleg, "Super Resolution From Image Sequences"

"""for f in low_res_files:
    low_res_images.append(Image.open(f))

estimated = Image.open(files[0])
bigger_size = (images[0].size[0]*zoom, images[0].size[1]*zoom)
estimated = estimated.resize(bigger_size, Image.ANTIALIAS)


for i in images:

    z = i.resize(bigger_size, Image.ANTIALIAS) 
   
    for x in range(0, estimated.size[0]-30):
        for y in range(0, estimated.size[1]-30):
            (fo,_,_) = estimated.getpixel((x,y))
            (fi,_,_) = z.getpixel((x,y)) 

            v = int((fo-fi)*c)
            estimated.putpixel((x, y), (fo+v, fo+v, fo+v))




estimated.save(output_fname)
"""

def load_images(files):
    images = []
    for f in files:
        images.append(Image.open(f))
    return images

def main():
    low_res_files = ['moon1.JPG', 'moon2.JPG']
    low_res_images = load_images(low_res_files)
    output_file = 'output.JPG'
    zoom = 2
    c = 2.2


if __name__=="__main__":
    main()
