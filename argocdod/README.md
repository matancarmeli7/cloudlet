# ArgoCDod
*	Deploying all of our default applications (Operators/Custom apps...) on a cluster using one central ArgoCD app.
*	This repository is based on ArgoCD's "App of Apps" methodology https://argoproj.github.io/argo-cd/operator-manual/cluster-bootstrapping/

## How to add an app to this repo
* Create a Helm chart/YAML for your app.

* Place your app in the ```apps``` folder.

* Create another Helm template defining your app as an ArgoCD application.
  * See full example - https://argoproj.github.io/argo-cd/operator-manual/application.yaml
  * Optional - add parameters to the repo's ```values.yaml``` if you need it for your app definition.

* Place your ArgoCD application definition in the ```templates``` folder. 

* Sync your app in ArgoCD (this step is needed if sync policy is manual).

## Deploying the main app example
**Notice the spec.destination.server parameter override inside spec.source.helm.parameters,** this handles to which cluster the apps are deployed. </br>
**DO NOT CHANGE the first spec.destination.server**, it should stay ```https://kubernetes.default.svc```.
```
apiVersion: argoproj.io/v1alpha1
metadata:
  name: argocdod-local
spec:
  destination:
    namespace: argocdod
    server: 'https://kubernetes.default.svc'
  source:
    path: argocdod
    repoURL: 'https://github.com/matancarmeli7/cloudlet'
    targetRevision: HEAD
    helm:
      parameters:
        - name: spec.destination.server
          value: https://kubernetes.default.svc
      valueFiles:
        - values.yaml
  project: argocdod
  syncPolicy: null
```
