import cv2, os, numpy

def getDataset(foldername):
    for imgname in os.listdir(foldername):
        img = cv2.imread(os.path.join(foldername, imgname), cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (256, 256))
        img = numpy.array(img.T).flatten()
        try:
            data = numpy.append(data, [img], axis=0)
        except:
            data = [img]
    return data

def getMean(dataset):
    sum = [0 for j in range(len(dataset[0]))]
    for data in dataset:
        sum = numpy.add(sum, data)
    return numpy.divide(sum, len(dataset))

def getDifference(dataset, mean):
    for data in dataset:
        x = numpy.subtract(data, mean)
        try:
            newdata += [x]
        except:
            newdata = [x]
    return newdata

def getCovarian(dataset):
    datatranspose = numpy.transpose(dataset)
    data = numpy.dot(dataset,datatranspose)
    return numpy.divide(data, len(dataset))


def writeImage(arr, name):
    arr = numpy.reshape(arr, (256,256))
    cv2.imwrite(name, arr.T)

def getEigenfaces(dataset, v):
    ui = [numpy.dot(numpy.transpose(dataset), v[:,0])]
    for i in range(1,len(v)):
        ui += [numpy.absolute(numpy.dot(numpy.transpose(dataset), v[:,i]))]
    return numpy.matrix(ui)

def getOmega(eigenFaces, subtractedArr):
    omega = []
    for eface in eigenFaces:
        omega += [numpy.dot(eface, subtractedArr)]
    return numpy.array(omega).flatten()

def getOmegaSet(eigenfaces, subtracted):
    omegas = []
    for sub in subtracted:
        omegas += [getOmega(eigenfaces, sub)]
    return numpy.matrix(omegas)

def getEuclidean(omegaSet, omegaNew):
    euclidean = []
    for omega in omegaSet:
        euclidean.append(numpy.linalg.norm(omegaNew - omega))
    return euclidean

def getFileName(foldername, index):
    for filename in os.listdir(foldername):
        if index == 0:
            return filename
        index -= 1

datasetfolder = input('enter dataset folder: (ex. newdataset)\n>> ')
testfacefile = input('enter testface file: (ex. test.jpg)\n>> ')

print('\nextracting dataset...', end=' ')
datasetfolder = r'..\test\\' + datasetfolder
dataset = getDataset(datasetfolder)
print('done!')
print('getting average face & subtracting faces...', end=' ')
mean = getMean(dataset)
subtracted = getDifference(dataset, mean)
print('done!')
print('processing covarian matrix...', end=' ')
covarian = getCovarian(subtracted)
evalues, evectors = numpy.linalg.eigh(covarian)
print('done!')
print('getting eigenfaces and omegas...', end=' ')
efaces = getEigenfaces(subtracted, evectors)
omegaset = getOmegaSet(efaces, subtracted)
print('done!')

print('\nprocessing testface...', end=' ')
testface = cv2.imread(r'..\test\\' + testfacefile, cv2.IMREAD_GRAYSCALE)
testface = cv2.resize(testface, (256, 256))
testface = numpy.array(testface.T).flatten()
subtracted_test = numpy.subtract(testface, mean)
print('done!')

print('getting new omega...', end=' ')
omega = getOmega(efaces, subtracted_test)
print('done!')
print('getting euclidean distances...', end=' ')
euclidean = getEuclidean(omegaset, omega)
print('done!')

closestresult = getFileName(datasetfolder, numpy.argmin(euclidean))
for i in range(len(euclidean)):
    print(i, euclidean[i])
print('minimum distance index: ',numpy.argmin(euclidean))
print('closest result for',testfacefile, ':',closestresult)

