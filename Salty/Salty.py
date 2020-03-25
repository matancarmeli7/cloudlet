import requests
import json

def main():

	# List of repositories to pull from central cloud
        repositories_to_pull = {}

	# Set local and remote Quay registries with basic api prefix
	local_reg_URL = "https://quay.io/api/v1"
        remote_req_URL = "https://quay.io/api/v1"

	# Get all repositories
	URL = "{}/repository".format(local_reg_URL)
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
		URL = "{}/repository/{}/{}".format(local_reg_URL, repository['namespace'], repository['name'])

		r = requests.get(url = URL, verify=False)
		response = r.json()

		data = json.loads(json.dumps(response))

		# Go over each tag in the repository and print each one with its full path and digest
		for tag in data['tags'].keys():
		    print "{}/{}:{} {}".format(repository['namespace'], repository['name'], data['tags'][tag]['name'], data['tags'][tag]['manifest_digest'])

                # Remember to pull this repository from the central cloud by namespace and repo name
                repositories_to_pull.add("/{}/{}".format(repository['namespace'], repository['name']))

	    else:
		pass # Helm Charts here

        # Get required repositories from central cloud
        for repository in repositories_to_pull:

             URL = "{}/repository/{}/{}".format(remote_reg_URL, repository['namespace'], repository['name'])
          
             r = requests.get(url = URL, verify=False)
             response = r.json()

             data = json.loads(json.dumps(response))

             # Go over each tag in the repository and print each one with its full path and digest
             for tag in data['tags'].keys():
                 print "{}/{}:{} {}".format(repository['namespace'], repository['name'], data['tags'][tag]['name'], data['tags'][tag]['manifest_digest'])
            

if __name__ == "__main__":
    main()
