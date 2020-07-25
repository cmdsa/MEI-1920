### Instruçoes de uso: <br/>
1º Executar o ficheiro Server.py num terminal <br/>
2º Executar o ficheiro Client.py num 2º terminal<br/>
3ª Escrever mensagem no terminal onde o Client.py está a rodar<br/>
4º Ver a mensagem no terminal onde o Server.py está a rodar<br/>

### Como foi gerado os certificados <br/>
Para realizar este guião utilizamos o guiao anterior (Guião 9), sendo que a modificação feita foi alterar os certificados e os pkcs12 utilizados para aqueles gerados por nós, para além da adição do certificado intermédio.<br/>
Para a criação dos certificados de cliente e servidor bem como dos certificados das autoridades de certificação recorremos ao tutorial presente neste link [https://jamielinux.com/docs/openssl-certificate-authority/index-full.html](https://jamielinux.com/docs/openssl-certificate-authority/index-full.html) <br/>
Todas os certificados e chaves resultantes encontram-se na pasta ```root```


### Funcionamento: <br/>

A mensagem é assinada com a chave privada do Cliente,sendo que depois é enviado o certificado publico para o servidor  <br/>
A mensagem é verificada com a chave publica do Cliente pelo Servidor, obtida apartir do certificado recebido <br/>
A mensagem é assinada com a chave privada do Servidor,sendo que depois é enviado o certificado publico para o Cliente<br/>
A mensagem é verificada com a chave publica do Servidor pelo Cliente, obtida apartir do certificado recebido  <br/>
Se o certificado é valido, aparecerá como "Validado" no output<br/>
Se a assinatura coincidir a mensagem é mostrada, se não ocorre uma excepção <br/>
<br/> 
<br/>
<br/>




