
import sqlite3

DB_FILE = "dbtest.db"

db = sqlite3.connect(DB_FILE)

c = db.cursor()

createCPEinPC = '''
create table CPEinPC(
    cpeID varchar(100) NOT NULL,
    vendorname varchar(20) NOT NULL,
    productname varchar(50) NOT NULL,
    version float NOT NULL,
    lastSearch date
);
'''

createCPECVE = '''
create table CPECVE(
    cpeID varchar(100) NOT NULL,
    cveID varchar(20) NOT NULL
);
'''
createallcve = '''
create table AllCVE (
   cveID varchar(20) NOT NULL,
   datatype varchar(5) NOT NULL,
   dataformat varchar(5) NOT NULL,
   dataversion float NOT NULL,
   description text,
   publishedDate date,
   lastModifiedDate date
);
'''
createcpeuri = '''create table CPE23URI (
    cveID varchar(20) NOT NULL,
    cpe23uri text,
    vulnerable bool
);'''

createcvss3 = '''create table CVSS3 (
    cveID varchar(20) NOT NULL,
    version float,
    vectorString varchar(50),
    attackVector  varchar(20),
    attackComplexity varchar(10),
    privilegesRequired varchar(10),
    userInteraction varchar(10),
    scope varchar(10),
    confidentialityImpact varchar(10),
    integrityImpact varchar(10),
    availabilityImpact varchar(10),
    baseScore float,
    baseSeverity varchar(10),
    exploitabilityScore float,
    impactScore float
);
'''

createcvss2 = '''create table CVSS2 (
cveID varchar(20) NOT NULL,
version float,
vectorString varchar(50),
accessVector varchar(20),
accessComplexity varchar(10),
authentication varchar(10),
confidentialityImpact varchar(20),
integrityImpact varchar(20),
availabilityImpact varchar(20),
baseScore float,
severity varchar(10),
exploitabilityScore float,
impactScore float,
acInsufInfo float,
obtainAllPrivilege bool,
obtainUserPrivilege bool,
obtainOtherPrivilege bool,
userInteractionRequired bool);'''

sqlstatments = [createCPEinPC,createCPECVE,createallcve,createcpeuri,createcvss3,createcvss2]

for sql in sqlstatments:
   db.execute(sql)