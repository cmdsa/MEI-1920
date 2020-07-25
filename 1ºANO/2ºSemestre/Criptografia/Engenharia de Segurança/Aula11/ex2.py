import re
import datetime

(LEN_Value,LEN_Name,LEN_NIF) = (10,30,9)

#Verifica se Input é valido
def validaValor(valor):
    #Apenas numeros[0-9], e apenas 2 casas decimais(. ou ,)   
    mat = re.match(r'^[1-9]\d*([\.\,]\d{1,2})?$', valor)
    if(mat is not None and len(valor) < LEN_Value):
        print('Input Aceite!')
        return True
    else:
        print('Input Rejeitado!')
        return False


#Verifica o input
def validaData(data):
    try:
        #(DD-MM-AAAA)
        dtv = datetime.datetime.strptime(data,'%d-%m-%Y')
        print('Input Aceite!')
        return dtv
    except:
        print('Input Rejeitado!')
        return False


#Verifica se nao tem numeros
#Verifica Comprimento do Input
def validaNome(nome):
    #Aceita primeiro nome com pelo menos 2 letras
    #Ve o espaço entre o segundo nome
    #aceita pelo menos 1 letra no segundo nome
    pad = re.match(r'^([a-zA-Z]{2,}\s[a-zA-z]{1,}'r'?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)', nome)

    if(pad is not None and len(nome)< LEN_Name):
        print('Input Aceite')
        return nome
    else:
        print('Input Rejeitado!')
        return False
#Verifica o comprimento do input
#Verifica carater inicial do NIF
def validaNIF(nif):
    if len(nif) != LEN_NIF:
        print('Input Rejeitado!')
        return False
    else:
        if nif[0] not in '125689':
            print('NIF Incorreto')
            return False
        else:
            #Falta a verificaçao da validade
            #https://gist.github.com/dreispt/024dd11c160af58268e2b44019080bbf
            print('Input Aceite!')
            return True


if __name__ == "__main__":

    val = input("Introduza valor (p.0.00): ")
    value = validaValor(val)
    
    dat = input("Introduza data (DD-MM-AAAA): ")
    data = validaData(dat)

    name = input("Introduza nome(Completo): ")
    nome = validaNome(name)

    nifV = input("Introduza NIF: ")
    nif = validaNIF(nifV)


