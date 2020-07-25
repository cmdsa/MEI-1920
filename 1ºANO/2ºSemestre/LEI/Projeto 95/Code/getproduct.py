from subprocess import check_output,check_call
import json
import sys
import re
import sys
import requests
from storeData import *
from datetime import datetime
import time

cpematch = "https://services.nvd.nist.gov/rest/json/cves/1.0?cpeMatchString="

def getProductList():
    '''Vai buscar os programas instalados, caso estejam instalados'''
    productList = []
    dpkg = "dpkg-query -W -f='${Package} ${Version}\n'"
    results = check_output(dpkg,shell=True)
    results = results.decode()
    installed = re.split("\n",results)
    for values in installed:
        productList.append(re.split(" ",values))
    for values in productList:
        if values[0] == "":
            productList.remove(values)
            break
        if "ubuntu" in values[1]:
            values[1] = re.split("ubuntu",values[1])[0]

    return ("debian",productList)


def getpythonmodules():
    '''Vai buscar os modulos do python, caso o python esteja instalado'''

    if(sys.version_info[0] == 2):
        command = "pip list --format=freeze"
    if(sys.version_info[0] >=3):
        command = "pip3 list --format=freeze"
    else:
        return None
    results = check_output(command,shell=True)
    results = results.decode()
    installed = re.split("\n",results)
    listpip = []
    for values in installed:
        listpip.append(re.split("==",values))
    return ("python",listpip)


def turnCPE(tuplewithlistandvendor,NoVersion = False):
    '''
    turnCPE(tuple, Bool)

    tuple = vendor,listaprodutos

    Bool if True = NoVersion

    Recebe um tuple com o vendor e a lista de produtos instalados
    como também uma flag,que caso seja True,
    procura estes produtos sem a versão especificada
    '''
    vendor,listofsoft = tuplewithlistandvendor
    cpelist = []
    for programs in listofsoft:
        if programs[0] == "":
            listofsoft.remove(programs)
        else:
            dicpe = {}
            if NoVersion == False:
                dicpe = {
                "part" : "a",
                "vendor" : vendor,
                "product" : programs[0].lower() ,
                "version" : programs[1] ,
                "Update" : "",
                "Edition" : "",
                "Language" : "",
                "Software" : "",
                "Target_Software" : "",
                "Target_Hardware" : "",
                "Other" : ""}
            elif NoVersion == True:
                dicpe = {
                "part" : "a",
                "vendor" : vendor,
                "product" : programs[0].lower() ,
                "version" : "" ,
                "Update" : "",
                "Edition" : "",
                "Language" : "",
                "Software" : "",
                "Target_Software" : "",
                "Target_Hardware" : "",
                "Other" : ""}

            for x in dicpe:
                if dicpe[x] == "":
                    dicpe[x] = "*"
            cpe23 = "cpe:2.3:"+ ':'.join(str(x) for x in dicpe.values())
            cpe23 = cpe23.replace(" ","_")

            cpelist.append((vendor,programs[0],programs[1],cpe23))
    
    return cpelist
        #with open ("file.txt","a")  as file:
            #file.write(cpe23 + "\n")


def getCVE(cpelist):
    '''
    Procura pelos CVE na base de dados da NIST, usando para isto
    a API especificada.
    Recebe um tuple, que contem o vendor, o nome do programa, a versão e o cpe
    '''
    for cpe in cpelist:
        getcpe = requests.get(cpematch +cpe[3])
        if getcpe.ok:
            
            data = getcpe.json()
            print("checking  " + cpe[3])
            StoreCPEinPC(cpe,datetime.today().strftime('%Y-%m-%d'))
            StoreCVE(data,cpe[3])
            
def getthingsdone(NoVersion=False):
    cpelistmodule = turnCPE(getpythonmodules(), NoVersion)
    cpelistproduct = turnCPE(getProductList(), NoVersion)
    getCVE(cpelistmodule)
    getCVE(cpelistproduct)