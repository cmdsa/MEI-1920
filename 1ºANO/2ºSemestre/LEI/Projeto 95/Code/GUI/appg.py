import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
import requests
from getproduct import *

#from createDB import *



class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
    #Elementos widgests correspondem a objetos de diversas clases
    #FRAME-Button-Label-Text-Canvas
    def create_widgets(self):
        
        #estado = 0
        #Botao TABELAS
        self.db_Btn = tk.Button(text = "TABELAS",  height = 3, 
          width = 15, fg = "black", bg = "grey",
                                   command = self.openTableW)

        self.db_Btn.pack(side=tk.BOTTOM)

        #Botao Scan
        self.scan_Btn = tk.Button(text = "ANALISAR",  height = 10, 
          width = 20, fg = "black", bg = "grey",
                                   command = lambda:[getCVE(cpelistmodule),self.popup])
        
        self.scan_Btn.pack(side=tk.BOTTOM, expand=tk.YES)
       
       
        #self.lista = tk.Listbox(root)
        #self.lista.pack(side="top")
        

        #vuln = ['vul2','vul1','vul3']
        #for vul in vuln:
        #    self.lista.insert(tk.END, vul)
        
    def popup(self):
        
        showinfo("Aviso!","A ANALISAR...Aguarde")


    def msgScan(self, estado):
             
        if estado == 1:
            msg = tk.Label(root, text = "A ANALISAR...Aguarde") 
            msg.config(font=("Courier", 14))
            msg.pack()
            print("Estado: " + str(estado))

    #Abre janela das tabelas
    def openTableW(self): 
      
        #Objeto q tratara nova janela
        newWindow = tk.Toplevel(self.master) 
        # Titulo da janela 
        newWindow.title("Resultado") 
        # Tamanho da janela 
        newWindow.geometry("300x300") 
        # A Label widget to show in toplevel 
        Label(newWindow,  
            text ="Falta os Dados").pack()
        #Acrescentar as tabelas
        newTable = self.tables()
         
    def tables(self):
        # code for creating table 
        for i in range(total_rows): 
            for j in range(total_columns): 
                  
                self.e = Entry(root, width=20, fg='blue', 
                               font=('Arial',16,'bold')) 
                  
                self.e.grid(row=i, column=j) 
                self.e.insert(END, lst[i][j])
         # take the data 
        lst = [(1,'Raj','Mumbai',19), 
            (2,'Aaryan','Pune',18), 
            (3,'Vaishnavi','Mumbai',20), 
            (4,'Rachna','Mumbai',21), 
            (5,'Shubham','Delhi',21)] 
        
   
        # find total number of rows and 
        # columns in list 
        total_rows = len(lst) 
        total_columns = len(lst[0]) 
    


    ##Função responde
    def list_update(self):        
        print("Atualiza lista")
        #Adicionar itens 1 de cada vez
        #self.lista.insert(tk.END,"1 item")
        #self.lista.insert(tk.END,"2 item")
        #self.lista.insert(tk.END,"3 item")
        #Adicionar varios itens apartir de uma list
        vuln = ['vul2','vul1','vul3']
        for vul in vuln:
            self.lista.insert(tk.END, vul)
        #Apaga todos os itens
        #self.lista.delete(0,tk.END)
        #Apaga apenas 1
        self.lista.delete(0,0)

        
    
    def listaVul(self):
        self.lista = tk.Listbox(root)
        self.lista.pack()
        #Adicionar itens 1 de cada vez
        self.lista.insert(tk.END, "1 item")
        



root = tk.Tk()
root.title("Scanner Vulnerabilidades")
root.geometry("600x400+400+150")
app = Application(master=root)
app.mainloop()


