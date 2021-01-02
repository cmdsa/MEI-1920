from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from Auxs import hashs
from BiConn import BiConn
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, hmac, cmac, serialization
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os
import lorem

def KeyAgree(conn):

	ecdh_private_key = ec.generate_private_key(
			ec.SECP256R1(), default_backend())
	
	ecdh_public_key = ecdh_private_key.public_key().public_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PublicFormat.SubjectPublicKeyInfo)
	
	ecdsa_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

	ecdsa_public_key  = ecdsa_private_key.public_key().public_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PublicFormat.SubjectPublicKeyInfo)
	
	sign = ecdsa_private_key.sign(ecdh_public_key, ec.ECDSA(hashes.SHA256()))

	conn.send((ecdsa_public_key,ecdh_public_key,sign))

	ecdsa_pub_recv,ecdh_pub_recv,sign_recv = conn.recv()

	peer_ecdsa_pub_recv = serialization.load_pem_public_key(
            ecdsa_pub_recv,
            backend=default_backend())
	try:
		peer_ecdsa_pub_recv.verify(sign_recv, ecdh_pub_recv, ec.ECDSA(hashes.SHA256()))
		
		print("ECDSA Signature OK")
	except InvalidSignature:
		print('ECDSA Signature fail')
	
	peer_ecdh_pub_key = serialization.load_pem_public_key(
            ecdh_pub_recv,
            backend=default_backend())
	shared_key = ecdh_private_key.exchange(ec.ECDH(),peer_ecdh_pub_key)

	my_tag = hashs(bytes(shared_key))
	conn.send(my_tag)
	peer_tag = conn.recv()
	if my_tag == peer_tag:
		print('DH OK')
		return my_tag
	else:
		print('DH FAIL')

	conn.close()       # fechar a conecção

def Emitter(conn):

	key = KeyAgree(conn)
	
	nonce = os.urandom(12)
	conn.send(nonce)

	text = lorem.text().encode('utf-8',"ignore")
	aad = b"authenticated but unencrypted data"
	conn.send(aad)
	chacha = ChaCha20Poly1305(key)
	ct = chacha.encrypt(nonce, text,aad)
	conn.send(ct)

def Reciever(conn):
	key = KeyAgree(conn)
	nonce = conn.recv()
	chacha = ChaCha20Poly1305(key)
	aad = conn.recv()
	ct = conn.recv()
	try:
		decriptedtext = chacha.decrypt(nonce, ct,aad)
		print(decriptedtext)
	except InvalidSignature:
		print("Decription Failed")
		

BiConn(Emitter,Reciever,timeout=30).auto()