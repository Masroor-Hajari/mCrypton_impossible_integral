import numpy as np
import Basic as Bsc

"""
Instruction:
- This module implements round-function operators for 4x4 nibble blocks used by the mCrypton-64 blockcipher.
- Use numpy types: pass blocks as numpy.ndarray with shape (4,4) and dtype=np.uint8; pass single nibbles as np.uint8 (e.g. np.uint8(5) or np.array(5, dtype=np.uint8)).
- Many functions check .dtype and .shape; plain Python ints/lists will cause TypeError. Convert inputs before calling: np.uint8(value) or np.array(value, dtype=np.uint8).
- Functions print error messages on invalid input and may return None; callers should validate inputs and/or catch exceptions and not rely on printed output for control flow.
- Returned values are numpy arrays or numpy scalars (dtype=np.uint8). Convert to Python int with int(...) when a native int is required.
"""

###################################################################################################
####                         4 SBOXes which are used in Gamma operator                         ####
###################################################################################################
def SBOX(x: np.uint8, ind: int) -> np.uint8:
    try:
        if x.dtype != np.uint8 or type(ind) != int:
            raise TypeError("Inputs must be integer numbers.")
        elif x < 0 or x > 15 or ind < 0 or ind > 3:
            raise ValueError("The first input must be an integer between 0 and 15, and the second one must be between 0 and 3.")
        else:
            M = np.array([
                [4, 15, 3, 8, 13, 10, 12, 0, 11, 5, 7, 14, 2, 6, 1, 9], 
                [1, 12, 7, 10, 6, 13, 5, 3, 15, 11, 2, 0, 8, 4, 9, 14], 
                [7, 14, 12, 2, 0, 9, 13, 10, 3, 15, 5, 8, 6, 4, 11, 1], 
                [11, 0, 10, 7, 13, 6, 4, 2, 12, 14, 3, 9, 1, 5, 15, 8]
                ])
            y = M[ind][x]
            return y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####                                      Gamma operator                                       ####
###################################################################################################
def Gamma(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of nibbles.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    y = SBOX(X[i][j], (i + j) % 4)
                    Y[i][j] = y
            return Y.astype(np.uint8)

    except TypeError as e:
        print("Error: Invalid dimentions.", e)

###################################################################################################
####                                     InvGamma operator                                     ####
###################################################################################################
def InvGamma(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of nibbles.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    y = SBOX(X[i][j], (i + j + 2) % 4)
                    Y[i][j] = y
            return Y.astype(np.uint8)

    except TypeError as e:
        print("Error: Invalid dimentions.", e)

###################################################################################################
####                                        Pi operator                                        ####
###################################################################################################
def Pi(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of nibbles.")
        else:
            M = np.array([14, 13, 11, 7], dtype = np.uint8)
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    for l in range(0, 4):
                        t = Bsc.NibAnd(M[(i + j + l) % 4], X[l][j])
                        Y[i][j] = Bsc.NibXor(t, Y[i][j])
            return Y.astype(np.uint8)

    except TypeError as e:
        print("Error: Invalid dimentions.", e)

###################################################################################################
####                                       Tau operator                                        ####
###################################################################################################
def Tau(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of nibbles.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    Y[i][j] = X[j][i]
            return Y.astype(np.uint8)

    except TypeError as e:
        print("Error: Invalid dimentions.", e)

###################################################################################################
####                                       Pi* operator                                        ####
###################################################################################################
def PiStar(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of nibbles.")
        else:
            Y = Tau(X)
            Y = Pi(Y)
            Y = Tau(Y)
            return Y.astype(np.uint8)

    except TypeError as e:
        print("Error: Invalid dimentions.", e)


###################################################################################################
####                                      Sigma operator                                       ####
###################################################################################################
def Sigma(X: np.uint8, K: np.uint8) -> np.uint8:
    m, n = X.shape
    p, q = K.shape
    try:
        if m != 4 or n != 4 or p != 4 or q != 4:
            raise TypeError("Inputs must be 4x4 matrices of nibbles.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    Y[i][j] = Bsc.NibXor(X[i][j], K[i][j])
            return Y.astype(np.uint8)

    except TypeError as e:
        print("Error: Invalid dimentions.", e)

###################################################################################################
####                                      Sigma* operator                                       ####
###################################################################################################
def SigmaSt(X: np.uint8, K: np.uint8) -> np.uint8:
    m, n = X.shape
    p, q = K.shape
    try:
        if m != 4 or n != 4 or p != 4 or q != 4:
            raise TypeError("Inputs must be 4x4 matrices of nibbles.")
        else:
            kt = Tau(K)
            kSt = Pi(kt)
            Y = Sigma(X, kSt)
            return Y.astype(np.uint8)

    except TypeError as e:
        print("Error: Invalid dimentions.", e)

###################################################################################################
####                                      Round function                                       ####
###################################################################################################
def RF(X: np.uint8, K: np.uint8) -> np.uint8:
    m, n = X.shape
    p, q = K.shape
    try:
        if m != 4 or n != 4 or p != 4 or q != 4:
            raise TypeError("Inputs must be 4x4 matrices of nibbles.")
        else:
            Z = Gamma(X)
            W = Pi(Z)
            V = Tau(W)
            Y = Sigma(V, K)
            return Y.astype(np.uint8)

    except TypeError as e:
        print("Error: Invalid dimentions.", e)

###################################################################################################
####                                   Last-Round function                                    #####
###################################################################################################
def LastRF(X: np.uint8, K: np.uint8) -> np.uint8:
    m, n = X.shape
    p, q = K.shape
    try:
        if m != 4 or n != 4 or p != 4 or q != 4:
            raise TypeError("Inputs must be 4x4 matrices of nibbles.")
        else:
            Z = Gamma(X)
            W = SigmaSt(Z, K)
            C = Tau(W)
            return C.astype(np.uint8)

    except TypeError as e:
        print("Error: Invalid dimentions.", e)





