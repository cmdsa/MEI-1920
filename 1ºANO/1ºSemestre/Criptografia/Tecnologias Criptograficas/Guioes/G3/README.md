Instruçoes de uso: <br/>
1º Criar um ficheiro texto ou usar o 'input.txt' <br/>
2º Executar um dos scripts 'EncThenMac.py','EncAndMac.py','MacThenEnc.py' <br/>


Funcionamento: <br/>
Ambos os scripts têm funcionamentos semelhantes, diferenciando na ordem em que o processo é realizado <br/>
No EncThenMac, primeiro aplica-se a cifra, sendo que o  MAC é aplicado depois sobre o ficheiro cifrado<br/>
No EncAndMac, tanto o MAC como a cifra são aplicados sobre o ficheiro<br/>
No MacThenEnc, primeiro é aplicado o MAC sobre o ficheiro, e depois o resultado é cifrado<br/>
 <br/>



Observação:<br/>
Ao realizar o script MacAndEnc, nós não guardamos o MAC num ficheiro, apenas porque este trabalho se trata de uma <br/>
demostração de aplicação, sendo que estamos cientes que neste metodo existe a necessidade de enviar o MAC com o <br/>
ficheiro cifrado <br/>
