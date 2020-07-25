Instruçoes de uso: <br/>
1º Criar um ficheiro texto ou usar o 'file.txt' <br/>
2º Executar o script 'encrypt.py' <br/>
3º Executar o script 'decrypt.py' <br/> <br/>

Funcionamento: <br/>
Executamos o encrypt.py para encriptar o file.txt; <br/>
Este vai criar o ficheiro "test.encrypted", com o ficheiro encriptado; <br/>
Guardamos a key para depois desencriptar num ficheiro txt, apenas para o teste <br/>
Depois para voltar a desencriptar, corremos o script decrypt.py para desencriptar o ficheiro test.encrypted <br/> <br/>

Testar o encriptamento: <br/>
Quando abrimos o ficheiro encriptado, podemos verificar que as informaçoes nele contidas já não são as originais,  <br/>
mas sim as encriptadas previamente pelo script. <br/>
Para testar a integridade, modificamos o valor dentro do ficheiro, <br/> 
e tentamos desencriptar novamente com a chave gerada, algo que desencandeia um erro <br/> <br/>

Dificuldades Encontradas: <br/>
Uma dificuldade encontrada foi o ato de guardar a chave de encriptação para uso na decriptação, <br/> 
algo que resolvemos guardando a chave para um ficheiro de texto, para teste. <br/>
