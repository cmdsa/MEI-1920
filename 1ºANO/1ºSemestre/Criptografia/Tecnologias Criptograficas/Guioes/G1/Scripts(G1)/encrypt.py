from cryptography.fernet import Fernet
#Main - input do nome do ficheiro e corre funçao
def main():
    fileName = input("Insere o nome do ficheiro a ser incriptado com o respetivo formato(file.txt): ")
    #acrestar exceçao caso não seja encontrado o ficheiro
    EncryptaFicheiro(fileName)
#EncryptaFicheiro
def EncryptaFicheiro(fileName):
    
        input_file = fileName
        output_file = 'test.encrypted'
        key = Fernet.generate_key()
        text_file = open("key.txt", "w+")
        text_file.write(key.decode('utf-8'))
        text_file.close()
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