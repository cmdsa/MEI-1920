Instruçoes de uso: <br/>
1º Executar o ficheiro genKey.py para gerar as chaves <br/>
2º Executar o ficheiro Server.py num terminal <br/>
3º Executar o ficheiro Client.py num 2º terminal<br/>
4ª Escrever mensagem no terminal onde o Client.py está a rodar<br/>
5º Ver a mensagem no terminal onde o Server.py está a rodar<br/>


Funcionamento: <br/>

A mensagem é assinada com a chave privada do Cliente e é enviada para o servidor<br/>
A mensagem é verificada com a chave publica do Cliente pelo Servidor <br/>
A mensagem é assinada com a chave privada do Servidor e é enviada para o Cliente<br/>
A mensagem é verificada com a chave publica do Servidor pelo Cliente <br/>
Se a assinatura coincidir a mensagem é mostrada, se não ocorre uma excepção <br/>
<br/> 
<br/>
<br/>




