import os, time
import SampleCreator
import SRRestorer

startTime = time.time()
samplesDir = './set'
errorFile = 'errors.txt'
scaleList = [0.5, 1, 2]

#for each image
for i in os.listdir(samplesDir):
    #iterations
    for j in range(10, 50, 10):
        #different scales
        for k in scaleList:
            sampleDir = 'sample_' + i[:-4] + '_' + str(k) + '_' + str(j)
            try:
                SampleCreator.main(os.path.join(samplesDir, i), sampleDir, k)
            except BaseException as e:
                f = open('errorFile.txt', 'a')
                f.write('###### IMAGE ' + i + ' ######\n')
                f.write('###### Iteration ' + str(j) + ' ######\n')
                f.write('Error creating samples\n')
                f.write(str(e) + '\n\n')
                f.close()
            try:
                SRRestorer.main(sampleDir, k, j)
            except BaseException as e:
                f = open('errorFile.txt', 'a')
                f.write('###### IMAGE ' + i + ' ######\n')
                f.write('###### Iteration ' + str(j) + ' ######\n')
                f.write('Error in restoring\n')
                f.write(str(e) + '\n\n')
                f.close()

print('elapsed Time: ', str((time.time() - startTime)/60), ' mins')
