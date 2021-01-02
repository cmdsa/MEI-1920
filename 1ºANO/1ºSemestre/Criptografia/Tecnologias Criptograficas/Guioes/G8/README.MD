## Usar a linha de commandos para converter e verificar <br />
 
### converter CA.cer para o formato .pem <br />
```
openssl x509 -inform der -in CA.cer -out CA.pem
```
### converter Servidor.p12 e Cliente1.p12 para o formato .pem: 
```
openssl pkcs12 -in Cliente1.p12 -passin pass:1234 -passout pass:1234 -out Cliente1.pem
openssl pkcs12 -in Servidor.p12 -passin pass:1234 -passout pass:1234 -out Servidor.pem
```

### Concatenar Servidor.pem e Cliente.pem com CA.pem:
```
cat Cliente1.pem CA.pem > Cliente1_trust.pem
cat Servidor.pem CA.pem > Servidor_trust.pem
```
### Verificar se os certificados são validos<br />
```
openssl verify -CAfile CA.pem Cliente1_trust.pem 
openssl verify -CAfile CA.pem Servidor_trust.pem 
```
<br />
Obs:<br />
Há um makefile com estas linhas de comando na diretoria (Chamado "Makefile", Abrir terminal na pasta -> escrever "make")<br />

## Com o PyOpenSSL:<br />
Rodar o script openpyssl.py




