# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
import socket
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
	Cipher, algorithms, modes)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh,padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from OpenSSL import crypto
from cryptography import x509

conn_port = 8888
max_msg_size = 9999

p = 99494096650139337106186933977618513974146274831566768179581759037259788798151499814653951492724365471316253651463342255785311748602922458795201382445323499931625451272600173180136123245441204133515800495917242011863558721723303661523372572477211620144038809673692512025566673746993593384600667047373692203583
g = 44157404837960328768872680677686802650999163226766694797650810379076416463147265401084491113667624054557335394761604876882446924929840681990106974314935015501571333024773172440352475358750668213444607353872754650805031912866692119819377041901642732455911509867728218394542745330014071040326856846990119719675


p12 = crypto.load_pkcs12(open("Cliente1.p12", 'rb').read(), "1234")
cert = p12.get_certificate()
pem = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
priv_key = p12.get_privatekey()
priv_key_ck = priv_key.to_cryptography_key()

CA_cer = crypto.load_certificate(crypto.FILETYPE_ASN1,open('CA.cer','rb').read())
CA_pem = crypto.dump_certificate(crypto.FILETYPE_PEM, CA_cer)
trusted_pem = crypto.load_certificate(crypto.FILETYPE_PEM, CA_pem)
store = crypto.X509Store()
store.add_cert(trusted_pem)

class Client:
	""" Classe que implementa a funcionalidade de um CLIENTE. """
	def __init__(self, sckt=None):
		""" Construtor da classe. """
		self.sckt = sckt
		self.msg_cnt = 0
	def process(self, msg=b""):
		""" Processa uma mensagem (`bytestring`) enviada pelo SERVIDOR.
			Retorna a mensagem a transmitir como resposta (`None` para
			finalizar ligação) """
		if(self.msg_cnt == 0):
			self.msg_cnt +=1

			pn = dh.DHParameterNumbers(p, g)
			parameters = pn.parameters(default_backend())

			self.peer_private_key = parameters.generate_private_key()
			peer_public_key  = self.peer_private_key.public_key()

			new_msg = peer_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

			signature = priv_key_ck.sign(
						 new_msg,
						 padding.PSS(
							 mgf=padding.MGF1(hashes.SHA256()),
							 salt_length=padding.PSS.MAX_LENGTH
						 ),
						 hashes.SHA256()
					 )
		 
			return signature + pem + new_msg  if len(new_msg)>0 else None
		
		if(self.msg_cnt == 1):
			self.msg_cnt +=1
			####
			#guarda o certificado
			public_server_pem = msg[256:1541]
			#carrega o certificado
			public_server_pem = crypto.load_certificate(crypto.FILETYPE_PEM, public_server_pem)
			#obtem a chave
			public_client_key_pk = public_server_pem.get_pubkey()
			#converte a chave para uma suportada pelo cryptography
			public_server_key_ck = public_client_key_pk.to_cryptography_key()
			
			store_ctx = crypto.X509StoreContext(store, public_server_pem)
			result = store_ctx.verify_certificate()

			if result is None:
				print(" Verificado")
			else:
				print("Não Verificado")

			public_server_key_ck.verify(
							 msg[0:256],
							 msg[1541:],
							 padding.PSS(
								 mgf=padding.MGF1(hashes.SHA256()),
								 salt_length=padding.PSS.MAX_LENGTH
							 ),
							 hashes.SHA256()
						 )

			server_key=load_pem_public_key(msg[1541:],default_backend())

			shared_key = self.peer_private_key.exchange(server_key)
			self.derived_key = HKDF(
			algorithm=hashes.SHA256(),
			length=32,
			salt=None,
			info=b'handshake data',
			backend=default_backend()
			).derive(shared_key)
			
			
			iv = os.urandom(16)
			key = os.urandom(32)
			encryptor = Cipher(algorithms.AES(self.derived_key),modes.GCM(iv),backend=default_backend()).encryptor()
			print('Input message to send (empty to finish)')
			new_msg = input().encode()
			
		   

			new_msg = encryptor.update(new_msg) + encryptor.finalize()
			return encryptor.tag + iv + key + new_msg if len(new_msg)>0 else None
		
		else:
			self.msg_cnt +=1
			decryptor = Cipher(algorithms.AES(self.derived_key),modes.GCM(msg[16:32],msg[:16]),backend=default_backend()).decryptor()
			txt = decryptor.update(msg[64:]) + decryptor.finalize()
		

			txt = txt.decode()

			print('Received (%d): %r' % (self.msg_cnt , txt))
			print('Input message to send (empty to finish)')
			new_msg = input().encode()
			iv = os.urandom(16)
			key = os.urandom(32)
			encryptor = Cipher(algorithms.AES(self.derived_key),modes.GCM(iv),backend=default_backend()).encryptor()
			
		 
			new_msg = encryptor.update(new_msg) + encryptor.finalize()
			return encryptor.tag + iv + key + new_msg if len(new_msg)>0 else None



#
#
# Funcionalidade Cliente/Servidor
#
# obs: não deverá ser necessário alterar o que se segue
#


@asyncio.coroutine
def tcp_echo_client(loop=None):
	if loop is None:
		loop = asyncio.get_event_loop()

	reader, writer = yield from asyncio.open_connection('127.0.0.1',
														conn_port, loop=loop)
	addr = writer.get_extra_info('peername')
	client = Client(addr)
	msg = client.process()
	while msg:
		writer.write(msg)
		msg = yield from reader.read(max_msg_size)
		if msg :
			msg = client.process(msg)
		else:
			break
	writer.write(b'\n')
	print('Socket closed!')
	writer.close()

def run_client():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(tcp_echo_client())


run_client()
