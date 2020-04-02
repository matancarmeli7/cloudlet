# ArgoCDod
*	Deploying all of our default applications (Operators/Custom apps...) on a cluster using one central ArgoCD app.
*	This repository is based on ArgoCD's "App of Apps" methodology https://argoproj.github.io/argo-cd/operator-manual/cluster-bootstrapping/

## How to add an app to this repo
* Create a Helm chart/YAML for your app.

* Place your app in the ```apps``` folder.

* Create another Helm template defining your app as an ArgoCD application.
  * See full example - https://argoproj.github.io/argo-cd/operator-manual/application.yaml
  * Optional - add parameters to the repo's ```values.yaml``` if you need it for your app definition.
