**_Red Hat Quay deployment with Minio Storage Backend_**

Main goals of Quay

This document based on the next official Red Hat documentation links

[Accessing Red Hat Quay (formerly Quay Enterprise) without a CoreOS login](https://access.redhat.com/solutions/3533201)

[Deploy Red Hat Quay on OpenShift with Quay Setup Operator](https://access.redhat.com/documentation/en-us/red_hat_quay/3.3/html-single/deploy_red_hat_quay_on_openshift_with_quay_operator/index#registry_storage_backend_types)



[OpenShift Container Platform (OCP) 4 upgrade paths](https://access.redhat.com/solutions/4583231)

[Configuring the Samples Operator](https://docs.openshift.com/container-platform/4.2/openshift_images/configuring-samples-operator.html)


##
*1. Create namespace*

```

```

##
*2. Install Quay Operator*

Go to quay-enterprise namespace and operator hub, and install red hat quay operator

##
*3. Create secrets*
In your installer server create /root/.docker/config.json file with the next content
```
{
  "auths":{
    "quay.io": {
        "auth": "cmVkaGF0K3F1YXk6TzgxV1NIUlNKUjE0VUFaQks1NEdRSEpTMFAxVjRDTFdBSlYxWDJDNFNEN0tPNTlDUTlOM1JFMTI2MTJYVTFIUg==",
        "email": ""
    }
  }
}
```
Then run the command to create secret in Openshift --> Quay-enterprise namespace
```
oc create secret generic redhat-pull-secret --from-file=".dockerconfigjson=/root/.docker/config.json" --type='kubernetes.io/dockerconfigjson'
```
Secret for your quay user password
```
oc create secret generic quay-super-user --from-literal=superuser-username=quay --from-literal=superuser-password=r3dh4t1! --from-literal=superuser-email=quay@redhat.com
```
Secret for your quayconfig user
```
oc create secret generic quay-config-app --from-literal=config-app-password=r3dh4t1!
```
Secret for your database credentials
```
oc create secret generic quay-database-credential --from-literal=database-username=quay --from-literal=database-password=redhat --from-literal=database-root-password=r3dh4t1! --from-literal=database-name=quay
```
Secret for your redis password
```
oc create secret generic quay-redis-password --from-literal=password=r3dh4t1!
```
##
*4. Create your quayecosystem.yaml*
Create your quayecosystem.yaml and provide all your relevant customizations:
```
apiVersion: redhatcop.redhat.io/v1alpha1
kind: QuayEcosystem
metadata:
  name: prod-quayecosystem
  namespace: quay-enterprise
spec:
  clair:
    enabled: true
    imagePullSecretName: redhat-pull-secret
    updateInterval: "60m"
  redis:
    credentialsSecretName: quay-redis-password
    imagePullSecretName: redhat-pull-secret
  quay:
    deploymentStrategy: RollingUpdate
    superuserCredentialsSecretName: quay-super-user
    configSecretName: quay-config-app
    externalAccess:
      hostname: quay.apps.ocp43-prod.cloudlet-dev.com
    imagePullSecretName: redhat-pull-secret
    keepConfigDeployment: true
    registryBackends:
      - name: default
        rhocs:
          hostname: minio.apps.ocp43-prod.cloudlet-dev.com
          accessKey: minio
          secretKey: minio123
          bucketName: quay-enterprise
          storagePath: /storage/registry
    database:
      volumeSize: 10Gi
      credentialsSecretName: quay-database-credential
    skipSetup: false
```
