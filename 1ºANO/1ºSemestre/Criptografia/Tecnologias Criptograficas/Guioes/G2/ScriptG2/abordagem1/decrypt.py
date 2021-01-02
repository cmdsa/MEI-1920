import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from getpass import getpass

input_file = input(" insere a diretoria de um ficheiro existente (test.encrypted)")
output_file = 'decrypt.txt'

with open(input_file, 'rb') as f:
    data = f.read()


userPassword = getpass() #pede a pass ao usuario
password = userPassword.encode() 
file = open('salt.salt', 'rb')
salt = file.read() 
file.close()
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
print(key)
fernet = Fernet(key)
encrypted = fernet.decrypt(data)

with open(output_file, 'wb') as f:
    f.write(encrypted)
