# -*- coding: utf-8 -*-

from hashlib import sha256
from ctypes import c_ulonglong


ALPHABET = u"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_encode(num, alphabet=ALPHABET):
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return u''.join(arr)

def base62_decode(string, alphabet=ALPHABET):
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

def make_item_key(pk):
    # make a one-to-one hash looking a pseudo-random number
    # by multiplying by a large odd number and xor with a different one
    A = 14629228519526648887
    B = 3966156462935221158
    x = c_ulonglong((pk * A) ^ B).value
    return base62_encode(x)

def make_hash(prefix, pk):
    input_str = u"{0}:{1}".format(prefix, pk)
    x = int(sha256(input_str).hexdigest(), 16)
    return base62_encode(x)

def make_wallet_key(pk):
    return make_hash("XC7xX1k_T6R*cBDfTsQc')U=-[2hty_2:wallet", pk)

def make_secret_key(pk):
    return make_hash("XC7xX1k_T6R*cBDfTsQc')U=-[2hty_2:secret", pk)

def main():
    print "validate uniqueness..."
    validation = set()
    for i in xrange(2**20):
        x = make_item_key(i)
        if not x in validation:
            validation.add(x)
        else:
            print "ERROR!"
            return 1
    print "print keys..."
    print make_item_key(3)
    print make_wallet_key(3)
    print make_secret_key(3)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
