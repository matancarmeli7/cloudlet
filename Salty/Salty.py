import requests
import json

# Set remote Quay registry with basic api prefix
BASEURL = "https://quay.io/api/v1"

# Get all repositories
URL = "{}/repository".format(BASEURL)
PAR = {
       'public':'true',
       'starred':'false'
      }

r = requests.get(url = URL, params = PAR, verify=False)
response = r.json()

data = json.loads(json.dumps(response))

# Go over each repository
for repository in data['repositories']:
    # Check if the repository is a Container Image Repository
    if repository['kind'] == 'image':

        # Get more infromation on each repository
        URL = "{}/repository/{}/{}".format(BASEURL, repository['namespace'], repository['name'])

        r = requests.get(url = URL, verify=False)
        response = r.json()

        data = json.loads(json.dumps(response))

        # Go over each tag in the repository and print each one with its full path and digest
        for tag in data['tags'].keys():
            print "{}/{}:{} {}".format(repository['namespace'], repository['name'], data['tags'][tag]['name'], data['tags'][tag]['manifest_digest'])

    else:
        pass # Helm Charts here
