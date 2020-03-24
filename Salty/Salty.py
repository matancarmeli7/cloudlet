import requests
import json

BASEURL = "https://quay.io/api/v1"
#URL = "https://quayecosystem-quay-quay-enterprise.apps.ocp43-prod.cloudlet-dev.com/api/v1/repository"
URL = "https://quay.io/api/v1/repository"
PAR = {
       'public':'true',
       'starred':'false'
      }

r = requests.get(url = URL, params = PAR, verify=False)
response = r.json()

data = json.loads(json.dumps(response))

for object in data['repositories']:
    if object['kind'] == 'image':

#        print object['namespace'] + object['name']

        URL = "{}/repository/{}/{}".format(BASEURL, object['namespace'], object['name'])

        r = requests.get(url = URL, verify=False)
        response = r.json()

        data = json.loads(json.dumps(response))
        print data['tags']

    else:
        pass # Helm Charts here
