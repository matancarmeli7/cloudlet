
**_OCP 4.x Upgrade to Minor and Major Version in restricted networking environment_**

Main goals of updates/upgrades - bug fixes, new features, security vulnaribilities fixes, where ideal state is always be up to date.
Updates/upgrades can be done to the latest minor version of the existing current major version or to the next major version. 
For instance, if you deployed your cluster when the latest version was 4.4.12 you can upgrade it today to the latest minor 4.4.13 version 
or gradually to the latest existing version,i.e ocp 4.5.4.
In restricted networks this process includes additional steps of mirroring the relevant images in your existing private registry and changing 
configuration of several cluster components that will allow you to perform upgrade smoothly.

This document based on the next official Red Hat documentation links

[Updating a restricted network cluster](https://docs.openshift.com/container-platform/4.4/updating/updating-restricted-network-cluster.html)

[Updating a cluster between minor versions](https://docs.openshift.com/container-platform/4.3/updating/updating-cluster-between-minor.html)

[OpenShift Container Platform (OCP) 4 upgrade paths](https://access.redhat.com/solutions/4583231)

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
# For example, our one called pull-secret2.json
OUTPUT
cat pull-secret2.json | jq
{
  "auths": {
    "cloud.openshift.com": {
      "auth": "b3BlbnNoaWZ0LXJlbGVhc2UtZGV2K21hdGFuY2FybWVsaTk4MXF1eWZuYTlxdHlvZW03NHZyazdka3JtZHY3OjU0NFpBUVQzQldPTVpIRjFMOVpGT0ZHMFM5QTZOQkZPNE9IOEVLMjREUEhROVNCRUQ2OU9SNEdPSU5VQVJMSEU=",
      "email": "matan.carmeli7@gmail.com"
    },
    "quay.io": {
      "auth": "b3BlbnNoaWZ0LXJlbGVhc2UtZGV2K21hdGFuY2FybWVsaTk4MXF1eWZuYTlxdHlvZW03NHZyazdka3JtZHY3OjU0NFpBUVQzQldPTVpIRjFMOVpGT0ZHMFM5QTZOQkZPNE9IOEVLMjREUEhROVNCRUQ2OU9SNEdPSU5VQVJMSEU=",
      "email": "matan.carmeli7@gmail.com"
    },
    "registry.connect.redhat.com": {
      "auth": "NTI0Nzc2MDF8dWhjLTFRdXlGTkE5cVRZb2VtNzR2Uks3RGtSbWR2NzpleUpoYkdjaU9pSlNVelV4TWlKOS5leUp6ZFdJaU9pSXdabVUwT0dFNU1qUXhaRGswWlRjMU9XTXlPVFZqTmpVeFl6Rm1PRGN4TUNKOS5uaGpuaTVjTHpIazF0Z243Z0NNZVVSQXlIRjE4NFlpd0tDd2pBcG9UX1JqUjZfak5JREJJSlZkLWhWUE1KYVlKWFFLY1pvY1ZQZWVfWFplUzZjVmQ3QXRkZGVNTWdLNWtZd3ZtczFsVnQyc0wtMHYwTDZOZ0FXQk9nY1hNbW9EcVFSb2tDQjBnakd0ZFNDbjItbTlSVXVwTkpfblJOUGpYSW1kVDAwSkJNd3dHUWUyVy1VQ0hWSTRzN09yNktNQUdHOWxWT0VoZU1tMnctRGpoOEZmTERTTlZDX0dueDNNODB6YUl4ak9MbmlZTzNXZGFaZXZmUUtoREtvYWpwREM5V1pXNTlEQkxiYTQ0b1lQWlVpUFMxNVdLMlVUcVNzUmpJR2JpMHV0LWwxLTRONGNSVlZsNmZLdWd2YjhudWxJUGV6cnU4ZXJzc1JyOWlrWXhCODFYQXVNUFNBc0xseG1KVzJPY1M0bERyeUlZX3daRFpYZ1M5X2FEUkNkSWppTWRuejZ0SG5KcHVfamFvalpVUmhyVDJfUUZVSEQ4dUwwMG9RVnJiUFBKNGVybENPQnJnMkRId1hvOGV2MFRoT2x2allfa0Q5azhCLTJZc2xtMVdvdTNnMEp3LS1Ia0w0MXNfd3F4OENMVXQtaDFMMWhKNHdfV3cxZFpUdlBIS2t2OXcwS0JjM1BZY1dzNWF4SU5uZk1kMEE1WWF3NGNVQnJvRjFFV0gyMU5NSzV0V1NoMm5Oa0ZFdTNWZEduRVhuelZpYnJJNko4Y01SeWxUR1hYUGdnMDF4a0FOVDlJNjV4RGpKMTJWNmRac0o4bXVJYjhobzZma25mekxPNHNicW9hR2xGbGZiTmRJTDYwSlpQYWV6RUdaQXdBOTlCYk83NFdjU0stN25zU0ZWOA==",
      "email": "matan.carmeli7@gmail.com"
    },
    "registry.redhat.io": {
      "auth": "NTI0Nzc2MDF8dWhjLTFRdXlGTkE5cVRZb2VtNzR2Uks3RGtSbWR2NzpleUpoYkdjaU9pSlNVelV4TWlKOS5leUp6ZFdJaU9pSXdabVUwT0dFNU1qUXhaRGswWlRjMU9XTXlPVFZqTmpVeFl6Rm1PRGN4TUNKOS5uaGpuaTVjTHpIazF0Z243Z0NNZVVSQXlIRjE4NFlpd0tDd2pBcG9UX1JqUjZfak5JREJJSlZkLWhWUE1KYVlKWFFLY1pvY1ZQZWVfWFplUzZjVmQ3QXRkZGVNTWdLNWtZd3ZtczFsVnQyc0wtMHYwTDZOZ0FXQk9nY1hNbW9EcVFSb2tDQjBnakd0ZFNDbjItbTlSVXVwTkpfblJOUGpYSW1kVDAwSkJNd3dHUWUyVy1VQ0hWSTRzN09yNktNQUdHOWxWT0VoZU1tMnctRGpoOEZmTERTTlZDX0dueDNNODB6YUl4ak9MbmlZTzNXZGFaZXZmUUtoREtvYWpwREM5V1pXNTlEQkxiYTQ0b1lQWlVpUFMxNVdLMlVUcVNzUmpJR2JpMHV0LWwxLTRONGNSVlZsNmZLdWd2YjhudWxJUGV6cnU4ZXJzc1JyOWlrWXhCODFYQXVNUFNBc0xseG1KVzJPY1M0bERyeUlZX3daRFpYZ1M5X2FEUkNkSWppTWRuejZ0SG5KcHVfamFvalpVUmhyVDJfUUZVSEQ4dUwwMG9RVnJiUFBKNGVybENPQnJnMkRId1hvOGV2MFRoT2x2allfa0Q5azhCLTJZc2xtMVdvdTNnMEp3LS1Ia0w0MXNfd3F4OENMVXQtaDFMMWhKNHdfV3cxZFpUdlBIS2t2OXcwS0JjM1BZY1dzNWF4SU5uZk1kMEE1WWF3NGNVQnJvRjFFV0gyMU5NSzV0V1NoMm5Oa0ZFdTNWZEduRVhuelZpYnJJNko4Y01SeWxUR1hYUGdnMDF4a0FOVDlJNjV4RGpKMTJWNmRac0o4bXVJYjhobzZma25mekxPNHNicW9hR2xGbGZiTmRJTDYwSlpQYWV6RUdaQXdBOTlCYk83NFdjU0stN25zU0ZWOA==",
      "email": "matan.carmeli7@gmail.com"
    },
    "registry.ocp43-prod.sales.lab.tlv.redhat.com:5000": {
      "auth": "YWRtaW46cmVkaGF0"
    }
  }
}

# export LOCAL_SECRET_JSON="/opt/registry/pull-secret2.json"
# export RELEASE_NAME="ocp-release"
# podman login quay.io 
OUTPUT
Authenticating with existing credentials...
Existing credentials are valid. Already logged in to quay.io
# oc adm -a ${LOCAL_SECRET_JSON} release mirror --from=quay.io/${PRODUCT_REPO}/${RELEASE_NAME}:${OCP_RELEASE}-x86_64 --to=${LOCAL_REGISTRY}/${LOCAL_REPOSITORY} --to-release-image=${LOCAL_REGISTRY}/${LOCAL_REPOSITORY}:${OCP_RELEASE} | tee -a '/opt/registry/mirror-output${OCP_RELEASE}.txt'
OUTPUT
info: Mirroring 109 images to registry.ocp43-prod.sales.lab.tlv.redhat.com:5000/ocp4.4.13/openshift4.4.13 ...
```
Uploading to your external registry can take a while. After completing those steps you can tar you relevant blob folders (from the last day) and the relevant repository folder and move with this tar file to whitening process and after that extracting and adding to the relevant folders in your internal mirror registry.

##
*3. Edit your cluster ImageContentSourcePolicy*
Next steps will be performed from installer machine of your cluster
```
# oc get ImageContentSourcePolicy
# oc edit ImageContentSourcePolicy image-policy-0
Change ocp4.4.12/openshift4.4.12 to ocp4.4.13/openshift4.4.13 and save
# oc edit ImageContentSourcePolicy image-policy-1
Change ocp4.4.12/openshift4.4.12 to ocp4.4.13/openshift4.4.13 and save
```
##
*4. Upgrade your cluster to latest minor version*
Now you can go to your Ocp console --> Administration --> Cluster settings --> Details --> Update
This process will run in background and can take a while.
