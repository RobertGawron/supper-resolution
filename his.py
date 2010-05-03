#!/usr/bin/env python
import Image
# poor code based on theory from:
# M. Irani and S. Peleg, "Super Resolution From Image Sequences"

def load_images(files):
    images = []
    for f in files:
        images.append(Image.open(f))
    return images

def create_hi_res_img(base_img, zoom):
    img  = base_img
    new_size = (base_img.size[0]*zoom, base_img.size[1]*zoom)
    return img.resize(new_size, Image.ANTIALIAS)

def main():
    # TODO this should be moved to config file or read from command line
    low_res_files = ['moon1.JPG', 'moon2.JPG']
    output_file = 'output.JPG'
    zoom = 2
    c = 2.2

    low_res_images = load_images(low_res_files)

    # as a base for high resolution image we will take first low 
    # resolution image, we need to resize it by zoom factor
    hi_res_img = create_hi_res_img(low_res_images[0], zoom)

    for i in low_res_files:
        z = i.resize(bigger_size, Image.ANTIALIAS)

        for x in range(0, estimated.size[0]-30):
            for y in range(0, estimated.size[1]-30):
                (fo,_,_) = estimated.getpixel((x,y))
                (fi,_,_) = z.getpixel((x,y)) 

                v = int((fo-fi)*c)
                estimated.putpixel((x, y), (fo+v, fo+v, fo+v))
       


    hi_res_img.save(output_file)



if __name__=="__main__":
    main()
