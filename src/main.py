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
    ui = [numpy.dot(numpy.transpose(dataset), v[0])]
    for i in range(1,len(v)):
        ui += [numpy.dot(numpy.transpose(dataset), v[i])]
    return numpy.matrix(ui)


dataset = getDataset(r"..\test\dataset")
mean = getMean(dataset)
subtracted = getDifference(dataset, mean)
covarian = getCovarian(subtracted)
evalues, evector = numpy.linalg.eigh(covarian)
efaces = getEigenfaces(subtracted, evector)


for i in range(len(efaces)):
    writeImage(efaces[i], fr"../test/eigenfaces/{i}.jpg")



"""print(evalue)
print(evector)
print('--'*25)
print('--'*25)
eigenfaces = getEigenfaces(evector)
print(eigenfaces[8])
print(len(covarian))
print(len(covarian[0]))"""


"""dataset = [
    [ 1,-2, 1,-3],
    [ 1, 3,-1, 2],
    [ 2, 1,-2, 3],
    [ 1, 2, 2, 1]
]
mean = getMean(dataset)
print(mean)
subtracted = getDifference(dataset, mean)
print(subtracted)
covarian = getCovarian(subtracted)
print(covarian)
evalue, evector = numpy.linalg.eigh(covarian)
print(evalue)
print(evector)
print(mean)
reconstruct0 = reconstruct(subtracted[0], evector, mean)
print(reconstruct0)
print('--'*25)
eigenfaces = getEigenfaces(evector)
print(eigenfaces)"""


"""img = cv2.imread("tes1.jpg", cv2.IMREAD_GRAYSCALE)
print(img)
img1 = numpy.array(img).flatten()
print(img1)
img2 = numpy.array(img.T).flatten()
print(img2)

cv2.imwrite("tes99.jpg", numpy.reshape(img1, (256,256)))
cv2.imwrite("tes98.jpg", numpy.reshape(img2, (256,256)))"""




