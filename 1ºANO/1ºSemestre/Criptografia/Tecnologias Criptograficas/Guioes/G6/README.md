Instruçoes de uso: <br/>
1º Executar o ficheiro Server.py num terminal <br/>
2º Executar o ficheiro Client.py num 2º terminal<br/>
3ª Escrever mensagem no terminal onde o Client.py está a rodar<br/>
4º Ver a mensagem no terminal onde o Server.py está a rodar<br/>


Funcionamento: <br/>
É gerado uma chave publica e uma chave privada por parte do cliente,sendo que a publica é enviada pro Servidor<br/>
É gerado uma chave publica e uma chave privada por parte do Servidor,sendo que a publica é enviada pro Cliente<br/>
<br/>
A partir da chave publica enviada pelo Servidor e a chave privada do Cliente, é gerada uma chave partilhada, <br/>
que é então usada como chave pelo AES para encriptação<br/>
<br/> 
A partir da chave publica enviada pelo Cliente e a chave privada do Server, é gerada uma chave partilhada,
que é então usada como chave pelo AES para desencriptação, caso sejam compativeis.

<br/>
<br/>




