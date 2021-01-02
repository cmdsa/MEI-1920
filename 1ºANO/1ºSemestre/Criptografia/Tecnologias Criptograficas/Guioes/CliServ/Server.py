# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
	Cipher, algorithms, modes)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh, padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from OpenSSL import crypto
from cryptography import x509

conn_cnt = 0
conn_port = 8888
max_msg_size = 9999

p = 99494096650139337106186933977618513974146274831566768179581759037259788798151499814653951492724365471316253651463342255785311748602922458795201382445323499931625451272600173180136123245441204133515800495917242011863558721723303661523372572477211620144038809673692512025566673746993593384600667047373692203583
g = 44157404837960328768872680677686802650999163226766694797650810379076416463147265401084491113667624054557335394761604876882446924929840681990106974314935015501571333024773172440352475358750668213444607353872754650805031912866692119819377041901642732455911509867728218394542745330014071040326856846990119719675

p12 = crypto.load_pkcs12(open("servidor.p12", 'rb').read(), "Cripto2019")
cert = p12.get_certificate()
pem = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
print(len(pem))
priv_key = p12.get_privatekey()
priv_key_ck = priv_key.to_cryptography_key()

CA_cer = crypto.load_certificate(crypto.FILETYPE_PEM,open('ca.cert.pem','rb').read())
CA_pem = crypto.dump_certificate(crypto.FILETYPE_PEM, CA_cer)
trusted_pem = crypto.load_certificate(crypto.FILETYPE_PEM, CA_pem)
CAinter_cer = crypto.load_certificate(crypto.FILETYPE_PEM,open('intermediate.cert.pem','rb').read())
CAinter_pem = crypto.dump_certificate(crypto.FILETYPE_PEM, CAinter_cer)
trustedinter_pem = crypto.load_certificate(crypto.FILETYPE_PEM, CAinter_pem)
store = crypto.X509Store()
store.add_cert(trusted_pem)
store.add_cert(trustedinter_pem)

class ServerWorker(object):
	""" Classe que implementa a funcionalidade do SERVIDOR. """
	def __init__(self, cnt, addr=None):
		""" Construtor da classe. """
		self.id = cnt
		self.addr = addr
		self.msg_cnt = 0
	def process(self, msg):
		""" Processa uma mensagem (`bytestring`) enviada pelo CLIENTE.
			Retorna a mensagem a transmitir como resposta (`None` para
			finalizar ligação) """

		if(self.msg_cnt == 0):
			self.msg_cnt +=1

			pn = dh.DHParameterNumbers(p, g)
			parameters = pn.parameters(default_backend())

			server_private_key = parameters.generate_private_key()
			server_public_key = server_private_key.public_key()
			

			public_client_pem = msg[256:2061]
			public_client_pem = crypto.load_certificate(crypto.FILETYPE_PEM, public_client_pem)
			public_client_key_pk = public_client_pem.get_pubkey()
			public_client_key_ck = public_client_key_pk.to_cryptography_key()

			store_ctx = crypto.X509StoreContext(store, public_client_pem)
			result = store_ctx.verify_certificate()

			if result is None:
				print(" Verificado")
			else:
				print("Não Verificado")

			public_client_key_ck.verify(
							 msg[:256],
							 msg[2061:],
							 padding.PSS(
								 mgf=padding.MGF1(hashes.SHA256()),
								 salt_length=padding.PSS.MAX_LENGTH
							 ),
							 hashes.SHA256()
						 )
		   
			client_key=load_pem_public_key( msg[2061:],default_backend())

			

			shared_key = server_private_key.exchange(client_key)

			self.derived_key = HKDF(
			algorithm=hashes.SHA256(),
			length=32,
			salt=None,
			info=b'handshake data',
			backend=default_backend()
			).derive(shared_key)

			new_msg = server_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

			signature = priv_key_ck.sign(
						 new_msg,
						 padding.PSS(
							 mgf=padding.MGF1(hashes.SHA256()),
							 salt_length=padding.PSS.MAX_LENGTH
						 ),
						 hashes.SHA256()
					 )

			return signature + pem + new_msg if len(new_msg)>0 else None

			

		else:
			self.msg_cnt +=1
			decryptor = Cipher(algorithms.AES(self.derived_key),modes.GCM(msg[16:32],msg[:16]),backend=default_backend()).decryptor()
			txt = decryptor.update(msg[64:]) + decryptor.finalize()

			
			txt = txt.decode()
			
		   
			
			print('%d : %r' % (self.id,txt))
			
			iv = os.urandom(16)
			key = os.urandom(32)
			encryptor = Cipher(algorithms.AES(self.derived_key),modes.GCM(iv),backend=default_backend()).encryptor()
			new_msg = txt.upper().encode()

			

			
			new_msg = encryptor.update(new_msg) + encryptor.finalize()
			
			return encryptor.tag + iv + key + new_msg if len(new_msg)>0 else None


#
#
# Funcionalidade Cliente/Servidor
#
# obs: não deverá ser necessário alterar o que se segue
#


@asyncio.coroutine
def handle_echo(reader, writer):
	global conn_cnt
	conn_cnt +=1
	addr = writer.get_extra_info('peername')
	srvwrk = ServerWorker(conn_cnt, addr)
	data = yield from reader.read(max_msg_size)
	while True:
		if not data: continue
		if data[:1]==b'\n': break
		data = srvwrk.process(data)
		if not data: break
		writer.write(data)
		yield from writer.drain()
		data = yield from reader.read(max_msg_size)
	print("[%d]" % srvwrk.id)
	writer.close()


def run_server():
	loop = asyncio.get_event_loop()
	coro = asyncio.start_server(handle_echo, '127.0.0.1', conn_port, loop=loop)
	server = loop.run_until_complete(coro)
	# Serve requests until Ctrl+C is pressed
	print('Serving on {}'.format(server.sockets[0].getsockname()))
	print('  (type ^C to finish)\n')
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass
	# Close the server
	server.close()
	loop.run_until_complete(server.wait_closed())
	loop.close()
	print('\nFINISHED!')

run_server()
