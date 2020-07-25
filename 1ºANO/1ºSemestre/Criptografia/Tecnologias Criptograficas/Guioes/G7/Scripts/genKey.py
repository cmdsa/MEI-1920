from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh, rsa
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import (load_pem_public_key, 
                                                         Encoding,PublicFormat, PrivateFormat)


def key_server():
    server_private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
                )
    enc_server_private_key = server_private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8,encryption_algorithm=serialization.BestAvailableEncryption(b'1234'))
    
    server_public_key = server_private_key.public_key()
    enc_server_public_key = server_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

   
    with open('server_private_key.bin', 'wb') as private, open('server_public_key,bin', 'wb') as public:
        private.write(enc_server_private_key)
        public.write(enc_server_public_key)


def key_client():
    client_private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
                )
    enc_client_private_key = client_private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8,serialization.NoEncryption())

    client_public_key = client_private_key.public_key()   
    enc_client_public_key = client_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)       

    with open('client_private_key.bin', 'wb') as private, open('client_public_key,bin', 'wb') as public:
        private.write(enc_client_private_key)
        public.write(enc_client_public_key)      

key_client()
key_server()