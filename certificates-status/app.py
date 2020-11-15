import sys
import urllib3
import requests
import datetime
import psycopg2
import os

urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)

sys.path.insert(1, '/certificates-status/src/config')
from config import *

def getCertsInfo():
    
    dbUser = os.environ.get('DB_USER')
    dbHost = os.environ.get('DB_HOST')
    dbPassword = os.environ.get('DB_PASSWORD')
    params = {
        "dbname": "postgres",
        "user": dbUser,
        "host": dbHost,
        "password": dbPassword,
        "port": "5432",
        "sslmode": "require",
    }
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute ("select * from cloudlets_certificates")
    dbInfo = cur.fetchall()
    for cluster in dbInfo:
        issuerApi = cluster[1]
        subjectApi = cluster[2]
        expApi = cluster[3]
        issuerApps = cluster[4]
        subjectApps = cluster[5]
        expApps = cluster[6]
        clusterNameSplit = (subjectApi.split("."))
        clusterName = (clusterNameSplit[1])
        
        expApiFormat = datetime.datetime.strptime(expApi, '%b  %d %H:%M:%S %Y GMT')
        expAppsFormat = datetime.datetime.strptime(expApps, '%b  %d %H:%M:%S %Y GMT')
        expApiStat = expValidation(expApiFormat)
        expAppsStat = expValidation(expAppsFormat)
        

        my_object = {"event":{"event_type": "certificates-status", "cluster": clusterName, "subject_name_api": subjectApi, "issued_by_api": issuerApi, "certs_exp_api": str(expApiFormat), "certs_validation_apps": expApiStat, "subject_name_apps": subjectApps, "issued_by_apps": issuerApps, "certs_exp_apps": str(expAppsFormat), "certs_validation_api": expAppsStat}}
        r = requests.post(splunk_url, json = my_object, auth=('Splunk', splunk_token), verify=False)
        print(r)

def expValidation(certs_exp):
    today = datetime.datetime.now()
    d = datetime.timedelta(days = days_calculate)
    delta = certs_exp - d
    if  delta <= today and today < certs_exp:
        return('About To Expire')
    if certs_exp <= today:
        return('Expired')
    else:
        return('Valid')
    
def main():
    getCertsInfo()


if __name__ == '__main__':
    main()
