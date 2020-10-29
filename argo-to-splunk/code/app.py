import requests
import schedule
import time
import json
import sys
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.insert(1, '/argocd_to_splunk/src/config')
from config import *

global argoAuth
global Image_name
authApi = '/api/v1/session'
argoAuth = requests.post(argoUrl + authApi, json={"username": "admin", "password": "redhat"}, verify=False)

def argoinf(app_name):

    manifestsApi = '/api/v1/applications/' + app_name + '/manifests'
    x = requests.get(argoUrl + manifestsApi, cookies=argoAuth.cookies, verify=False)
    return(x.json())

def getImage(app_name):

    manifestsRes = argoinf(app_name)
    if "error" in manifestsRes:
        return("No Manifest")
    for data in manifestsRes['manifests']:
        loadData = json.loads(data)
        try:
            if loadData['kind']=="Deployment" or loadData['kind']=="DeploymentConfig":
                return(loadData['spec']['template']['spec']['containers'][0]['image'])
        except Exception:
            pass

def job():

    appsApi = '/api/v1/applications'
    splunkAuth = {'Authorization': 'Splunk ' + splunkToken}
    argo = requests.get(argoUrl + appsApi, cookies=argoAuth.cookies, verify=False)
    appsRes = json.loads(argo.content)
    for app in appsRes['items']:
        name = app['metadata']['name']
        image_name = getImage(name)
        server = app['spec']['destination']['server']
        splitCluster = server.split(".")
        cluster_name = splitCluster[1]
        if image_name!="No Manifest" and type(image_name)==str:
            splitImage = image_name.split(":")
            image = splitImage[0]
            regex_image = re.search('[^\/]+$', image)
            tag = splitImage[1]
            jsonSplunk = {"event":{"event_type": "argocd", "data": app,"image": regex_image.group(), "image_tag": tag, "cluster": cluster_name}}
            r = requests.post(splunkUrl, headers=splunkAuth, json=jsonSplunk, verify=False)
            print(r)
        elif type(image_name)!=str or image_name=="No Image":
            jsonSplunk = {"event":{"event_type": "argocd", "data": app,"image": "No Image", "image_tag": "No Image", "cluster": cluster_name}}
            r = requests.post(splunkUrl, headers=splunkAuth, json=jsonSplunk, verify=False)
            print(r)
        else:
            jsonSplunk = {"event":{"event_type": "argocd", "data": app,"image": "No Manifest", "image_tag": "No Manifest", "cluster": cluster_name}}
            r = requests.post(splunkUrl, headers=splunkAuth, json=jsonSplunk, verify=False)
            print(r)

job()
