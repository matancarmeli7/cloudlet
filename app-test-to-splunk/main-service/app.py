import requests
import schedule
import time
import urllib3
import json
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.insert(1, '/app-test-to-splunk/src/config')
from config import *

hed = {'Authorization': 'Splunk ' +  splunkToken}

def runServiceTest():

    for route in servicesRoutes:
        appName = getAppName(route)
        runTest = requests.get(route , verify=False)
        jsonBody = {"event":{"event_type": "app-test-to-splunk", "app": appName, "cluster": clusterName, "message": runTest.text}}
        r = requests.post(splunkUrl, headers=hed, json=jsonBody, verify=False)
        print(r)

def getAppName(route):
    splitRoute = route.split("/")
    return(splitRoute[-2])

schedule.every(1).hour.do(runServiceTest)
while 1:
    schedule.run_pending()
    time.sleep(1)
