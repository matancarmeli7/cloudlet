#!/usr/bin/env python3

import requests
import schedule
import time
def gatherdata():
    url = 'https://quayecosystem-quay-quay-enterprise.apps.ocp43-prod.sales.lab.tlv.redhat.com/api/v1/superuser/logs'
    token = 'ieeVPVGwUsC8YVJAcM9ECA9zBn4SeRCPoYogmDet'
    hed = {'Authorization': 'Bearer ' + token}
    x = requests.get(url, headers=hed, verify=False)
    return(x.json())

def senddata():
    mydata = gatherdata()
    url = 'https://13.90.23.80:8088/services/collector/event'
    myobj = {"event": {"event_type": "quaylogs", "cluster_name": "offline", "data": mydata }}
    x = requests.post(url, json = myobj, auth=('Splunk', '6e5af836-9581-45b8-bcab-820bd9f7398e'), verify=False)
schedule.every(3).minutes.do(senddata)
while True:
    schedule.run_pending()
