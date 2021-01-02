import sqlite3

database = "dbtest.db"

class databaseManager():

    def __init__(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect(database, check_same_thread=False)
            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            print(e)
    
    def insertintoCPEinPC(self,values):
        sqlquery = '''insert into CPEinPC(cpeID,vendorname,
        productname,version,lastSearch) values(?,?,?,?,?);'''
        try:
            self.cur.execute(sqlquery,(values))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
    
    def checkifCPEalreadyinPC(self,Cpe):
        sqlquery = "SELECT EXISTS(SELECT 1 FROM CPEinPC WHERE cpeID = ?)"
        try:
            self.cur.execute(sqlquery,(Cpe,))
            return self.cur.fetchone()[0]
        except sqlite3.Error as e:
            print(e)
    def UpdateCPEinPCTable(self,date,Cpe):
        sqlquery = "UPDATE CPEinPC Set lastSearch = ? WHERE cpeID = ?"
        try:
            self.cur.execute(sqlquery,(date,Cpe,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
            
    def insertintoCPECVE(self,values):
        '''CPECVE(cpeID,cveID)'''
        sqlquery = '''insert into CPECVE(cpeID,cveID) values(?,?);'''
        try:
            self.cur.execute(sqlquery,(values))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def insertintoALLCVE(self,values):
        sqlquery = '''insert into ALLCVE(cveID,datatype,dataformat,
        dataversion,description,publishedDate,lastModifiedDate) values(?,?,?,?,?,?,?);'''
        try:
            self.cur.execute(sqlquery,(values))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
    


    def insertintoCVSS3(self,values):
        sqlquery = '''insert into CVSS3(cveID,version,vectorString,attackVector,attackComplexity
        ,privilegesRequired,userInteraction,scope,confidentialityImpact,integrityImpact,
        availabilityImpact,baseScore,baseSeverity,exploitabilityScore,impactScore) 
        values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''
        try:

            self.cur.execute(sqlquery,(values))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def insertintoCVSS2(self,values):
        sqlquery = '''insert into CVSS2(cveID,version,vectorString,accessVector,accessComplexity,authentication,
        confidentialityImpact,integrityImpact,availabilityImpact,baseScore,severity,exploitabilityScore,
        impactScore,acInsufInfo,obtainAllPrivilege,obtainUserPrivilege,obtainOtherPrivilege,
        userInteractionRequired) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''
        try:
            self.cur.execute(sqlquery,(values))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def getCPE(self):
        sqlquery = '''SELECT * FROM CPECVE'''
        try:
            self.cur.execute(sqlquery)
            self.cur.row_factory = lambda cursor, row: [row[0],row[1]]
            rows = self.cur.fetchall()
            return rows
        except sqlite3.Error as e:
            print(e)

    def getCVEData(self,cveid):
        sqlquery = "SELECT * FROM ALLCVE where cveID =?"
        try:
            self.cur.execute(sqlquery,(cveid,))
            self.cur.row_factory = lambda cursor, row: {'cveID': row[0],'datatype':row[1],'dataformat':row[2],
                                                        'dataversion':row[3],'description' : row[4],
                                                        'publishedDate':row[5],'lastModifiedDate':row[5]}
            rows = self.cur.fetchone()
            return rows
        except sqlite3.Error as e:
            print(e)

    def getCVSS2Data(self,cveid):
        sqlquery = "SELECT * FROM CVSS2 where cveID =?"
        try:
            self.cur.execute(sqlquery,(cveid,))
            self.cur.row_factory = lambda cursor, row:{"version":row[1],"vectorString":row[2],
                                                        "accessVector":row[3], "accessComplexity":row[4],
                                                        "authentication":row[5],"confidentialityImpact":row[6],
                                                        "integrityImpact":row[7],"availabilityImpact":row[8],
                                                        "baseScore":row[9], "severity":row[10],
                                                        "exploitabilityScore":row[11],"impactScore":row[12],
                                                        "acInsufInfo":row[13],
                                                        "obtainAllPrivilege":row[14],"obtainUserPrivilege":row[15],
                                                        "obtainOtherPrivilege":row[16],"userInteractionRequired": row[17]}
            rows = self.cur.fetchone()
            return rows
        except sqlite3.Error as e:
            print(e)
    def getCVSS3Data(self,cveid):
        sqlquery = "SELECT * FROM CVSS3 where cveID =?"
        try:
            self.cur.execute(sqlquery,(cveid,))
            self.cur.row_factory = lambda cursor, row:{"version":row[1],"vectorString":row[2],
                                                        "attackVector":row[3], "attackComplexity":row[4],
                                                        "privilegesRequired":row[5],"userInteraction":row[6],
                                                        "scope":row[7],"confidentialityImpact":row[8],
                                                        "integrityImpact":row[9], "availabilityImpact":row[10],
                                                        "baseScore":row[11],"baseSeverity":row[12],
                                                        "exploitabilityScore":row[13],
                                                        "impactScore":row[14]}
            rows = self.cur.fetchone()
            return rows
        except sqlite3.Error as e:
            print(e)
    