import numpy as np

def getEVEV(covarian):  
    # Power Iteration Method
    n = len(covarian)

    Q = np.random.rand(n, n)
    # QR Decomp menggunakan library numpy
    Q, R = np.linalg.qr(Q)

    for i in range(20):
        QR = np.matmul(covarian,Q)
        Q, R = np.linalg.qr(QR)

    return Q

def getEVEV2(covarian):
    n = len(covarian)

    Q = np.random.rand(n, n)
    # QR Decomp tanpa library
    Q, R = QRDecomp(Q)

    for i in range(20):
        QR = np.matmul(covarian,Q)
        Q, R = QRDecomp(QR)

    return Q

def QRDecomp(mat):
    # Gram-Schmidt
    n = len(mat)
    Q = np.zeros((n,n))
    R = np.zeros((n,n))
    
    for i in range(n):
        # kolom i dari mat
        u = mat[:, i]

        for j in range(i - 1):
            q = Q[:, j]
            R[j, i] = np.matmul(q,u)
            u = u - R[j, i] * q
        
        unorm = norm(u)

        # ei = ui/norm(ui)
        Q[:, i] = u / unorm
        # diagonal
        R[i, i] = unorm
    return Q, R

def norm(u):
    # norm for 1xn matrix
    n = len(u)
    norm = 0
    for i in range(n):
        norm += (u[i])**2
    return (norm)**(1/2)