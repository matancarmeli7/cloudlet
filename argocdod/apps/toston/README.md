<div> <p align="center"> <img src="https://i.imgur.com/5nOQztK.png"> </p> </div>

# toston
* This repository holds all the cloudlet tests.
* The toston is a helm chart that deploys your tests via yaml files, therefore all tests run as cronjobs.
* Prerequisites
    * Docker image set for the test
    * Roles defined in accurate and concise yaml files

## Deploying tests
* Add the required files to the repo (pod yaml and roles)
* Sync toston project in argocd on the right cluster.

## Recommendation
* Keep your code safe and clean - **Do not keep hardcoded creds in files!**
