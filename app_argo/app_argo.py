#!/usr/bin/env python3

import logging
import httpx
import asyncio
import requests
import sys
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.insert(1, '/app_argo/config')
from config import *

global argoAuth
argoAuth = requests.post(argoUrl + authApi, json=login, verify=verifySSl)

def url_up(url):
    logger = logging.getLogger()
    logger.setLevel('INFO')
    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s", "%H-%M-%S")
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    try:
        r = requests.get(url + appsApi, cookies=argoAuth.cookies, verify=verifySSl)
        if (r.status_code != 200):
       # logger.info(f"URLUPSTATUS:{url}:UP:STATUS_CODE={r.status_code}")
            raise Exception

    except:
       # logger.warning(f"URLUPSTATUS:{url}:DOWN:STATUS_CODE={r.status_code}")
        print('Argo is Down')
        sys.exit(1)
        return False
    return True

def clusterjob():
    argo = requests.get(argoUrl + appsApi, cookies=argoAuth.cookies, verify=verifySSl)
    appsRes = json.loads(argo.content)
    for app in appsRes['items']:

       server = app['server']
       splitCluster = server.split(".")
       Cluster_name = splitCluster[1]
       status = app['connectionState']['status']
       if Cluster_name==cluster_name:
         if status!="Successful":
           print("cluster no connected", 'err')
           sys.exit(1)
           return False
         elif (status=="Successful"):
            return True

    print("cluster not found", 'err')
    sys.exit(1)


def repojob():

    argo = requests.get(argoUrl + repoApi, cookies=argoAuth.cookies, verify=verifySSl)
    appsRes = json.loads(argo.content)
    for app in appsRes['items']:

      repo = app['repo']
      status = app['connectionState']['status']
      if status != "Successful":
          print("repo no connected", 'err')
          sys.exit(1)
      break

def main(url):

     url_up(url)
     clusterjob()
     repojob()
     print('Test Successful')
     sys.exit(0)

if __name__ == '__main__':
    (main(url))
