import numpy as np
import RF_Operators as RF_Opr
import KS_Operators as KS_Opr

"""
Instruction:
- Encryption.py — implements the mCrypton-64 block encryption routine Enc(P, MK, r).

- Inputs:
  - P: numpy.ndarray, shape (4, 4), dtype=np.uint8 — plaintext nibble matrix (values 0..15).
  - MK: numpy.ndarray, shape (4, 4), dtype=np.uint8 — master key nibble matrix (values 0..15).
  - r: int — number of rounds (1..12).

- Output:
  - Returns numpy.ndarray, shape (4, 4), dtype=np.uint8 — ciphertext nibble matrix.

- Conventions and expectations:
  - All nibble values must be numpy uint8 (use np.uint8(...) or np.array(..., dtype=np.uint8)).
  - Many helper functions (in Basic.py, RF_Operators.py, KS_Operators.py) check .dtype and .shape;
    passing plain Python ints or nested lists will raise TypeError from those checks.
  - Convert inputs before calling Enc to avoid silent dtype/shape issues:
      P = np.array(P, dtype=np.uint8).reshape(4,4)
      MK = np.array(MK, dtype=np.uint8).reshape(4,4)

- Error handling:
  - Enc validates inputs and prints error messages on invalid input; it may return None after printing.
  - For robust code, validate and convert inputs in callers or modify helpers to raise exceptions instead of printing.

- Example:
    P = np.array([[4,11,7,2],
                  [0,5,6,7],
                  [1,15,12,7],
                  [13,0,12,10]], dtype=np.uint8)
    MK = np.array([[6,10,10,10],
                   [14,0,12,2],
                   [12,13,11,11],
                   [15,14,6,0]], dtype=np.uint8)
    C = Enc(P, MK, 12)  # returns np.ndarray (4,4) dtype=np.uint8

- Notes:
  - If you need reproducible keys or deterministic behavior, construct KS externally and pass prepared numpy arrays.
  - Convert returned numpy scalars to native Python ints with int(...) when needed.
"""

###################################################################################################
####                             mCrypton-64 encryption algorithm                              ####
###################################################################################################
def Enc(P: np.uint8, MK: np.uint8, r: int) -> np.uint8:
    try:
        m, n = MK.shape
        p, q = P.shape
        if type(r) != int or r < 1 or r > 12:
            raise TypeError("The third input must be an integer between 1 and 12.")
        elif m != 4 or n != 4 or p != 4 or q != 4:
            raise ValueError("The first and second inputs must be a 4x4 matrices of nibbles.")
        else:
            RK = KS_Opr.Ext(MK, 0)
            X = RF_Opr.Sigma(P, RK)
            for i in range(1, r):
                KS = KS_Opr.Updt(MK, i)
                RK = KS_Opr.Ext(KS, i)
                X = RF_Opr.RF(X, RK)
            KS = KS_Opr.Updt(MK, r)
            RK = KS_Opr.Ext(KS, r)
            C = RF_Opr.LastRF(X, RK)
            return C.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

