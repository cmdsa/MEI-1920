from os import terminal_size
from threading import Thread
from storeData import dbmanager
from flask_table import Table, Col, LinkCol
from flask import Flask,render_template,request,flash,redirect
from managedb import databaseManager
from getproduct import getthingsdone
from threading import Thread

app = Flask(__name__)

dbmanager = databaseManager()

@app.route('/', methods=('GET', 'POST'))
def main():

    if(request.form.get("resulbutton")):
        
        return  redirect("/results")

    elif(request.form.get("analbutton")):
        getthingsdone()
        return  redirect("/results")

    return render_template('frontpage.html')

@app.route('/Analise', methods=('GET', 'POST'))
def proce():

    return render_template('loading.html')


@app.route('/results')
def index():
    
    rows = dbmanager.getCPE()
    headers = ['CPEID','CVEID']
    if(len(rows) > 0):
        return render_template('cpefound.html',headers=headers,rows=rows)
    else:
        return "nothing here yet"

@app.route('/item/<string:CVEID>')
def single_item(CVEID):
    rowCVE = dbmanager.getCVEData(CVEID)
    rowCVSS2 = dbmanager.getCVSS2Data(CVEID)
    rowCVSS3 = dbmanager.getCVSS3Data(CVEID)
    # Similarly, normally you would use render_template
    return render_template('cvedetail.html',rowCVSS2=rowCVSS2,rowCVE=rowCVE,rowCVSS3=rowCVSS3)

if __name__ == '__main__':
    app.run(debug=True,port=5002)