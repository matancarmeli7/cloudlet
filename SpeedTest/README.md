### Speed Test ###

This repository contains 4 applications, for the purpose of testing the speed of the link between the cloudlets and the IDFCTS cloud.

**1. download-cloud-app:**     
    This is the server part of the download speed test, which runs on the Cloud. It exposes files.   
**2. download-cloudlet-app:**   
    This is the client of the download speed test, which will be deployed using argocd on each cloudlet. The information about the speed of the download will be sent for here.    
**3. upload-cloud-app:**    
    This is the server part of the upload speed test, which runs on the Cloud. It listens indefinitely to connecitons. It records the speed of each connection and sends the data to Splunk.    
**4. upload-cloudlet-app:**    
    This is the client of the upload speed test, which will be deployed using argocd on each cloudlet.   
  
