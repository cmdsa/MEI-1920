#!/usr/bin/python3

import os
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


#encripta o texto
def encripta(texto):
	key = os.urandom(32)
	nonce = os.urandom(16)
	algorithm = algorithms.ChaCha20(key, nonce)
	cipher = Cipher(algorithm, mode=None, backend=default_backend())
	encryptor = cipher.encryptor()
	mensagem = encryptor.update(texto.encode("utf-8"))
	print("Texto encriptado:")
	print(mensagem)


#funcao que recebe o input de texto
def introduzirTexto(txtnum,tamanho):
	i = True
	while(i):
		texto = input("Texto "+txtnum + " com tamanho " + tamanho + ":")
		if(len(texto) == int(tamanho)):
			i = False
		else:
			print("Erro : Texto tem de ter tamanho "+tamanho)
	return texto



opcao = 2
tentativas = 0
acertadas =0
while opcao!=0:

	tentativas+=1
	print("tamanho do texto a encriptar")
	tamanho= input()

	texto1 = introduzirTexto("1",tamanho)
	texto2 = introduzirTexto("2",tamanho)
	#random para escolher qual texto vai ser encriptado
	txtencript = random.randint(0,1)
	if txtencript == 0:
		encripta(texto1)
	else:
		encripta(texto2)

	print("Qual é o texto encriptado?")
	print("Opcao 0 : "+ texto1)
	print("Opcao 1 : "+ texto2)
	resposta = input()
	#verifica se a resposta é igual ao texto encriptado
	if txtencript == int(resposta):
		print("Correto")
		acertadas +=1
	else:
		print("Errado")
	
	option = input("Continuar?[s/n] ")
	if option =="s":
		continue
	elif  option =="n":
		opcao = 0

#estatisticas
print("Acertadas: " + str(acertadas))
print("Tentativas: " + str(tentativas))
print("Segurança estabelecida = " + str(2*((acertadas/tentativas)- 1/2)))
