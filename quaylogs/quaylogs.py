#!/usr/bin/env python3

import requests
import schedule
import time
def repolist():
    url = 'quay_repo'
    token = 'quay_token'
    hed = {'Authorization': 'Bearer ' + token}
    x = requests.get(url, headers=hed, verify=False)
    return(x.json())	
	
	
def senddata():
    myrepo = repolist()
    splunk_url = 'splunk_event_url'
    for repo in myrepo['results']:
        reponame = repo['href']
        print (reponame)
        url = quay_mirror
        token = 'quay_token'
        hed = {'Authorization': 'Bearer ' + token}
        mydata = requests.get(url, headers=hed, verify=False)
        myobj = {"event":{"event_type": "quaylogs", "cluster": "prod", "organization": repo['namespace']['name'],"repository": repo['name'],"data": mydata.json() }}
        r = requests.post(splunk_url, json = myobj, auth=('Splunk', '6e5af836-9581-45b8-bcab-820bd9f7398e'), verify=False)
schedule.every(3).minutes.do(senddata)
while True:
    schedule.run_pending()
