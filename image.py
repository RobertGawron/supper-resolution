#!/usr/bin/env python
__version__ =  '1.11'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'

import sys
import yaml
import Image 
from SuperResolution import SamplesCreator
from SuperResolution import MotionEstimator
from SuperResolution import SRRestorer

# TODO is this needed at all>
def parse_config_file(config_path):
    config = open(config_path, 'r')
    config = yaml.load(config)
    return config

# TODO this is fucked, but it works
def get_samples(defaults, cmd_args):
    config = parse_config_file(defaults['config_path'])
    scale = defaults['downscale']
    input_image = Image.open(cmd_args[0])
    SamplesCreator.stub(input_image, scale, config)

def get_movement(defaults, cmd_args):
    MotionEstimator.stub()


def sr_restoration(defaults, cmd_args):
    
    SRRestorer.stub()

if __name__ == "__main__":
    # image.py samples path 3
    defaults = {'config_path' : 'config.yaml',
                'downscale' : 3}

    actions = { 'samples' : get_samples, 
                'movement': get_movement,
                'restore' : sr_restoration}

    for key in actions:
        if key == sys.argv[1]:
            actions[key](defaults, sys.argv[2:])
