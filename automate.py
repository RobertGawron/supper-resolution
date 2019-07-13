"""
This module automates generation of test images and restoration of higher resolution image via super-resolution algorithm.

Input argument is filename of original (high resolution) image from ./input directory. Example of how to run the script:

     python3 automate.py circuit.tif


Steps this script performs:
1. generation of low resolution images in ./samples that will be taken as an input for super-resolution algorithm
2. Restore high resolution image in iterations
3. Output image is in ./samples named super_resolution.tif
"""

import os, sys, time
import SampleCreator
import SRRestorer
import srconfig

samplesDir = './samples'

if __name__=="__main__":
    # get input file name
    imageName = sys.argv[1]

    # remove artifacts from previous tests
    for file in os.scandir(srconfig.cfg['inputImageDirectory']):
        os.unlink(file.path)

    os.makedirs(srconfig.cfg['inputImageDirectory'], exist_ok = True)
    startTime = time.time()
  
    print('Testing algorithm for %s, iterations: %d, scaling factor: %f' % (imageName, srconfig.cfg['iterations'], srconfig.cfg['scale']) )
    
    originalImagePathName = os.path.join(samplesDir, imageName)
    SampleCreator.main(originalImagePathName, srconfig.cfg['inputImageDirectory'], srconfig.cfg['scale'])
    print('Samples created cuccesfully, restoring (this might take time)')

    SRRestorer.main(srconfig.cfg['inputImageDirectory'], srconfig.cfg['scale'], srconfig.cfg['iterations'])
        
    print('Total elapsed time: %s mins' % str((time.time() - startTime)/60)) 
