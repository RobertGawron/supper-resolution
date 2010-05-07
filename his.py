#!/usr/bin/env python
import Image
# poor implementation based on theory from:
# M. Irani and S. Peleg, "Super Resolution From Image Sequences"


class RawImage:
    def __init__(self, file_name):
        self.body = []
        img = Image.open(file_name)
        for y in range(0, img.size[1]):
            row = []
            for x in range(0, img.size[0]):
                row.append(img.getpixel((x,y)))
            self.body.append(row)
        self.width = img.size[0]
        self.height = img.size[1]

    def save(self, file_name):
        img = Image.open(file_name)
        size = (self.width, self.height)
        img.resize(size, Image.LINEAR)

        for y in range(0, self.height):
            for x in range(0, self.width):
                img.putpixel((x,y), self.body[y][x])

        img.save(file_name)
    

class SRParams:
    def __init__(self, iterations=10, zoom=2, c=10):
        self.iterations = iterations
        self.zoom = zoom
        self.c = c


class SRImage(RawImage):
    def __init__(self, images, params):
        self.images = images
        self.params = params 

    def save(self, file_name):
        # shit here
        self.img = RawImage(file_name)
        self._create_image()
        self.img.save(file_name)

    def _create_image(self):
        pass

def create_hi_res_img(images, zoom):
    base = images[0]
    second = images[1]
    (width, height) = (len(base[0]), len(base))
    img = []

    for y in range(0, height):
        row = []
        for x in range(0, width):
            row.append(base[y][x])
            #row.append((100,200,0))
            row.append(second[y][x])

        img.append(row)
        img.append(row) 

    return img


def update_by_backprojection(hi_res_img, low_res_images, c):
    (width, height) = (len(hi_res_img[0]), len(hi_res_img))
    sp = []
    for y in range(0, height):
        row = []
        for x in range(0, width):
            if (x%2)==1 or (y%2)==1:
                ""
            else:
                (p1,_,_) = hi_res_img[y][x]
                (p2,_,_) = hi_res_img[y+1][x]
                (p3,_,_) = hi_res_img[y][x+1]
                (p4,_,_) = hi_res_img[y+1][x+1]
                p = int((p1+p2+p3+p4)*0.25)
                row.append((p,p,0))
                #row.append((100,200,0))

        if row != []:
            sp.append(row)
  
    print  (len(sp[0]), len(sp)) 
    

    for low_res_img in low_res_images:
        for x in range(1, len(low_res_img[0])):
            for y in range(1, len(low_res_img[0][0])):
                (hp1, _, _) = hi_res_img[y][x]
                (hp2, _, _) = hi_res_img[y+1][x]
                (hp3, _, _) = hi_res_img[y][x+1]
                (hp4, _, _) = hi_res_img[y+1][x+1]

                (lp, _, _) = low_res_img[x][y]
                try:
                    (sp, _, _) = sp[y][x]
                except:
                    pass


                hp1 += (sp-lp)/c
                x*=2
                y*=2
                hi_res_img[y][x] = (hp1, hp1, hp1)
                hi_res_img[y+1][x] = (hp2, hp2, hp2)
                hi_res_img[y][x+1] = (hp3, hp3, hp3)
                hi_res_img[y+1][x+1] = (hp4, hp4, hp4)

    return hi_res_img
               


def main():
    low_res_files = ['100_1040.JPG', '100_1041.JPG']
    output_file = 'output.JPG'

    params = SRParams(iterations=2, zoom=10, c=10) 
    low_res_images = map(lambda u: RawImage(u), low_res_files)
    sr_image = SRImage(low_res_images, params)
    sr_image.save(output_file)


if __name__=="__main__":
    main()
