#!/usr/bin/env python
__version__ =  '0.1'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import math
import random
import pprint
import Image
import ImageOps
import yaml

class EstimationTester:
    def __init__(self, samples, estimator):
        self.samples = samples 
        self.estimator = estimator

    def compare_known_movement(self, expectations):
        results = {'total' : 0, 'image' : []}
        for i in range(1, len(self.samples)):
            x, y = self.estimator.estimate(self.samples[0], self.samples[i])
            error = abs(x - expectations[i][0]) + abs(y - expectations[i][1])
            img = {'expected' : expectations[i], 'estimated' : (x, y), 'error' : error}
            results['total'] += error
            results['image'].append(img)
        return results

    def compare_unknown_movement(self):
        width, height = self.samples[0].size
        results = {'total' : 0, 'image' : []}
        for i in range(1, len(self.samples)):
            difference = 0
            dx, dy = self.estimator.estimate(self.samples[0], self.samples[i])
            for x in range(abs(dx), width - abs(dx)):
                for y in range(abs(dy), height - abs(dy)):
                    p1 = images[0].getpixel((x + dx, y + dy))
                    p2 = images[i].getpixel((x, y))
                    difference += abs(p1 - p2)
            img = {'error' : difference/width*height}
            results['image'].append(img)
            results['total'] += difference
        return results

class MotionEstimator:
    def __init__(self, iteraions_per_check=9):
        self.iteraions_per_check = iteraions_per_check
        #self.mask = ((0, 0), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
        self.mask = ((-1, -1), (0, -1), (1, -1), 
                     (-1,  0), (0,  0), (1,  0), 
                     (-1,  1), (0,  1), (1,  1) )

        self._mask = ((-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), 
                     (-2, -2), (-1, -1), (0, -1), (1, -1), (2, -1), 
                     (-2, -2), (-1,  0), (0,  0), (1,  0), (2,  0), 
                     (-2, -2), (-1,  1), (0,  1), (1,  1), (2,  1), 
                     (-2, -2), (-1,  2), (0,  2), (1,  2), (2,  2), )

        self._mask = (( 0,  0), ( 1,  0), (-1,  1), (0,  1), (1,  1), 
                     (-1,  0), (-1, -1), (0, -1), (1, -1), (2, -1), 
                     ( 2,  0), ( 2,  1), (2,  2), (1,  2), (0,  2), (-1, 2), 
                        (-2, -2),(-2, -2), (-2, -2), (-2, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2))


        self.mask = ((0, 0), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
    def compute_offset(self, a, b, (x, y)):
        """# compute initial difference
        p1, p2 = a.getpixel((x, y)), b.getpixel((x+self.mask[0][0], y+self.mask[0][1]))
        difference = abs(p1 - p2)
        smalest_difference = difference
        estimation = self.mask[0] 

        for dx, dy in self.mask:
            p1, p2 = a.getpixel((x, y)), b.getpixel((x + dx, y + dy))
            difference = abs(p1 - p2)
            if difference < smalest_difference:
                smalest_difference = difference
                estimation = (dx, dy) 

        return estimation""" 

        
        x_start, y_start = x, y
        p1, p2 = a.getpixel((x, y)), b.getpixel((x, y))
        difference = abs(p1 - p2)
        smalest_difference = difference

        for i in range(self.iteraions_per_check):
            p = i % len(self.mask)
            x_checked, y_checked = x + self.mask[p][0], y + self.mask[p][1]
            p1, p2 = a.getpixel((x, y)), b.getpixel((x_checked, y_checked))
            difference = abs(p1 - p2)

            if difference < smalest_difference:
                smalest_difference = difference
                x, y = x_checked, y_checked

        return x - x_start, y - y_start

    def estimate(self, base_img, checked_img, iterations=100):
        width, height = base_img.size
        w = 5 # TODO where this belongs?
        x, y = 0, 0

        for i in range(iterations):
            point = random.randrange(w, width-w), random.randrange(w, height-w)
            xn, yn = self.compute_offset(base_img, checked_img, point)
            x, y = x + xn, y + yn

        return x / iterations, y / iterations


if __name__=="__main__":
    default_config_path = 'motion_estimator_config.yaml'
    config = open(default_config_path, 'r')
    config = yaml.load(config)
    # there is no need to use pretty printer here, it's only for better readability
    screen = pprint.PrettyPrinter(indent=3, width=16)
 
    samples = map(lambda u: config['samples_directory'] + u, config['samples_names'])
    images = map(Image.open, samples)
    # is resizing needed? 
    englargment = images[0].size[0] * 2, images[0].size[1] * 2
    # convert to grayscale
    images = map(lambda u: ImageOps.grayscale(u), images)
    # resize
    images = map(lambda u: u.resize(englargment), images)
   
    screen.pprint('** calculating movement, first image is base image **')
    e = MotionEstimator()
    base_img = images[0]

    #for i,j in zip(images[1:], config['samples_movments'][1:]):
    #    results = e.estimate(base_img, i)
    #    print results , j

    screen.pprint( map(lambda u: e.estimate(base_img, u), images[1:]) )
    
    tester = EstimationTester(images, MotionEstimator())
    screen.pprint('** checking estimation quality [known movement] **')
    screen.pprint(tester.compare_known_movement(config['samples_movments']))

    #screen.pprint('** checking estimation quality [unknown movement] **')
    #screen.pprint(tester.compare_unknown_movement())

