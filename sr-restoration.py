#!/usr/bin/env python
import Image
import math


def main():
    low_res_files = [('gen_0_0.tif', (0,0)), ('gen_1_0.tif', (1,0))]
    output_file = 'output.tif'
    hps = [0.2, 1.0, 0.2, 1.0, 3.0, 1.0, 0.2, 1.0, 0.2]


    d = [ [hps[0], hps[1], hps[2]], 
            [hps[3], hps[4], hps[5]], 
            [hps[6], hps[7], hps[8]] ]

    for x in range(0,3):
        for y in range(0,3):
            d[x][y] = 0
            for i in range(0,3):
                d[x][y] += d[x][i] * d[i][y]

    #hps = [d[0][0], d[0][1], d[0][2], d[1][0], d[1][1], d[1][2], d[2][0], d[2][1], d[2][2]]
    print hps

    f = 4

    low_res_imgs = map(lambda (f,v):  (Image.open(f),v), low_res_files)
    base_for_estimation = low_res_imgs[0][0]
    estimation = base_for_estimation.resize((base_for_estimation.size[0]*f, base_for_estimation.size[1]*f), Image.LINEAR)

    for iter in range(0, 4):
        #pierwsze zdjecie
        o = estimation.copy()

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

        o1 = o # !!!


        o = 1
        #drugie zdjecie
        o = estimation.copy()
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
        
        o2 = o # !!!

        o = 5

        # robie diffa do pierwszego
        for x in range(1, o1.size[0]-1):
            for y in range(1, o1.size[1]-1):
                (r, g, b) = o1.getpixel((x, y))
                (r0, g0, b0) = low_res_imgs[0][0].getpixel((x, y))
                r -= r0
                g -= g0
                b -= b0
                o1.putpixel((x,y), (r,g,b))


        # robie diffa do drugiego
        for x in range(2, o2.size[0]-1):
            for y in range(1, o2.size[1]-1):
                (r, g, b) = o2.getpixel((x, y))
                (r0, g0, b0) = low_res_imgs[1][0].getpixel((x, y))
                r += r0
                g += g0
                b += b0
                o2.putpixel((x,y), (r,g,b))
 
        #print estimation.size, low_res_imgs[0][0].size, o2.size"""
  
        o1 = o1.resize((o1.size[0]*f, o1.size[1]*f), Image.LINEAR)
        o2 = o2.resize((o2.size[0]*f, o2.size[1]*f), Image.LINEAR)
        c = 3.0

        o1.save('dupa1.tif')
        o2.save('dupa2.tif')

        for x in range(1, o1.size[0]-1):
            for y in range(1, o1.size[1]-1):
                (r, g, b) = estimation.getpixel((x, y))
                (r1, g1, b1) = o1.getpixel((x, y))
                (r2, g2, b2) = o2.getpixel((x+1, y))

                #r += int((r1*r2) * c)
                #g += int((g1*g2) * c)
                #b += int((b1*b2) * c)
                r1 = 0
                if (r1+r2) * c < 0:
                    r += (r1+r2)*c
                elif (r1+r2) * c > 0:
                    r -= (r1+r2)*c

                g = r
                b = r

                estimation.putpixel((x,y), (r,g,b))




    estimation.save(output_file)




if __name__=="__main__":
    main()
