**_Red Hat Quay deployment with Minio Storage Backend_**

Main goals of Quay

This document based on the next official Red Hat documentation links

[Accessing Red Hat Quay (formerly Quay Enterprise) without a CoreOS login](https://access.redhat.com/solutions/3533201)

[Deploy Red Hat Quay on OpenShift with Quay Setup Operator](https://access.redhat.com/documentation/en-us/red_hat_quay/3.3/html-single/deploy_red_hat_quay_on_openshift_with_quay_operator/index#registry_storage_backend_types)



[OpenShift Container Platform (OCP) 4 upgrade paths](https://access.redhat.com/solutions/4583231)

[Configuring the Samples Operator](https://docs.openshift.com/container-platform/4.2/openshift_images/configuring-samples-operator.html)


##
*1. Define your cluster upgrade path*

To upgrade your specific cluster to the latest minor version you don't need to perform upgrade path check, so you can jump directly to the next chapter.
But if you want to upgrade to the major version you need to know what is your cluster version upgrade path. 
To define it, perform the next:
```
# export CURRENT_VERSION=4.4.12
# export CHANNEL_NAME=stable-4.5
# curl -sH 'Accept:application/json' "https://api.openshift.com/api/upgrades_info/v1/graph?channel=${CHANNEL_NAME}" | jq -r --arg CURRENT_VERSION "${CURRENT_VERSION}" '. as $graph | $graph.nodes | map(.version=='\"$CURRENT_VERSION\"') | index(true) as $orig | $graph.edges | map(select(.[0] == $orig)[1]) | map($graph.nodes[.].version) | sort_by(.)'
OUTPUT
[]
```
It means you can't upgrade directly from existing version, 4.4.12, to any version in 4.5 major version, so next action is to define to what version inside 4.4 you can upgrade. For that, change your CHANNEL_NAME environment variable accordingly.
```
# export CHANNEL_NAME=stable-4.4
# curl -sH 'Accept:application/json' "https://api.openshift.com/api/upgrades_info/v1/graph?channel=${CHANNEL_NAME}" | jq -r --arg CURRENT_VERSION "${CURRENT_VERSION}" '. as $graph | $graph.nodes | map(.version=='\"$CURRENT_VERSION\"') | index(true) as $orig | $graph.edges | map(select(.[0] == $orig)[1]) | map($graph.nodes[.].version) | sort_by(.)'
OUTPUT
[
  "4.4.13"
]
```
Now you know that your next version for upgrade should be 4.4.13. And only after you will complet to upgrade to this latest minor version, you will repeat the steps above with CHANNEL_NAME=stable-4.5 to understand how to continue with upgrade path.

##
*2. Mirroring the OpenShift Container Platform image repository*

This step assume that you have external mirror registry and internal mirror registry ready with existing version repositories (It was required for your cluster deployment).
On your external mirror registry server (one that have connection to the Internet):
Set the required environment variables:
```
# export OCP_RELEASE=4.4.13
# export LOCAL_REGISTRY='registry.ocp43-prod.sales.lab.tlv.redhat.com:5000'
# export LOCAL_REPOSITORY='ocp4.4.13/openshift4.4.13'
# export PRODUCT_REPO='openshift-release-dev'
# cd /opt/registry/ (this is my base registry folder)
Check the content of the json file you prepared in deployment process that including your mirror registry.
