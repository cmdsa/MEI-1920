import os
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Hash import SHA256

with open("input.txt", 'rb') as f:
    message = f.read()
key = os.urandom(32)
key1 = os.urandom(32)
nonce = os.urandom(16)

algorithm = algorithms.ChaCha20(key1, nonce)
cipher = Cipher(algorithm, mode=None, backend=default_backend())
encryptor = cipher.encryptor()
ct = encryptor.update(message)
with open("test.encrypted", 'wb') as f:
    f.write(ct)
h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
h.update(ct)
m = h.finalize()