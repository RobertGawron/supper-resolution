#!/usr/bin/env python
import Image
import math
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
        size = (self.width, self.height)
        img = Image.new("RGB", size)

        for y in range(0, self.height):
            for x in range(0, self.width):
                img.putpixel((x,y), self.body[y][x])

        img.save(file_name)
    
    def scale(self, factor):
        # TODO add zoom here
        scaled = []
        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                if (x%2)==0 and (y%2)==0:
                    (p1,_,_) = self.body[y][x]
                    (p2,_,_) = self.body[y+1][x]
                    (p3,_,_) = self.body[y][x+1]
                    (p4,_,_) = self.body[y+1][x+1]
                    p = int((p1+p2+p3+p4)*0.25)
                    row.append((p,p,p))

            if row != []:
                scaled.append(row)

        self.body = scaled    


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
        self._create_init_sr_image()

        for n in range(0, self.params.iterations):
            print self._get_error() 
            self._update_by_backprojection()
    

    def _get_error(self):
        sp = self._simulate_making_img()
        error = 0
        for i in self.images:
            for y in range(0, i.height):
                for x in range(0, i.width):
                    error += abs(sp[y][x] - i.body[y][x][0])
        return error/float(i.height*i.width)

    def _simulate_making_img(self):
        simulated = []
        z = self.params.zoom
        for y in range(0, self.img.height/z):
            row = []
            for x in range(0, self.img.width/z):

                (p0,_,_) = self.img.body[y*z][x*z]

                (p1,_,_) = self.img.body[y*z-1][x*z-1]
                (p2,_,_) = self.img.body[y*z-1][x*z]
                (p3,_,_) = self.img.body[y*z-1][x*z+1]

                (p4,_,_) = self.img.body[y*z][x*z-1]
                (p5,_,_) = self.img.body[y*z][x*z+1]

                (p6,_,_) = self.img.body[y*z+1][x*z-1]
                (p7,_,_) = self.img.body[y*z+1][x*z]
                (p8,_,_) = self.img.body[y*z+1][x*z+1]

                row.append( int( (0.4*p0 + 0.6*(p1+p2+p3+p4+p5+p6+p7+p8))/9.0 ) )

            simulated.append(row)

        return simulated

    def _update_by_backprojection(self):
        #sp = self._simulate_making_img()

        for low_res_img in self.images:
            sp = self._simulate_making_img()

            for y in range(1, low_res_img.height-1):
                for x in range(1, low_res_img.width-1):
                    (hp1, _, _) = self.img.body[y*2][x*2]
                    (hp2, _, _) = self.img.body[y*2+1][x*2]
                    (hp3, _, _) = self.img.body[y*2][x*2+1]
                    (hp4, _, _) = self.img.body[y*2+1][x*2+1]

                    (lp, _, _) = low_res_img.body[y][x]
                    spp = sp[y][x]
    
                    diff = int(float(spp-lp)/self.params.c) % 5

                    hp1 += diff
                    hp2 += diff
                    hp3 += diff
                    hp4 += diff
                    
                    self.img.body[y*2][x*2] = (hp1, hp1, hp1)
                    self.img.body[y*2+1][x*2] = (hp2, hp2, hp2)
                    self.img.body[y*2][x*2+1] = (hp3, hp3, hp3)
                    self.img.body[y*2+1][x*2+1] = (hp4, hp4, hp4)



    def _create_init_sr_image(self):
        # shit here
        first = self.images[0]
        second = self.images[1]
        self.img.body = []

        # TODO add zoom here
        for y in range(0, first.height):
            row = []

            for x in range(0, first.width):
                row.append(first.body[y][x])
                row.append(second.body[y][x])

            self.img.body.append(row)
            self.img.body.append(row) 

        self.img.width = first.width*2
        self.img.height = first.height*2


def main():
    low_res_files = ['100_1048.JPG', '100_1048.JPG']
    output_file = 'output.tif'

    params = SRParams(iterations=8, zoom=2, c=10) 
    low_res_images = map(lambda u: RawImage(u), low_res_files)
    sr_image = SRImage(low_res_images, params)
    sr_image.save(output_file)


if __name__=="__main__":
    main()
