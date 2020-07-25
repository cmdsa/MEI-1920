Instruçoes de uso: <br/>
1º Criar um ficheiro texto ou usar o 'file.txt' <br/>
2º Executar o script 'encrypt.py' <br/>
3º Executar o script 'decrypt.py' <br/> <br/>

Funcionamento: <br/>
Executamos o encrypt.py para encriptar o file.txt; <br/>
Este vai criar o ficheiro "test.encrypted", com o ficheiro encriptado;<br/>
E ainda vai criar outro ficheiro para guardar o salt gerado aleatoreamente<br/>
Depois para voltar a desencriptar, corremos o script decrypt.py para desencriptar o ficheiro test.encrypted <br/> <br/>

Testar o encriptamento: <br/>
Ao encriptar o ficheiro é criada uma senha, para incriptar o ficheiro e de seguida é observado a criaçao de 2 ficheiros.
Um encriptado e outro igualmente encriptado mas do salt.
Quando abrimos o ficheiro encriptado, podemos verificar que as informaçoes nele contidas já não são as originais,  <br/>
mas sim as encriptadas previamente pelo script. <br/>
Para desincriptar o ficheiro é entao necessario insirir a tal senha e so depois é realizada a desencriptação.<br/>
Em caso de brutal attack podiamos ainda aumentar as interções de modo a mitigar esses ataques <br/>
e assim protegem mais a chave derivada.<br/>


Dificuldades Encontradas: <br/>
Uma dificuldade encontrada foi na distinçao das duas abordagens, principalmente perceber melhor o conceito da segunda abordagem.  <br/><br/>

Observação:<br/>
Usar a password como salt faz com que a necessidade de guardar o salt não seja necessário<br/>
mas claro que isso faz com que o salt seja igual à password, e como tal, desprotegido.<br/>
