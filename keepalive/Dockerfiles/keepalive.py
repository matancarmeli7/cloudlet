#!/usr/bin/env python3

import requests
import schedule
import time
def keepalive():
    url = 'Url'
    myobj = {"event": {"event_type": "keepalive", "cluster_name": "Clustername"}}
    x = requests.post(url, json = myobj, auth=('Splunk', 'Token'), verify=False)
    print(x.text)
schedule.every(3).minutes.do(keepalive)
while True:
    schedule.run_pending()
