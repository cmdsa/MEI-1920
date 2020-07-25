from OpenSSL import crypto



def getpem(cert,passwd):
	# open it, using password. 
	p12 = crypto.load_pkcs12(open(cert, 'rb').read(), passwd)
	cert = p12.get_certificate()
	pem = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
	return pem

def verify_chain_of_trust(name,cert_pem):
	
	trusted_cert = crypto.load_certificate(crypto.FILETYPE_PEM, CA_pem)

	certificate = crypto.load_certificate(crypto.FILETYPE_PEM, cert_pem)
	# Create and fill a X509Sore with trusted certs
	store = crypto.X509Store()
	store.add_cert(trusted_cert)
	
	# Create a X590StoreContext with the cert and trusted cert
    # and verify the the chain of trust
	store_ctx = crypto.X509StoreContext(store, certificate)
	# Returns None if certificate can be validated
	result = store_ctx.verify_certificate()

	if result is None:
		print(name + " Verificado")
	else:
		print(name+ "Não Verificado")

CA_cer = crypto.load_certificate(crypto.FILETYPE_ASN1,open('CA.cer','rb').read())
CA_pem = crypto.dump_certificate(crypto.FILETYPE_PEM, CA_cer)


verify_chain_of_trust("Cliente1",getpem("Cliente1.p12","1234"))
verify_chain_of_trust("Servidor",getpem("Servidor.p12","1234"))