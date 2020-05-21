#!/usr/bin/env python3

import requests
import schedule
import time
def gatherdata():
    url = 'quay_url'
    token = 'quay_token'
    hed = {'Authorization': 'Bearer ' + token}
    x = requests.get(url, headers=hed, verify=False)
    return(x.json())

def senddata():
    mydata = gatherdata()
    url = 'splunk_url'
    myobj = {"event": {"event_type": "quaylogs", "cluster_name": "cluster_name", "data": mydata }}
    x = requests.post(url, json = myobj, auth=('Splunk', 'splunk_token'), verify=False)
schedule.every(3).minutes.do(senddata)
while True:
    schedule.run_pending()
