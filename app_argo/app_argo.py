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

    if (r.status_code not in [503, 404]):
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
       print(app['server'])
       splitCluster = server.split(".")
       cluster_name = splitCluster[1]
       print(cluster_name)

       status = app['connectionState']['status']
       print(app['connectionState']['status'])

       jsonSplunk = {"event":{"event_type": "argo"  , "cluster": cluster_name, "status": status }}
       r = requests.post(splunkUrl, headers=splunkAuth, json=jsonSplunk, verify=False)
       print(r)


async def repojob():

    argo = requests.get(argoUrl + repoApi, cookies=argoAuth.cookies, verify=False)
    appsRes = json.loads(argo.content)
    for app in appsRes['items']:

      repo = app['repo']
      print(app['repo'])

      status = app['connectionState']['status']
      print(app['connectionState']['status'])

      jsonSplunk = {"event":{"event_type": "argo"  , "repositories": repo, "status": status }}
      r = requests.post(splunkUrl, headers=splunkAuth, json=jsonSplunk, verify=False)
      print(r)


async def main():

    await url_up('https://argocd-server-argocd.apps.np.cloudlet-dev.com')

if __name__ == '__main__':
    asyncio.run(main())
    asyncio.run(argoinf())
    asyncio.run(clusterjob())
    asyncio.run(repojob())

