#!/usr/bin/env python
import Image


files = ['ksiezyc1.JPG', 'ksiezyc2.JPG']
images = []
output_fname = 'output.JPG'
zoom = 2

for f in files:
    images.append(Image.open(f))


