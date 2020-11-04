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
- SPLUNK_TOKEN: The HEC token for the index to which the test results should be sent.
- SPLUNK_URL: The splunk url (should be a url for the indexers).
- MIN_CHECK_TIME: The minimum amount of seconds after which a test is considered legitimate (DEFAULT: 2)
- OCP_NAME: The name of the OpenShift this app is deployed one. **Will be dynamically assigned in future version**
- IMAGE_NAME: The name of the image
