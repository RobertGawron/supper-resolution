# Supper-resolution

## Abstract

Super resolution (SR) algorithms are used to obtain high resolution images from a set of low resolution samples. The high resolution image contains more information that single low resolution sample image, so it's different from simple resize algorithms, where the amount of information in image stay the same after upsize.

There are a couple of the main methods to obtain mentioned effect, including statistical methods, transform image info frequency domain, using neural network, or mixing it.

Where SR algorithms are used? In **military** (spying satellites), **astronomy** (telescopes), **medicine** (data from tomography) and others.

## Limitations

To obtain high resolution images, it's needed PSF function and movement of sample images. This is "must have", but if there are more data available (e.g. details of optic in camera or camera's movement), then it's possible to create better model and obtain better results.

Low resolution images used as a base for creating higher resolution image must have some movements. It can be e.g. move of satellite or move of camera. This movement is required for performing the SR algorithm.

## Instalation and usage

[Instruction on Wiki](https://github.com/RobertGawron/supper-resolution/wiki/Installation-and-usage)

## More details

* [Super Resolution From Image Sequences Michal Irani and Shmuel Peleg](http://www.cs.huji.ac.il/~peleg/papers/icpr90-SuperResolutionSequences.pdf) - this project is based on ide described in this paper
* [More info about this project, how to use it etc.](http://robertgawron.blogspot.com/2011/01/super-resolution-algorithm-implemented.html)
* [Estimating motion for SR](http://robertgawron.blogspot.com/2013/03/motion-estimation-for-super-resolution.html)



