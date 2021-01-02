
from cryptography.fernet import Fernet

input_file = input(" insere a diretoria de um ficheiro existente (decrypt.txt)")
output_file = 'decrypt.txt'

with open(input_file, 'rb') as f:
    data = f.read()

text_file = open("key.txt", "r")
key = text_file.read()
fernet = Fernet(key)
encrypted = fernet.decrypt(data)

with open(output_file, 'wb') as f:
    f.write(encrypted)
