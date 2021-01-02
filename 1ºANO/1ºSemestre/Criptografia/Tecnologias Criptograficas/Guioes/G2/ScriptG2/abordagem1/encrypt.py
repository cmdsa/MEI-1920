import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from getpass import getpass

#Main - input do nome do ficheiro e corre funçao
def main():
    fileName = input("Insere o nome do ficheiro a ser incriptado com o respetivo formato(file.txt): ")
    #acrestar exceçao caso não seja encontrado o ficheiro
    EncryptaFicheiro(fileName)

#EncryptaFicheiro
def EncryptaFicheiro(fileName):
        input_file = fileName
        output_file = 'test.encrypted'

        userPassword = getpass() 
        password = userPassword.encode() 
        salt = os.urandom(16)
        file = open('salt.salt', 'wb')
        file.write(salt)
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
    
        try:
                with open(input_file, 'rb') as f:
                    data = f.read()
            
                fernet = Fernet(key)
                encrypted = fernet.encrypt(data)

                with open(output_file, 'wb') as f:
                    f.write(encrypted)
        except IOError:
            print("Ficheiro não encontrado")
            
if __name__ == "__main__":
    main()