# MinIOInstance Helm
## values.yaml
* ```Name``` - object name
* ```accessKey``` - access key for MinIO (like username)
* ```secretKey``` - secret key for MinIO (like password)
* ```replicas``` - number of replicas (recommened 4 minimum)
* ```image``` - image details
  * ```repository``` - image name
  * ```tag``` - image tag
* ```requests``` - pod requests
  * ```memory``` - memory requests
  * ```cpu``` - cpu requests
* ```port``` - port for the service
* ```disksize``` - size of each disk on each replica in Gi (must be more than 2)
## After deployment
The operator creates an amount of pvcs and containers as specified in the ```replicas``` parameter, and a Service to access them. </br>
You can access your MinIO instance via its service at the url **http://NAME-hl-svc:port**, for example: </br>
```http://s3-hl-svc:9000```
