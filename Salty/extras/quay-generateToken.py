import requests
import json
import re

API_ENDPOINT = "https://quayecosystem-quay-quay-enterprise.apps.ocp43-offline.sales.lab.tlv.redhat.com/oauth/authorizeapp"

data = {'client_id':'CIZP1IQMXMIQEN8O43NB', 
        'redirect_uri':'', 
        'scope':'org:admin,repo:admin,repo:create,repo:read,repo:write,super:user,user:admin,user:read'}

AUTH = "Y2xvdWRsZXRfYWRtaW46UGFzc3dvcmRAMTIz" # echo -n "cloudlet_admin:Password@123" | base64
authorization = "Basic {}".format(AUTH)
HEADERS = {'content-type': 'application/json', 'Authorization': authorization}

r = requests.post(url = API_ENDPOINT, data = data, headers=HEADERS, verify=False) 

print r.text
print r
print r.json
