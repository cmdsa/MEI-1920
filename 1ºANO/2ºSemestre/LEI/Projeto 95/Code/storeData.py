from gettext import dngettext
import requests
import sqlite3
import json
import os
from managedb import databaseManager




dbmanager = databaseManager()

def StoreCPEinPC(cpedata,date):
    if(dbmanager.checkifCPEalreadyinPC(cpedata[3]) == 0):
        dbmanager.insertintoCPEinPC((cpedata[3],cpedata[0],cpedata[1],cpedata[2],date))
    else:
        dbmanager.UpdateCPEinPCTable(date,cpedata[3])

def StoreCVE(data,cpe):
    '''Recebe os dados obtidos do NIST, como tambem o cpe para guardar na base de dados'''
    for cves in data["result"]['CVE_Items']:
        if cves != []:
            dbmanager.insertintoCPECVE((str(cpe),cves['cve']['CVE_data_meta']['ID']))
            

            dbmanager.insertintoALLCVE((
                cves['cve']['CVE_data_meta']['ID'],
                cves['cve']['data_type'],
                cves['cve']['data_format'],
                cves['cve']['data_version'],
                cves['cve']['description']['description_data'][0]['value'],
                cves['publishedDate'],
                cves['lastModifiedDate']))


               # TABELA CVSS3 e CVSS2
            if cves['impact'] != {}:

                if 'baseMetricV3' in cves['impact'] and cves['impact']['baseMetricV3'] != {}:
                    cvss3 = cves['impact']['baseMetricV3']['cvssV3']
                    dbmanager.insertintoCVSS3((
                                            cves['cve']['CVE_data_meta']['ID'],
                                            cvss3['version'],
                                            cvss3['vectorString'],
                                            cvss3['attackVector'],
                                            cvss3['attackComplexity'],
                                            cvss3['privilegesRequired'],
                                            cvss3['userInteraction'],
                                            cvss3['scope'],
                                            cvss3['confidentialityImpact'],
                                            cvss3['integrityImpact'],
                                            cvss3['availabilityImpact'],
                                            cvss3['baseScore'],
                                            cvss3['baseSeverity'],
                                            cves['impact']['baseMetricV3']['exploitabilityScore'],
                                            cves['impact']['baseMetricV3']['impactScore']
                                            ))

                if 'baseMetricV2' in cves['impact'] and cves['impact']['baseMetricV2'] != {}:
                    cvss2 = cves['impact']['baseMetricV2']['cvssV2']
                    dbmanager.insertintoCVSS2((
                        cves['cve']['CVE_data_meta']['ID'],
                        cvss2['version'],
                        cvss2['vectorString'],
                        cvss2['accessVector'],
                        cvss2['accessComplexity'],
                        cvss2['authentication'],
                        cvss2['confidentialityImpact'],
                        cvss2['integrityImpact'],
                        cvss2['availabilityImpact'],
                        cvss2['baseScore'],
                        cves['impact']['baseMetricV2']['severity'],
                        cves['impact']['baseMetricV2']['exploitabilityScore'],
                        cves['impact']['baseMetricV2']['impactScore'],
                        cves['impact']['baseMetricV2']['acInsufInfo'] if 'acInsufInfo' in cves['impact']['baseMetricV2'] else "",
                        cves['impact']['baseMetricV2']['obtainAllPrivilege'],
                        cves['impact']['baseMetricV2']['obtainUserPrivilege'],
                        cves['impact']['baseMetricV2']['obtainOtherPrivilege'],
                        cves['impact']['baseMetricV2']['userInteractionRequired'] if 'userInteractionRequired' in cves['impact']['baseMetricV2'] else ""
                        ))


