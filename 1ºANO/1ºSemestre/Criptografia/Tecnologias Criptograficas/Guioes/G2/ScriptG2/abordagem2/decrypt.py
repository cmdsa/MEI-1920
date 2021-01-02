import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from getpass import getpass

input_file = input(" insere a diretoria de um ficheiro existente (test.encrypted)")
output_file = 'decrypt.txt'

with open(input_file, 'rb') as f:
    data = f.read()


userPassword = getpass() #pede a pass ao usuario
password = userPassword.encode() 
file = open('salt.keystore', 'rb')
salt = file.read() 
file.close()
kdf = Scrypt(
      salt=salt,
      length=32,
      n=2**15,
      r=8,
      p=1,
      backend=default_backend()
 )
key = base64.urlsafe_b64encode(kdf.derive(password))
fernet = Fernet(key)
encrypted = fernet.decrypt(data)

with open(output_file, 'wb') as f:
    f.write(encrypted)
