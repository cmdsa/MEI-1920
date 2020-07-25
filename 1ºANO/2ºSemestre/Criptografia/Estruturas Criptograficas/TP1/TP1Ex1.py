import os, io
from BiConn import BiConn
from Auxs import hashs, mac, kdf, default_algorithm
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import *
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac, cmac, serialization
from cryptography.hazmat.primitives.asymmetric import dh, dsa
import lorem

#gerar parametros DH
dh_parameters = dh.generate_parameters(generator=2, key_size=1024,backend=default_backend())

#gerar parametros DSA
dsa_parameters = dsa.generate_parameters(key_size=1024, backend=default_backend())


def KeyAgree(conn):
    #gera chave privada (DH)
    dhpk = dh_parameters.generate_private_key()

    #gera chave publica (DH, formato PEM)
    dhpubkey = dhpk.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)

    #chave dsa privada
    dsapk = dsa_parameters.generate_private_key()

    #pem publico dsa
    dsapub_pem = dsapk.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    
    #assina a mensagem (assina-se com a chave privada)
    sig = dsapk.sign(dhpubkey, default_algorithm())

    #envia a chave publica dsa, a chave publica dh e a assinatura
    conn.send((dsapub_pem,dhpubkey,sig))

    ##recebe a chave publica dsa, a chave publica dh e a assinatura
    dsa_pub_recv,dh_pub_recv,sig_recv = conn.recv()

    peer_dsa_pub_recv = serialization.load_pem_public_key(
            dsa_pub_recv,
            backend=default_backend())
    #valida a assinatura
    try:
        peer_dsa_pub_recv.verify(sig_recv,dh_pub_recv,default_algorithm())
        print('DSA Signature ok')
        # shared_key calculation
        peer_dh_pub_key = serialization.load_pem_public_key(
                dh_pub_recv,
                backend=default_backend())
        shared_key = dhpk.exchange(peer_dh_pub_key)
        
        # confirmation
        my_tag = hashs(bytes(shared_key))
        conn.send(my_tag)
        peer_tag = conn.recv()
        if my_tag == peer_tag:
            print('DH OK')
            return my_tag
        else:
            print('DH FAIL')
    except InvalidSignature:
        print('DSA Signature fail')

    

    conn.close()       # fechar a conecção

def Emitter(conn):
    
    key = KeyAgree(conn)
    iv  = os.urandom(16)

  
    text = lorem.text().encode('utf-8',"ignore")
    encryptor = Cipher(algorithms.AES(key),modes.CFB(iv),backend=default_backend()).encryptor()
  
    conn.send(iv)

    encrypttext = encryptor.update(text) + encryptor.finalize()
    this_mac = mac(key,encrypttext)

    conn.send((this_mac,encrypttext))

    conn.close()

def Reciever(conn):
    
    key = KeyAgree(conn)

    iv = conn.recv()
    decryptor = Cipher(algorithms.AES(key),modes.CFB(iv),backend=default_backend()).decryptor()
    
    peer_mac, peer_msg = conn.recv()
    try:
        mac(key,peer_msg,peer_mac)
        try:
            decrypttext = decryptor.update(peer_msg) + decryptor.finalize()
            print(decrypttext.decode('utf-8',"ignore"))
        except InvalidSignature:
            print("autenticação do ciphertext falhou")
    except InvalidSignature:
        print('Hmac didnt match')

    
    
    conn.close()
    

BiConn(Emitter,Reciever,timeout=30).auto()