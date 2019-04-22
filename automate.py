import os, time
import SampleCreator
import SRRestorer

# testing conditions to be modified by user
scaleList = [1]
restoringIterations = 2


samplesDir = './samples'
trainingImagesDir ='./input'

if __name__=="__main__":
    os.makedirs(trainingImagesDir, exist_ok = True)

    startTime = time.time()

    #for each image
    for imageName in os.listdir(samplesDir):
        for scalingFactor in scaleList:
            print('Testing algorithm for %s, iterations: %d, scaling factor: %f' % (imageName, restoringIterations, scalingFactor) )
            print('You can change those values by modyfiying this script.')
            
            originalImagePathName = os.path.join(samplesDir, imageName)
            SampleCreator.main(originalImagePathName, trainingImagesDir, scalingFactor)
            print('Samples created cuccesfully, restoring (this might take time)')

            SRRestorer.main(trainingImagesDir, scalingFactor, restoringIterations)
        
    print('Total elapsed time: %s mins' % str((time.time() - startTime)/60)) 
