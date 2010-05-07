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
        self._create_init_sr_image()

    def _create_init_sr_image(self):
        first = self.images[0]
        second = self.images[1]
        self.img.body = []

        # TODO add zoom here
        for y in range(0, self.img.height):
            row = []
            for x in range(0, self.img.width):
                #row.append(first[y][x])
                row.append((200, 200, 0))
                row.append(second[y][x])

            self.img.body.append(row)
            self.img.body.append(row) 





def main():
    low_res_files = ['100_1040.JPG', '100_1041.JPG']
    output_file = 'output.JPG'

    params = SRParams(iterations=2, zoom=10, c=10) 
    low_res_images = map(lambda u: RawImage(u), low_res_files)
    sr_image = SRImage(low_res_images, params)
    sr_image.save(output_file)


if __name__=="__main__":
    main()
