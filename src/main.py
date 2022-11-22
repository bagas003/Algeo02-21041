import cv2, os, numpy, time
import eigen

# mengambil dataset dari foldername dan mengembalikan matriks berisi vektor-vektor gambar
def getDataset(foldername):
    data = []
    for imgname in os.listdir(foldername):
        img = cv2.imread(os.path.join(foldername, imgname), cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (256, 256))
        data += [numpy.array(img.T).flatten()]
    return data

# mengembalikan matriks C' (kovarian') dari dataset yang sudah dikurangkan oleh rata-rata
def getCovarian(subtracted):
    return numpy.divide(numpy.dot(subtracted,numpy.transpose(subtracted)), len(subtracted))

# menampilkan gambar arr dalam file
def writeImage(arr, name):
    arr = numpy.reshape(arr, (256,256))
    cv2.imwrite(name, arr.T)

# mengembalikan eigenfaces dari subtracted dataset dan evector v
def getEigenfaces(subtracted, v):
    ui = []
    row = len(v)
    for i in range(row):
        ui += [numpy.dot(numpy.transpose(subtracted), v[:,i])]
    return numpy.matrix(ui)

# mengembalikan vektor omega dari eigenfaces dan vektor subtracted
def getOmega(eigenFaces, subtractedArr):
    omega = []
    for eface in eigenFaces:
        omega += [numpy.dot(eface, subtractedArr)]
    return numpy.array(omega).flatten()

# mengembalikan matriks vektor omega dari eigenfaces dan matriks subtracted vektor
def getOmegaSet(eigenfaces, subtracted):
    omegas = []
    for sub in subtracted:
        omegas += [getOmega(eigenfaces, sub)]
    return numpy.matrix(omegas)

# mengembalikan nilai euclidean distance antara 2 vektor
def getDistance(vector1, vector2):
    ret = 0
    vector = numpy.array(vector1 - vector2).flatten()
    for i in vector:
        ret += i*i
    return int(numpy.sqrt(ret))

# mengembalikan euclidean distance terpendek dan index closest result dari
# matriks omega dataset dan omega testing face baru
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

# mengembalikan nama file di foldername sesuai index
def getFileName(foldername, index):
    return os.listdir(foldername)[index]

# mengembalikan threshold dari omega dataset
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

# pemanggilan program utama
def runprogram(foldername, filename):
    start = time.time()
    '''
    ----DATASET FOLDER-----           ---MATRIKS VEKTOR DATASET (D)---
     img 1   img 2   img 3
    [A A A] [B B B] [C C C]             [ [A A A A A A A A A],
    [A A A] [B B B] [C C C]     ---->     [B B B B B B B B B],
    [A A A] [C C C] [C C C]               [C C C C C C C C C] ]
    '''
    dataset = getDataset(foldername) 
    mean = numpy.mean(dataset, axis=0) # mean =  [x x x x x x x x]
    '''
    MATRIKS SUBTRACTED DATASET (A)
              A = D - mean
    [ [A1 A1 A1 A1 A1 A1 A1 A1 A1],
      [B1 B1 B1 B1 B1 B1 B1 B1 B1],
      [C1 C1 C1 C1 C1 C1 C1 C1 C1] ]
    '''  
    subtracted = dataset - mean
      
    '''
    Covarian' (C')
    Covarian = A x A.Transpose ; Covarian' = A.Transpose x A
    '''
    covarian = getCovarian(subtracted)
    '''
    C' x v(i) = lambda(i) x v(i)
    dengan: lambda = eigenvalues
                 v = eigenvector
    '''
    evectors = eigen.getEVEV(covarian)
    
    '''
    eigenfaces (u)
    u(i) = A x v(i)
    '''
    efaces = getEigenfaces(subtracted, evectors) 
    '''
    omega(i) = sigma( u(k) x A(i) )
    '''
    omegaset = getOmegaSet(efaces, subtracted) 

    # membaca dan memproses testface baru menjadi vektor
    testface = cv2.imread(filename, cv2.IMREAD_GRAYSCALE) 
    testface = cv2.resize(testface, (256, 256)) 
    testface = numpy.array(testface.T).flatten()

    # mendapatkan ANew
    subtracted_test = testface - mean

    # mendapatkan omegaNew
    omega = getOmega(efaces, subtracted_test)

    '''
    euclidean distance (ed)
    ed = sqrt( sigma(i=1,n)((y(i) - x(i))^2) )
    '''
    # mendapatkan euclidean distance dan indeks closest result
    ed, index = getEuclideanAndIndex(omegaset, omega)

    # mendapatkan file closestresult
    closestresult = getFileName(foldername, index) 
    
    '''
    threshold (t)
    t = max( ed(omega(j) - omega(k)) ) ; j,k = 1,2,3,...M
    '''
    # mendapatkan threshold dan similarity
    threshold = getThreshold(omegaset)
    similarity = (threshold - ed) * 100 / threshold
    
    timetaken = time.time() - start

    return closestresult, timetaken, similarity

