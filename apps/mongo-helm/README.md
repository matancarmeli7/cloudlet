# MongoDB Helm
## Prerequisites
Create a new organization in the opsmanager UI.
In the new organization, go to the Access tab in the left corner of the page. Create a new API key, grant it sufficient permissions ( such as Organization Owner), Whitelist 10.130.0.0/23 IP. Take note of the privatekey as you wont be able to see it later. After finishing these requirements you can fill your ```values.yaml```.

## values.yaml
* ```namespace``` - namespace to deploy instance
* ```apiPublicKey``` - api public key (created in Prerequisites)
* ```apiPrivateKey``` - api private key (created in Prerequisites)
* ```replicaset``` - replicaset details
  * ```name``` - name
  * ```members``` - amount of replicas that should be created
  * ```version``` - db version
  * ```persistent``` - should it be persistent with pvs (true/false)

## After deployment
You should see your database in the opsmanager UI, under your organization in a new project.
