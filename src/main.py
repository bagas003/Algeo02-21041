import cv2, os, numpy, time

def getDataset(foldername):
    data = []
    for imgname in os.listdir(foldername):
        img = cv2.imread(os.path.join(foldername, imgname), cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (256, 256))
        data += [numpy.array(img.T).flatten()]
    return data

def getCovarian(dataset):
    return numpy.divide(numpy.dot(dataset,numpy.transpose(dataset)), len(dataset))

def writeImage(arr, name):
    arr = numpy.reshape(arr, (256,256))
    cv2.imwrite(name, arr.T)

def getEigenfaces(dataset, v):
    ui = []
    row = len(v)
    for i in range(row):
        ui += [numpy.dot(numpy.transpose(dataset), v[:,i])]
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
        euclidean += [numpy.linalg.norm(omegaNew - omega)]
    return euclidean

def getEuclideanAndIndex(omegaSet, omegaNew):
    ed = numpy.linalg.norm(omegaNew - omegaSet[0])
    idx = 0
    row = len(omegaSet)
    for i in range(1,row):
        edtemp = numpy.linalg.norm(omegaNew - omegaSet[i])
        if edtemp < ed:
            ed = edtemp
            idx = i
    return ed, idx

def getFileName(foldername, index):
    return os.listdir(foldername)[index]

# def getThreshold(omegaset):
#     l = len(omegaset)
#     threshold = 0
#     for i in range(l):
#         for j in range(i, l):
#             threshold = max(threshold, numpy.linalg.norm(omegaset[i] - omegaset[j]))
#     return threshold / 2

datasetfolder = input('enter dataset folder: (ex. newdataset)\n>> ')
testfacefile = input('enter testface file: (ex. test.jpg)\n>> ')

start = time.time()

datasetfolder = r'..\test\\' + datasetfolder
dataset = getDataset(datasetfolder)
mean = numpy.mean(dataset, axis=0)
subtracted = dataset - mean

covarian = getCovarian(subtracted)
evalues, evectors = numpy.linalg.eigh(covarian)

efaces = getEigenfaces(subtracted, evectors)
omegaset = getOmegaSet(efaces, subtracted)

testface = cv2.imread(r'..\test\testface_folder\\' + testfacefile, cv2.IMREAD_GRAYSCALE)
testface = cv2.resize(testface, (256, 256))
testface = numpy.array(testface.T).flatten()
subtracted_test = testface - mean

omega = getOmega(efaces, subtracted_test)

ed, index = getEuclideanAndIndex(omegaset, omega)
# treshold = getThreshold(omegaset)

closestresult = getFileName(datasetfolder, index)
print('\nclosest result for',testfacefile, ':',closestresult)

print('time taken: ', time.time() - start)

writeImage(dataset[index], '../test/result.jpg')
writeImage(testface, '../test/testface.jpg')