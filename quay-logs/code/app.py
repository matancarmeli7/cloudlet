import requests
import schedule
import time
import urllib3
import json
import re
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.insert(1, '/quay-logs/src/config')
from config import *

def repolist():

    url = quay_repo + '/api/v1/find/repositories'
    token = quay_token
    hed = {'Authorization': 'Bearer ' + token}
    x = requests.get(url, headers=hed, verify=False)
    return(x.json())


def senddata():

    myrepo = repolist()
    splunk_url = splunk_event_url
    for repo in myrepo['results']:
        reponame = repo['href']
        url = quay_repo + '/api/v1' + reponame
        token = quay_token
        hed = {'Authorization': 'Bearer ' + token}
        my_tags =  requests.get(url, headers=hed, verify=False)
        my_image =  requests.get(url + '/mirror', headers=hed, verify=False)
        my_image_json = my_image.json()
        my_tags_json = my_tags.json()
        for data in my_tags_json['tags']:
            image = my_image_json['external_reference']
            regex = re.search('[^\/]+$', image)
            myobj = {"event":{"event_type": "quaylogs", "cluster": cluster_name, "organization": repo['namespace']['name'],"repository": repo['name'], "image": regex.group(), "image_tag": data, "data": my_image_json }}
            r = requests.post(splunk_url, json = myobj, auth=('Splunk', splunk_token), verify=False)
            print(r)

schedule.every(3).minutes.do(senddata)
while True:
    schedule.run_pending()
