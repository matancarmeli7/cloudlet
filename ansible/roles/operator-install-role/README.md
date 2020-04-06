## Install an Operator on an OCP cluster

Installing operators from the operator hub easily and automatically.

Default Vars -
namespace: openshift-operators	In this case the operator will be installed across all namespaces. Remember to check if it supports it..
channel: stable
source: redhat-operators
installPlan: Automatic

Mandatory Vars -
operator_name: [name]
