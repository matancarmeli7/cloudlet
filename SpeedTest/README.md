# Speed Test 

This repository contains 4 applications, for the purpose of testing the speed of the link between the cloudlets and the IDFCTS cloud.

---
### download-cloud-app 
##### Overview
This is the server part of the download speed test, which runs on the Cloud. It exposes files.   
  
##### Requirements:
1. A python alpine image
  
##### Variables
You should update the following variables to deploy this app using Helm:
- OPENSHIFT_URL: The wildcard of the OpenShift, to use for creation of the route
- PORT: The port to expose the app on
- IMAGE_NAME: The name of the image

---		
### download-cloudlet-app 
##### Overview  
This is the client of the download speed test, which will be deployed using argocd on each cloudlet. The information about the speed of the download will be sent from here.  
  
##### Requirements
1. A python alpine image
2. The following python packages, dependencies of requests and schedule:  
&nbsp;&nbsp;- requests >= 2.23.0  
&nbsp;&nbsp;- schedule >=0.6.0  
&nbsp;&nbsp;- certifi >=2017.4.17  
&nbsp;&nbsp;- chardet >=2.5,<3  
&nbsp;&nbsp;- urllib3 >=1.21.1,<1.26,  
 
##### Variables
You should update the following variables to deploy this app using Helm:
- MAIN_APP_URL: The URL of the main up, which exposes the files
- SPLUNK_TOKEN: The HEC token for the index to which the test results should be sent
- SPLUNK_URL: The splunk url (should be a url for the indexers)
- MIN_CHECK_TIME: The minimum amount of seconds after which a test is considered legitimate (DEFAULT: 2)
- OCP_NAME: The name of the OpenShift this app is deployed one. **Will be dynamically assigned in future version**
- IMAGE_NAME: The name of the image
---
### 3. upload-cloud-app
##### Overview  
This is the server part of the upload speed test, which runs on the Cloud. It listens indefinitely to connecitons. It records the speed of each connection and sends the data to Splunk. This server should be deployed on a dedicated AppNode, which will be exposed using 
a NodePort or ExternalIp. The python client can only connect to the server using an IP address, and if you try to expose the server
using a regular OpenShift route, the DNS will be resolved to the IP of the OpenShift router, and the clients will not be able to connect.
  
##### Requirements
1. A python alpine image
2. The following python packages, dependencies of requests:  
&nbsp;&nbsp;- requests >= 2.23.0   
&nbsp;&nbsp;- certifi >=2017.4.17  
&nbsp;&nbsp;- chardet >=2.5,<3  
&nbsp;&nbsp;- urllib3 >=1.21.1,<1.26  

##### Variables
You should update the following variables to deploy this app using Helm:
- PORT: The port to expose the server on
- KB_CHUNKS: Amount of KB chunks to read in each iteration (DEFAULT: 16)
- SPLUNK_TOKEN: The HEC token for the index to which the test results should be sent
- SPLUNK_URL: The splunk url (should be a url for the indexers)
- IMAGE: The name of the image
- TESTS_PER_CLIENT: Amount of tests to perform before sending the results to Splunk (DEFAULT: 1)
- NODE_SELECTOR: The selector of the App nodes to deploy on (DEFAULT: node-port-exposed)

---
### 4. upload-cloudlet-app:  
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
