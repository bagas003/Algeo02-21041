import cv2, os, numpy

def getMean(dataset):
    cnt = 0
    sum = [[0 for i in range(256)] for j in range(256)]
    for imgname in os.listdir(dataset):
        img = cv2.imread(os.path.join(dataset, imgname), cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (256, 256))
        sum = numpy.add(sum, img)
        cnt += 1
    sum = numpy.divide(sum, cnt)
    return sum

meanMatrix = getMean(r"..\test\dataset")
print(meanMatrix)
