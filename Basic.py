import numpy as np

"""
Instruction:
- This module provides utilities for 4-bit nibbles and hexadecimal operations.

- Pass values using the types annotated on each function (e.g. np.uint8 for nibbles/hex values,
  Python int for RandInt bounds). Convert/validate inputs before calling.

- Callers should catch exceptions raised by these functions; do not rely on printed error messages
  for control flow.
"""

###################################################################################################
####             Convert a 4-bit binary vector to the corresponding decimal number             ####
###################################################################################################
def Nib2Int(B: np.uint8) -> np.uint8:
    try:
        if B.dtype != np.uint8:
            raise TypeError(f"Input must be a 4-bit binary vector.")
        elif (B.shape != (4, )) or (np.min(B) < 0 or np.max(B) > 1):
            raise ValueError(f"Input must be a 4-bit binary vector.")
        else:
            y = 8 * B[0] + 4 * B[1] + 2 * B[2] + B[3]
            return y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)


###################################################################################################
####                   Convert an integer to the corresponding 4-bit nibble                    ####
###################################################################################################
def Int2Nib(n: np.uint8) -> np.uint8:
    try:
        if n.dtype != np.uint8:
            raise TypeError(f"Input must be an integer value.")
        elif n < 0 or n > 15:
            raise ValueError(f"Input must be an integer value between 0 and 15.")
        else:
            B = np.array([], dtype = np.uint8)
            t = n
            B = np.append(B, (t // 8))
            t = t - B[0] * 8
            B = np.append(B, (t // 4))
            t = t - B[1] * 4
            B = np.append(B, (t // 2))
            t = t - B[2] * 2
            B = np.append(B, t)
            return B.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####                  The integer represtentation of a hexadecimal character                   ####
###################################################################################################
def Hex2Int(x: str) -> np.uint8:
    try:
        if type(x) != str:
            raise TypeError(f"Input must be a hexadecimal string.")
        elif len(x) != 1 or x not in "0123456789abcdefABCDEF":
            raise ValueError(f"Input must be a hexadecimal string of length 1.")
        else:
            y = int(x, 16)
            y = np.array([y], dtype = np.uint8)
            return y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)
    
###################################################################################################
####                        The hexadecimal represtation of an integer                         ####
###################################################################################################
def Int2Hex(x: np.uint8) -> str:
    try:
        if x.dtype != np.uint8:
            raise TypeError(f"Input must be an integer number.")
        elif x < 0 or x > 15:
            raise ValueError(f"Input must be an integer between 0 and 15.")
        else:
            if x < 10:
                y = chr(x + 48)
            else:
                y = chr(x + 87)
            return y

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####            The integer representation of the bitwise AND result of two nibbles            ####
###################################################################################################
def NibAnd(x: np.uint8, y: np.uint8) -> np.uint8:
    X = Int2Nib(x)
    Y = Int2Nib(y)
    Z = X & Y
    z = Nib2Int(Z)
    return z.astype(np.uint8)

###################################################################################################
####            The integer representation of the bitwise XOR result of two nibbles            ####
###################################################################################################
def NibXor(x: np.uint8, y: np.uint8) -> np.uint8:
    X = Int2Nib(x)
    Y = Int2Nib(y)
    Z = X ^ Y
    z = Nib2Int(Z)
    return z.astype(np.uint8)

###################################################################################################
####                                  Random integer genrator                                  ####
###################################################################################################
def RandInt(a: int, b: int, inclusive: bool) -> np.uint8:
    try:
        if type(a) != int or type(b) != int or type(inclusive) != bool:
            raise TypeError("Bounds must be integers. The thitd parameter must be a boolean value.")
        if a > b:
            raise ValueError("The lower bound must be less than or equal to the upper bound.")
        else:
            rng = np.random.default_rng()
        if inclusive:
            y = rng.integers(a, b + 1)
            return y.astype(np.uint8)
        else:
            try:
                if a == b and inclusive == False:
                    raise ValueError("The lower and upper bounds must be different when the range is exclusive.")
                else:
                    y = rng.integers(a, b)
                    return y.astype(np.uint8)

            except ValueError as e3:
                print("Error: Invalid input.", e3)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)




