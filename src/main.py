import cv2, os, numpy, time
import eigen

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
        euclidean += [getDistance(omegaNew, omegaNew)]
    return euclidean

def getEuclideanAndIndex(omegaSet, omegaNew):
    ed = getDistance(omegaNew, omegaSet[0])
    idx = 0
    row = len(omegaSet)
    for i in range(1,row):
        edtemp = getDistance(omegaNew, omegaSet[i])
        if edtemp < ed:
            ed = edtemp
            idx = i
    return ed, idx

def getFileName(foldername, index):
    return os.listdir(foldername)[index]

def getThreshold(omegaset):
    l = len(omegaset)
    threshold = 0
    for i in range(l):
        for j in range(i, l):
            threshold = max(threshold, getDistance(omegaset[i], omegaset[j]))
    return threshold / 4

def getDistance(vector1, vector2):
    ret = 0
    vector = numpy.array(vector1 - vector2).flatten()
    for i in vector:
        ret += i*i
    return int(numpy.sqrt(ret))


def runprogram(foldername, filename): #keduanya dirac full 
    start = time.time()

    dataset = getDataset(foldername) 
    mean = numpy.mean(dataset, axis=0) 
    subtracted = dataset - mean 
    
    covarian = getCovarian(subtracted)
    # evalues, evectors = numpy.linalg.eigh(covarian)
    evectors = eigen.getEVEV(covarian)
    
    efaces = getEigenfaces(subtracted, evectors) 
    omegaset = getOmegaSet(efaces, subtracted) 

    testface = cv2.imread(filename, cv2.IMREAD_GRAYSCALE) 
    testface = cv2.resize(testface, (256, 256)) 
    testface = numpy.array(testface.T).flatten()
    subtracted_test = testface - mean

    omega = getOmega(efaces, subtracted_test)
    # euclidean = getEuclidean(omegaset, omega)
    # ed = min(euclidean);
    # threshold = max(euclidean)
    # index = numpy.argmin(euclidean)
    ed, index = getEuclideanAndIndex(omegaset, omega)

    closestresult = getFileName(foldername, index) # nama file hasil similarity

    
    threshold = getThreshold(omegaset)
    similarity = (threshold - ed) * 100 / threshold
    
    timetaken = time.time() - start
    #===== sementara =====#
    # print('\nclosest result for',foldername, ':',closestresult)
    # print('time taken: ', timetaken) 

    return closestresult, timetaken, similarity

'''
#datasetfolder = input('enter dataset folder: (ex. newdataset)\n>> ')
#testfacefile = input('enter testface file: (ex. test.jpg)\n>> ')

# start = time.time() ini nanti dipindahin ke start button

#datasetfolder = r'..\test\\' + datasetfolder diganti sama folderdirec dari cfolder
dataset = getDataset(datasetfolder) # jadi matriks dari semua foto yang ada di dataset
mean = numpy.mean(dataset, axis=0) 
subtracted = dataset - mean 

covarian = getCovarian(subtracted)
evalues, evectors = numpy.linalg.eigh(covarian) # ini punya si farhan

efaces = getEigenfaces(subtracted, evectors) 
omegaset = getOmegaSet(efaces, subtracted) 

testface = cv2.imread(r'..\test\testface_folder\\' + testfacefile, cv2.IMREAD_GRAYSCALE)
testface = cv2.resize(testface, (256, 256))
testface = numpy.array(testface.T).flatten()
subtracted_test = testface - mean

omega = getOmega(efaces, subtracted_test)

ed, index = getEuclideanAndIndex(omegaset, omega)


closestresult = getFileName(datasetfolder, index)
# print('\nclosest result for',testfacefile, ':',closestresult)

# print('time taken: ', time.time() - start) nanti ditaro di ex time 

# writeImage(dataset[index], '../test/result.jpg')
# writeImage(testface, '../test/testface.jpg')'''
