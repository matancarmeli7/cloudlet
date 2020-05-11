###  upload-cloudlet-app:  
##### Overview  
This is the client of the upload speed test, which will be deployed using argocd on each cloudlet.  
  
##### Requirements
1. A python alpine image
2. The following python package: schedule >= 0.6.0
  
##### Variables
You should update the following variables to deploy this app using Helm:
- UPLOAD_HOST: The **ip address** of the upload server app. This requires the usage of NodePorts or External IPs, and not OpenShift
regular routes. 
- PORT: The port the server is exposed on
- TEST_LENGTH: The length of each up load test, in seconds (DEFAULT: 5)
- TESTS_AMOUNT: The amounts of test to perform in each iteration (DEFAULT: 1)
- TESTS_INTERVAL: The interval (in minutes) between tests (DEFAULT: 2)
- KB_CHUNKS: The amout of KB chunks to send in each message (DEFAULT: 500)
- IMAGE_NAME: The name of the image
- OCP_NAME: The name of the OpenShift this app is deployed one. **Will be dynamically assigned in future version**
