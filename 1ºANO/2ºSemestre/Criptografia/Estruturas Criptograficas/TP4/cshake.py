from binascii import hexlify, unhexlify
from CompactFIPS202 import SHAKE128, Keccak
import os
def left_encode(x):
    """function bytepad
        
        left_encode(x) encodes the integer x as a byte string in a way that can be unambiguously parsed from the beginning of the string by inserting the length of the byte string before the byte string representation of x. As an example, left_encode(0) will yield 00000001 00000000.
        
        Args:
        x: the input integer
        
        Returns:
        O: binary string
    """
    if (x >= 0) and (x < (1 << 2040)):
        x_bin = '{0:b}'.format(x)
        On = x_bin
        while (len(On) % 8) != 0:
            On = '0' + On
        n = len(On) // 8
        n_bin = '{0:b}'.format(n)
        O0 = n_bin
        while (len(O0) % 8) != 0:
            O0 = '0' + O0
        O = O0 + On
        return O
    else:
        print ('Invalid bit string (left_encode)')

def encode_string(S):
    """function bytepad
        
        The encode_string function is used to encode bit strings in a way that may be parsed unambiguously from the beginning of the string S.
        
        Args:
        S: the input ascii string
        
        Returns:
        U: binary string
    """
    if S != '':
        S = '{0:b}'.format(int(hexlify(S), 16))
        while (len(S) % 8) != 0:
            S = '0' + S
    if (len(S) >= 0) and (len(S) < 2040):
        U = left_encode(len(S)) + S
        return U
    else:
        print ('Invalid bit string (encode_string)')

def bytepad(X, w):
    """function bytepad
        
        The bytepad(X, w) function prepends an encoding of the integer w to an input string X, then pads the result with zeros until it is a byte string whose length in bytes is a multiple of w. In general, bytepad is intended to be used on encoded strings-the byte string bytepad(encode_string(S), w) can be parsed unambiguously from its beginning, whereas bytepad does not provide unambiguous padding for all input strings.
        
        Args:
        X: the input binary string
        w: the rate (in bytes) of the KECCAK sponge function
        
        Returns:
        z: binary string
    """
    if w > 0:
        z = left_encode(w) + X
        while (len(z) % 8) != 0:
            z += '0'
        while ((len(z) / 8) % w) != 0:
            z += '00000000'
        return z
    else:
        print ('Invalid integer (bytepad)')


def cSHAKE128(X, L, N = '', S = ''):
    """Hash function cSHAKE128
        
        Pad the input string to the specified length, add the custom parameter and call the SHAKE128 function in the library.
        
        Args:
        X: the input string
        L: the length of output
        N: a function-name string
        S: the custom parameter
        
        Returns:
        out_int: Integer hash value
    """

    if (N == '') and (S == ''):
        return SHAKE128(X,L)
    else:
        n = '{0:x}'.format(int(bytepad(encode_string(N) + encode_string(S), 168), 2))
        while (len(n) % 8) != 0:
            n = '0' + n
        return Keccak(1344, 256, bytearray(unhexlify(n) + X), 0x04, L)