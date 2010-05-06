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

def update_by_backprojection(hi_res_img, low_res_images, c):
    for i in low_res_images:
        z = i.resize(hi_res_img.size, Image.ANTIALIAS)

        for x in range(1, hi_res_img.size[0]-30):
            for y in range(1, hi_res_img.size[1]-30):
                (fo,_,_) = hi_res_img.getpixel((x,y))

                small = 0.2125
                v = 0.0
                # center
                (fi,_,_) = z.getpixel((x,y)) 

                v += (fo-fi) * 1.0 / (1+c*small*4)

                # down
                (fi,_,_) = z.getpixel((x,y+1)) 
                v += (fo-fi) * small*small / (1+c*small*4)
                # up
                (fi,_,_) = z.getpixel((x,y-1)) 
                v += (fo-fi) * small*small / (1+c*small*4)
                # left
                (fi,_,_) = z.getpixel((x+1,y)) 
                v += (fo-fi) * small*small / (1+c*small*4)
                # right
                (fi,_,_) = z.getpixel((x-1,y)) 
                v += (fo-fi) * small*small / (1+c*small*4)




                v = int(v)

                hi_res_img.putpixel((x, y), (fo+v, fo+v, fo+v))

    return hi_res_img



def main():
    # TODO this should be moved to config file or read from command line
    low_res_files = ['100_1040.JPG', '100_1041.JPG']

    output_file = 'output.JPG'
    zoom = 2
    iterations = 5
    c = 15.0

    low_res_images = load_images(low_res_files)

    # as a base for high resolution image we will take first low 
    # resolution image, we need to resize it by zoom factor
    hi_res_img = create_hi_res_img(low_res_images[0], zoom)

    for i in range(0, iterations):
        hi_res_img = update_by_backprojection(hi_res_img, low_res_images, c)

    hi_res_img.save(output_file)



if __name__=="__main__":
    main()
