import requests
import schedule
import time
import json
import sys
sys.path.insert(1, '/argocd_to_splunk/src/config')
from config import *

def job():

    argoAuth = requests.post(argoUrl+authApi, json=login, verify=False)
    argo = requests.get(argoUrl+appsApi, cookies=argoAuth.cookies, verify=False)

    appsRes = json.loads(argo.content)
    for app in appsRes['items']:
        jsonSplunk = {"event":{"event_type":"argocd", "data": app }}
        r = requests.post(splunkUrl, headers=splunkAuth, json=jsonSplunk, verify=False)
        print(r.text)

schedule.every(1).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)


