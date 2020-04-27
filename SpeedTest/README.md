# Speed Test 

This repository contains 4 applications, for the purpose of testing the speed of the link between the cloudlets and the IDFCTS cloud.

---
### download-cloud-app 
##### Overview
This is the server part of the download speed test, which runs on the Cloud. It exposes files.   
##### Requirements:
1. A python alpine image

---		
### download-cloudlet-app 
##### Overview  
This is the client of the download speed test, which will be deployed using argocd on each cloudlet. The information about the speed of the download will be sent for here.  
  
##### Requirements
1. A python alpine image
2. The following python packages, dependencies of requests and schedule:  
&nbsp;&nbsp;- requests >= 2.23.0  
&nbsp;&nbsp;- schedule >=0.6.0  
&nbsp;&nbsp;- certifi >=2017.4.17  
&nbsp;&nbsp;- chardet >=2.5,<3  
&nbsp;&nbsp;- urllib3 >=1.21.1,<1.26,  
  
---
### 3. upload-cloud-app
##### Overview  
This is the server part of the upload speed test, which runs on the Cloud. It listens indefinitely to connecitons. It records the speed of each connection and sends the data to Splunk.    
  
##### Requirements
1. A python alpine image
2. The following python packages, dependencies of requests:
&nbsp;&nbsp;- requests >= 2.23.0
&nbsp;&nbsp;- certifi >=2017.4.17
&nbsp;&nbsp;- chardet >=2.5,<3
&nbsp;&nbsp;- urllib3 >=1.21.1,<1.26,

---
### 4. upload-cloudlet-app:  
##### Overview  
This is the client of the upload speed test, which will be deployed using argocd on each cloudlet.  
  
##### Requirements
1. A python alpine image
2. The following python package: schedule >= 0.6.0
  
