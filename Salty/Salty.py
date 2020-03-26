import requests
import json
import re

def getReqtoDict(URL, VERIFY, TOKEN, PARMS = None):
    authorization = "Bearer {}".format(TOKEN)
    HEADERS = {'content-type': 'application/json', 'Authorization': authorization}
    r = requests.get(url = URL, params = PARMS, verify=VERIFY, headers=HEADERS)
    response = r.json()

    return json.loads(json.dumps(response))

def getRepoTags():
    pass

def differencesInDicts(first, second):
    unmatchedKeys = []
    sharedKeys = set(first.keys()).intersection(second.keys())
    for key in sharedKeys:
        if first[key] != second[key]:
	    unmatchedKeys.append(key)
    return unmatchedKeys

def main():

	# Dictionaries of registries digest
	local_digests = {}
        remote_digests = {}

	# List of repositories to pull from central cloud
        repos_to_pull = set()

	# Set local and remote Quay registries with basic api prefix
	local_reg_URL = "https://quayecosystem-quay-quay-enterprise.apps.ocp43-prod.cloudlet-dev.com/api/v1"
        remote_reg_URL = "https://quay.io/api/v1"

        # Path to trusted certificates        
        VERIFY = '/etc/pki/tls/certs/ca-bundle.crt'

	# Tokens used to authenticate to the registries
        local_TOKEN = "YUAua36BQy2Y8vSHHlBL7tOyfRank0I1Lc5H2fx4"
        remote_TOKEN = "86bh0B1hiEgD8wL1YkRVCRCUJcT3cDK6wGSu4WgM"

	# Get all repositories from local regitsry
	URL = "{}/repository".format(local_reg_URL)
	PARMS = {
	       'public':'true',
	       'starred':'false'
	      }

	data = getReqtoDict(URL, VERIFY, local_TOKEN, PARMS = PARMS)
	
	# Go over each repository
	for repository in data['repositories']:
	    # Check if the repository is a Container Image Repository
	    if repository['kind'] == 'image':

                # Get more infromation on the repository
		URL = "{}/repository/{}/{}".format(local_reg_URL, repository['namespace'], repository['name'])

		data = getReqtoDict(URL, VERIFY, local_TOKEN)
		
		# Go over each tag in the repository and save each one with its full path and digest
		for tag in data['tags'].keys():
                    local_digests["{}/{}:{}".format(repository['namespace'], repository['name'], data['tags'][tag]['name'])] = data['tags'][tag]['manifest_digest']
                    

                # Remember to pull this repository from the central cloud by namespace and repo name
                repos_to_pull.add("{}/{}".format(repository['namespace'], repository['name']))	


	    else:
		pass # Helm Charts here

        # Get required repositories from central cloud
	# Go over each repository
        for repository in repos_to_pull:

	     # Get more infromation on the repository
             URL = "{}/repository/{}".format(remote_reg_URL, repository)
             
             data = getReqtoDict(URL, VERIFY, remote_TOKEN)
	     
             # Go over each tag in the repository and save each one with its full path and digest
             for tag in data['tags'].keys():
                 remote_digests["{}:{}".format(repository, data['tags'][tag]['name'])] = data['tags'][tag]['manifest_digest']

	# Print local tag that has a diffrenet digest then the central cloud
	unmatchedKeys = differencesInDicts(local_digests, remote_digests)
        if unmatchedKeys:
           print unmatchedKeys

if __name__ == "__main__":
    main()
