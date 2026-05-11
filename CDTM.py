import numpy as np
import Basic as Bsc
import Encryption as Enc

"""
Instruction:
- CDTM.py — prepares ciphertext collections from plaintexts produced by DDTM, writes/reads them to disk,
  and provides a simple verification helper.
"""

###################################################################################################
####                       Writing the prepared blocks into a text file                        ####
###################################################################################################
def WriteDoc(ctxList: list, Address: str) -> None:
    try:
        if type(ctxList) != list:
            raise TypeError("The first input must be a list of plaintexts.")
        else:
            flag = True
            Address = Address + "\\Ciphertexts.txt"
            Len = len(ctxList)
            with open(Address, "w") as f:
                for i in range(0, Len):
                    f.write("0x")
                    for j in range(0, 4):
                        for l in range(0, 4):
                            f.write(Bsc.Int2Hex(ctxList[i][j][l]))
                    f.write("\n")
                    y = round((i + 1) / Len * 100, 2)
                    if abs(y - round(y)) < 0.05 and flag == True:
                        print(f"CDTM: {round(y)}% of the writing has been completed.")
                        flag = False
                    elif abs(y - round(y)) >= 0.05:
                        flag = True
                    else:
                        continue
            f.close()

    except TypeError as e:
        print("Error: Invalid input.", e)

###################################################################################################
####                         Reading the plaintexts preapared by DDTM                          ####
###################################################################################################
def ReadDoc(Address: str) -> list:
    try:
        if type(Address) != str:
            raise TypeError("The first input must be the address of the target file.")
        else:
            ptxList = []
            Address = Address + "\\Plaintexts.txt"
            with open(Address, "r") as f:
                Data = f.read()
                f.close()
            Len = len(Data)
            ctr = 0
            ctr2 = 0
            flag = True
            while(ctr < Len):
                if Data[ctr] == "0" and Data[ctr + 1] == "x":
                    ctr += 2
                elif Data[ctr - 2] == "0" and Data[ctr - 1] == "x":
                    ctr3 = 0
                    X = np.array([
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                        ], dtype = np.uint8)
                    for i in range(0, 4):
                        for j in range (0, 4):
                            X[i][j] = Bsc.Hex2Int(Data[ctr + ctr3])
                            ctr3 += 1
                    ctr += 16
                    ptxList.append(X.copy())
                elif Data[ctr] == "\n":
                    ctr += 1
                    ctr2 += 1
                else:
                    ctr += 1
                y = round(100 * ctr / Len, 2)
                if abs(y - round(y)) < 0.05 and flag == True:
                    print(f"CDTM: {round(y)}% of the reading has been completed.")
                    flag = False
                elif abs(y - round(y)) >= 0.05:
                    flag = True
                else:
                    continue
            return ptxList

    except TypeError as e:
        print("Error: Invalid input.", e)

###################################################################################################
####                          Preparing and wrinting the random Data                           ####
###################################################################################################
def CDTM_Write(Address: str) -> bool:
    ptxList = ReadDoc(Address)
    N = len(ptxList)
    ctxList = []
    MK = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ], dtype = np.uint8)
    b = Bsc.RandInt(0, 65535, True)
    b = b % 2
    if b == 0:
        for i in range (0, 4):
            for j in range(0, 4):
                MK[i][j] = Bsc.RandInt(0, 15, True)
    flag = True
    for i in range(0, N):
        if b == 0:
            X = Enc.Enc(ptxList[i], MK, 5)
        else:
            X = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for j in range(0, 4):
                for l in range(0, 4):
                    X[j][l] = Bsc.RandInt(0, 15, True)
        ctxList.append(X.copy())
        y = round(100 * i / N, 2)
        if abs(y - round(y, 1)) < 0.005 and flag == True:
            print(f"CDTM: {round(y, 1)}% of the generating data has been completed.")
            flag = False
        elif abs(y - round(y, 1)) >= 0.005:
            flag = True
        else:
            continue
    WriteDoc(ctxList, Address)
    b = bool(b)
    return b

###################################################################################################
####                                 Verifying DDTM's response                                 ####
###################################################################################################
def CDTM_Verify(b, bHat) -> None:
    try:
        if type(b) != bool or type(bHat) != bool:
            raise TypeError("Inputs must be boolean values.")
        else:
            if b == bHat:
                print("The decision is correct.")
            else:
                print("The decision is wrong.")

    except TypeError as e:
        print("Error: Invalid input.", e)
