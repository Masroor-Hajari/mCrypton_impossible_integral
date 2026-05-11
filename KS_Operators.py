import numpy as np
import Basic as Bsc
from RF_Operators import SBOX

"""
Instruction:
- KS_Operators.py — key-schedule helpers for the mCrypton-64 block cipher.
- All inputs and outputs use numpy types:
    - Blocks: numpy with shape (4, 4) and dtype=np.uint8.
    - Single nibble values: numpy scalar or 0-dim numpy array with dtype=np.uint8 (e.g. np.uint8(5) or np.array(5, dtype=np.uint8)).
    - Round/index parameters: plain Python int.
- Functions check input types and values, printing error messages on invalid input and may return None; callers should validate inputs and/or catch exceptions and not rely on printed output for control flow.
"""

###################################################################################################
####                                     Updating process                                      ####
###################################################################################################
def Updt(MK: np.uint8, r: int) -> np.uint8:
    try:
        m, n = MK.shape
        if type(r) != int or r < 1 or r > 12:
            raise TypeError("The second input must be an integer value between 1 and 12..")
        elif m != 4 or n != 4:
            raise ValueError("The first input must be a 4x4 matrix.")
        else:
            KS = MK.copy()
            Temp = MK.copy()
            for n in range(1, r + 1):
                for i in range(0, 3):
                    for j in range (0, 4):
                        Temp[i][j] = KS[(i + 1)][j]
                for i in range(0, 4):
                    B1 = Bsc.Int2Nib(KS[0][i])
                    B2 = Bsc.Int2Nib(KS[0][(i + 1) % 4])
                    k = Bsc.Nib2Int(np.array([B1[3], B2[0], B2[1], B2[2]]))
                    Temp[3][i] = k
                KS = Temp.copy()
            return KS.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####                                    Extracting process                                     ####
###################################################################################################
def Ext(KS: np.uint8, r: int) -> np.uint8:
    try:
        m, n = KS.shape
        if type(r) != int or r < 0 or r > 12:
            raise TypeError("The second input must be an integer between 0 and 12.")
        elif m != 4 or n != 4:
            raise ValueError("The first input must be a 4x4 matrix of nibbles.")
        else:
            RC = np.array([1, 2, 4, 8, 3, 6, 12, 11, 5, 10, 7, 14, 15], dtype = np.uint8)
            RK = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range (0, 4):
                    RK[i][j] = KS[(i + 1) % 4][j]
                RK[i][i] = Bsc.NibXor(RK[i][i], SBOX(KS[0][i], 0))
                RK[i][i] = Bsc.NibXor(RK[i][i], RC[r])
            return RK.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)



