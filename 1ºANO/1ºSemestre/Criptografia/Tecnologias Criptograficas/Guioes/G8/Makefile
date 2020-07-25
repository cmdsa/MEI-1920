make:
	openssl x509 -inform der -in CA.cer -out CA.pem
	openssl pkcs12 -in Cliente1.p12 -passin pass:1234 -passout pass:1234 -out Cliente1.pem
	openssl pkcs12 -in Servidor.p12 -passin pass:1234 -passout pass:1234 -out Servidor.pem
	openssl verify -CAfile CA.pem Cliente1.pem 
	openssl verify -CAfile CA.pem Servidor.pem 
	cat Cliente1.pem CA.pem > Cliente1_trust.pem
	cat Servidor.pem CA.pem > Servidor_trust.pem
	openssl verify -CAfile CA.pem Cliente1_trust.pem
	openssl verify -CAfile CA.pem Servidor_trust.pem
	

