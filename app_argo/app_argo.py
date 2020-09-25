#!/usr/bin/env python3

import logging
import httpx
import asyncio
import requests
import sys
import urllib3
import json


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


sys.path.insert(1, '/app_argo/url_argo_up/config')
from config import *

global argoAuth
argoAuth = requests.post(argoUrl + authApi, json=login, verify=False)

async def url_up(url):
    logger = logging.getLogger()
    logger.setLevel('INFO')
    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s", "%H-%M-%S")
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)

    async with httpx.AsyncClient(verify=False) as client:
        try:
            r = await client.get(url)
        except Exception as e:
            logger.error(f"URLUPSTATUS:{url}:{e}")
            return False

    if (r.status_code==[503, 404]):
        logger.info(f"URLUPSTATUS:{url}:UP:STATUS_CODE={r.status_code}")
        return True
    else:
        logger.warning(f"URLUPSTATUS:{url}:DOWN:STATUS_CODE={r.status_code}")
        return False


async def argoinf():

    argoApi = 'api/v1/clusters/'
    x = requests.get(argoUrl + appsApi, cookies=argoAuth.cookies, verify=False)

    return(x.json())
     

async def clusterjob():

    argo = requests.get(argoUrl + appsApi, cookies=argoAuth.cookies, verify=False)
    appsRes = json.loads(argo.content)
    for app in appsRes['items']:

       server = app['server']
       splitCluster = server.split(".")
       Cluster_name = splitCluster[1]

       if Cluster_name=="p":
        print('Cluster', Cluster_name, 'found')
       else:
        print('Cluster', Cluster_name, 'not found','err')

       status = app['connectionState']['status']
       
       if status=="Successful":
        print('Cluster', Cluster_name, 'is Connected to argocd')
       else:
        print('Cluster', Cluster_name, 'is Disconnected to argocd','err')


async def repojob():

    argo = requests.get(argoUrl + repoApi, cookies=argoAuth.cookies, verify=False)
    appsRes = json.loads(argo.content)
    for app in appsRes['items']:

      repo = app['repo']
      status = app['connectionState']['status']

      if status=="Successful":
        print('repository', repo, ' is connected to argocd')
      else:
        print('repository', repo, 'is Disconnected to argocd', 'err')


async def main():

    await url_up('https://argocd.apps.np.cloudlet-dev.com')

if __name__ == '__main__':
    asyncio.run(main())
    asyncio.run(argoinf())
    asyncio.run(clusterjob())
    asyncio.run(repojob())

