#!/usr/bin/env python
__version__ =  '0.1'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import Image
import yaml
import math
import random

class MotionEstimator:
    def __init__(self, iteraions_per_check=9):
        self.iteraions_per_check = iteraions_per_check
        self.mask = ((0, 0), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
 

    def compute_offset(self, a, b, start_point):
        width, height = a.size
        x_start, y_start = start_point
        x, y = x_start, y_start 

        p1, p2 = a.getpixel((x, y)), b.getpixel((x, y))
        difference = abs(p1[0] - p2[0])
        smalest_difference = difference

        for i in range(self.iteraions_per_check):
            p = i % len(self.mask)
            x_checked, y_checked = x + self.mask[p][0], y + self.mask[p][1]
            p1, p2 = a.getpixel((x, y)), b.getpixel((x_checked, y_checked))
            difference = abs(p1[0] - p2[0])

            if difference < smalest_difference:
                smalest_difference = difference
                x, y = x_checked, y_checked

        return x - x_start, y - y_start


    def estimate(self, a, b):
        iterations=100

        width, height = a.size
        a = a.resize((width*2, height*2)) 
        b = b.resize((width*2, height*2)) 

        width, height = a.size
        w = 4
        x, y = 0, 0

        for i in range(iterations):
            p = random.randrange(w, width-w), random.randrange(w, height-w)
            xn, yn = self.compute_offset(a, b, p)
            x, y = x + xn, y + yn

        return x / iterations, y / iterations

class EstimationTester:
    def __init__(self, samples, estimator):
        self.samples = samples 
        self.estimator = estimator

    def compare_known_movement(self, expectations):
        results = {'total' : 0, 'image' : []}
        for i in range(1, len(self.samples)):
            x, y = self.estimator.estimate(self.samples[0], self.samples[i])
            error = abs(x - expectations[i][0]) + abs(y - expectations[i][1])
            img = {'expected' : expectations[i], 'computed':(x, y), 'error':error}
            results['total'] += error
            results['image'].append(img)
        return results

    def compare_unknown_movement(self):
        results = {'total' : 0, 'image' : []}
        for i in range(1, len(self.samples)):
            pass
            #x, y = self.estimator.estimate(self.samples[0], self.samples[i])
            #error = abs(x - expectations[i][0]) + abs(y - expectations[i][1])
            #img = {'expected' : expectations[i], 'computed':(x, y), 'error':error}
            #results['total'] += error
            #results['image'].append(img)
        return results


if __name__=="__main__":
    default_config_path = 'motion_estimator_config.yaml'
    config = open(default_config_path, 'r')
    config = yaml.load(config)

    samples = map(lambda u: config['samples_directory'] +u, config['samples_names'])
    images = map(Image.open, samples)
    
    tester = EstimationTester(images, MotionEstimator())
    print tester.compare_known_movement(config['samples_movments'])
    print tester.compare_unknown_movement()

