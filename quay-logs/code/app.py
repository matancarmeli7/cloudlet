import requests
import time
import urllib3
import json
import re
import sys
import base64
from kubernetes import client, config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.insert(1, '/quaylogs/src/config')
from config import *

def quayToken():
    config.load_kube_config('kube')
    v1 = client.CoreV1Api()
    base64_data_json=v1.read_namespaced_secret('quay-token-secret', 'quay-enterprise')
    base64_data = base64_data_json.data['token']
    base64_bytes = base64_data.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    data_decode = message_bytes.decode('ascii')
    return(data_decode)

def repolist(quay_token):

    url = quay_repo + '/api/v1/find/repositories'
    hed = {'Authorization': 'Bearer ' + quay_token}
    x = requests.get(url, headers=hed, verify=False)
    return(x.json())


def senddata():
    
    quay_token = quayToken()
    myrepo = repolist(quay_token)
    splunk_url = splunk_event_url
    for repo in myrepo['results']:
        reponame = repo['href']
        url = quay_repo + '/api/v1' + reponame
        hed = {'Authorization': 'Bearer ' + quay_token}
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

senddata()
