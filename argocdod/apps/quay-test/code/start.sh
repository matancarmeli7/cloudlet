#!/bin/bash
export KUBECONFIG=./kubeconfig
oc login https://api."$fqdn":6443 -u admin -p redhat --insecure-skip-tls-verify=true > /dev/null 2>&1
oc config view > kube
sed -i "s/fqdn/$fqdn/" nginx.yaml
