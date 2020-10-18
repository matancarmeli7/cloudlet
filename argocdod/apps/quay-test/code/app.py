import urllib3
from kubernetes import client, config
from os import path
import yaml
import sys
import requests
import datetime
import base64
sys.path.insert(1, '/quaytest/config')
from config import *

def create_user(quayUrl, quayAuth):
    create_user_api = '/api/v1/user/'
    jsonBody = {'username': 'quaytest', 'password': 'Aa123456'}
    try:
        x = requests.post(quayUrl + create_user_api, headers=quayAuth, json=jsonBody, verify=False)
        if(x.status_code!=200):
            raise Exception
    except:
        pass
    return(True)
        
def delete_user(quayUrl, quayAuth):
    delete_user_api = '/api/v1/user/'
    jsonBody = {'username': 'quaytest', 'password': 'Aa123456'}
    try:
        x = requests.delete(quayUrl + create_user_api, headers=quayAuth, json=jsonBody, verify=False)
    except:
        print("err")


def create_org(quayUrl, quayAuth):
    create_org_api = '/api/v1/organization/'
    jsonBody = {"name": "quaytest-org"}
    try:
        x = requests.post(quayUrl + create_org_api, headers=quayAuth, json=jsonBody, verify=False)
   # print(x)
        if(x.status_code!=201):
            raise Exception
    except:
        return(False)
    return(True)
def delete_org(quayUrl, quayAuth):
    delete_org_api = '/api/v1/organization/quaytest-org'
    jsonBody = {"name": "quaytest-org"}
    try:
        x = requests.delete(quayUrl + delete_org_api, headers=quayAuth, json=jsonBody, verify=False)
    except:
        print("err")


def give_permmisoins(quayUrl, quayAuth):
    give_permmisions_api = '/api/v1/organization/quaytest-org/team/owners/members/quaytest'
    try:
        x = requests.put(quayUrl + give_permmisions_api, headers=quayAuth, verify=False)
        if(x.status_code!=200):
            raise Exception
    except:
        return(False)
    return(True)

def create_robot_user(quayUrl, quayAuth):
    create_robot_user_api = '/api/v1/organization/quaytest-org/robots/quaytest'
    try:
        x = requests.put(quayUrl + create_robot_user_api, headers=quayAuth, verify=False)
        if(x.status_code!=201):
            raise Exception
    except:
        return(False)
    return(True)

def create_repo(quayUrl, quayAuth):
    create_repo_api = '/api/v1/repository'
    jsonBody = {"repo_kind": "image", "namespace": "quaytest-org", "visibility": "public", "repository": "nginx", "description": "test repo"}
    try:
        x = requests.post(quayUrl + create_repo_api, headers=quayAuth, json=jsonBody, verify=False)
        if(x.status_code!=201):
            raise Exception
    except:
        return(False)
    return(True)

def set_repo_mirror(quayUrl, quayAuth):
    set_repo_mirror_api = '/api/v1/repository/quaytest-org/nginx/changestate'
    jsonBody= {"state": "MIRROR"}
    try:
        x = requests.put(quayUrl + set_repo_mirror_api, headers=quayAuth, json=jsonBody, verify=False)
        if(x.status_code!=200):
            raise Exception
    except:
        return(False)
    return(True)

def config_mirroring(quayUrl, quayAuth, d):
    config_mirroring_api = '/api/v1/repository/quaytest-org/nginx/mirror'
    jsonBody = {"is_enabled": True, "external_registry_config": { "proxy": {"https_proxy": "","http_proxy": "", "no_proxy": "" }, "verify_tls": True }, "external_registry_username": "yakir32","external_reference": "docker.io/nginx","sync_start_date": d,"root_rule":{ "rule_kind": "tag_glob_csv", "rule_value": ["latest"]}, "external_registry_password": "Password123!@#", "sync_interval": 1, "robot_username": "quaytest-org+quaytest"}
 #   jsonBody = {"is_enabled": True, "external_registry_config": {"proxy": {"https_proxy": "", "http_proxy": "", "no_proxy": ""}, "verify_tls": True}, "external_registry_username": "ss", "external_reference": "docker.io/httpd", "sync_start_date": d, "root_rule": {"rule_kind": "tag_glob_csv", "rule_value": ["latest"]}, "external_registry_password": "dffdsfdfd", "sync_interval": "500", "robot_username": "quaytest-org+quaytest"}
    try:
        x = requests.post(quayUrl + config_mirroring_api, headers=quayAuth, json=jsonBody, verify=False)
        if(x.status_code!=201):
            raise Exception
    except:
        return(False)
    return(True)

def deploy():
    config.load_kube_config('kube')

    api = client.CustomObjectsApi()

    # it's my custom resource defined as Dict
    with open(path.join(path.dirname(__file__), "nginx.yaml")) as f:
        dep = yaml.safe_load(f)
        k8s_apps_v1 = client.AppsV1Api()
        try:
            resp = k8s_apps_v1.create_namespaced_deployment(
                    body=dep, namespace="default")
        except:
            return(False)
        return(True)
def delete_deployment():
    # Delete deploymenti
    config.load_kube_config('kube')
    k8s_apps_v1 = client.AppsV1Api()
    api_response = k8s_apps_v1.delete_namespaced_deployment(
        name='nginx-deployment',
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
def check_pod():
    config.load_kube_config('kube')
    v1 = client.CoreV1Api()
    ret=v1.list_namespaced_pod('default')
#    print(ret.items[0].status.container_statuses[0].state.waiting.reason)
    while(ret.items[0].status.phase!="Running"):
        for i in ret.items:
            try:
                ms=i.status.container_statuses[0].state.waiting.message
#                    print(i.status.container_statuses[0].state.waiting)
 #                   return(False)
  #              elif(i.status.phase=="Running"):
   #                 return(True)
    #            raise Exception
            except:
                if(i.status.phase=="Running"):
                    print("ok")
                    return(True)
                print("conn err")
                return(False)
            if(ms!=None):
                if("Pulling" not in ms and "manifest" not in ms and "Back-off" not in ms):
                    print(ms)
                    return(False)
            ret=v1.list_namespaced_pod('default')
           # if(i.status.phase=="Running"):
            #     return(True)
                #print("err")
                #return(False)
    return(True)



def main():
   urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
   d = datetime.datetime.now()
   da=d.strftime("%Y-%m-%dT%H:%M:%SZ")
   #quay_url='https://quay.apps.ocp43-np.cloudlet-dev.com'
   quay_url=quay_url_conf
   config.load_kube_config('kube')
   v1 = client.CoreV1Api()
   base64_message_json=v1.read_namespaced_secret('quay-token-secret', 'quay-enterprise')
   base64_message = base64_message_json.data['token']
   base64_bytes = base64_message.encode('ascii')
   message_bytes = base64.b64decode(base64_bytes)
   token = message_bytes.decode('ascii')
   quay_auth={'Authorization': 'Bearer ' + token}
   #quay_auth=quay_auth_conf

   if(not create_user(quay_url, quay_auth)):
       print("failed create user")
       return(1)
  
   if(not create_org(quay_url, quay_auth)):
       print("failed create organization")
       return(1)
  
   if(not give_permmisoins(quay_url, quay_auth)):
       delete_org(quay_url, quay_auth)
       print("failed give permmisions")
       return(1)
  
   if(not create_robot_user(quay_url, quay_auth)):
       delete_org(quay_url, quay_auth)
       print("failed  to create robot user")
       return(1)

   if(not create_repo(quay_url, quay_auth)):
       delete_org(quay_url, quay_auth)
       print("failed to create repository")
       return(1)
  
   if(not set_repo_mirror(quay_url, quay_auth)):
       delete_org(quay_url, quay_auth)
       print("failed to mirror state")
       return(1)
  
   if(not config_mirroring(quay_url, quay_auth, da)):
       delete_org(quay_url, quay_auth)
       print("failed to configure mirroring")
       return(1)

   if(not deploy()):
       delete_org(quay_url, quay_auth)
       print("deploy failed")
       delete_deployment()
       return(1)

   if(not check_pod()):
       delete_org(quay_url, quay_auth)
       delete_deployment()
       return(1)
   
   delete_org(quay_url, quay_auth)
   delete_deployment()
   
   print("success")
   return(0)
       

if __name__ == '__main__':
    exitcode=main()
    sys.exit(exitcode)


