from fuzzywuzzy import fuzz


#vai por as palavras numa lista
def GetWords(word_list):
    file = open(word_list, 'r', encoding='latin1')
    
    data = file.read()
    data = data.split("\n")
    words_inList = list(data)
    
    return words_inList


# Retorna a string "corrigida" falha as vezes, nothing is perfect
#4 palavras ou menos tende a falhar mais
def ill_Correct(corrString, word_List):
   
    palavrinhas = corrString.split()
    print(palavrinhas)
    newfrase = []
    # loop das palavras a serem verificadas
    for i in range(len(palavrinhas)):
        
        max_ratio = 0
        newstring = ''
        
        # verifica na lista de palavras
        for name in GetWords(word_List):
            
            # calcula o ratio da palavra
            ratio = fuzz.ratio(palavrinhas[i], name)
        
            # se for 100, ou igual, acaba aqui
            if ratio == 100:
                newstring = name
                print(newstring + " " + str(ratio) + "%")
                break
            # se for 60 
            if ratio >= 60:
             #e maior que a anterior
                if ratio > max_ratio:
                    
                    # vai ficar com ela
                    newstring = name
                    print(newstring + " " + str(ratio) + "%")
                    max_ratio = ratio
        print(max_ratio)
        newfrase.append(newstring)
        
    
    return " ".join(newfrase)

#texto com as palavras
with_this_word_List = 'wordlist-preao-20190329.txt'
print('Escrebe mal portuges:')
this_String = input()
print(ill_Correct(this_String,with_this_word_List))