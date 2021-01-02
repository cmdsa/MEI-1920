Instruçoes de uso: <br/>
1º Executar o ficheiro Server.py num terminal <br/>
2º Executar o ficheiro Client.py num 2º terminal<br/>
3ª Escrever mensagem no terminal onde o Client.py está a rodar<br/>
4º Ver a mensagem no terminal onde o Server.py está a rodar<br/>


Funcionamento: <br/>
O utilizador dá o input no terminal onde o Client.py está a correr<br/>
O ficheiro é então encriptado e é retornado a mensagem encriptada junto com a key o iv <br/>
A mensagem é recebida pelo server, sendo então desencriptada. A string recebida é dividida em : iv, key, mensg. encrp. <br/>
<br/>
<br/>



Observação:<br/>
Existem duas implementaçoes, uma com AES em modo GCM, e outra com AES em modo CCM<br/>
O AES-GCM é composta pela cifra por blocos AES a utilizar Galois/Counter Mode, que é conhecido pela sua performance<br/>
O AES-CCM é composta pela cifra por blocos AES a utilizar Counter com CBC-MAC, que combina CTR (Counter Mode) <br/>
e CBC-MAC (cipher block chaining message authentication code)<br/>
Ambas oferecem integridade e confidencialidade a mensagem <br/>

