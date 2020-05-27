# APICast 

* An helm chart to deploy 3Scale APICast version 2.7
* The following values should be set:
  - THREE_SCALE_TOKEN: The token with which the APICast will connect to 3Scale (you should generate this token in the main 3Scale)
  - OPENSHIFT_URL: The OpenShift url of the main 3Scale
  - PROJ_NAME: The name of the projec you want the apicast to be created in
  - OC_WILDCARD: The wildcard of the OpenShift (for the route). Usually "apps.***.***..."
