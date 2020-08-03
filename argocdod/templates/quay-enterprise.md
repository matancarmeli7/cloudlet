# This yaml is for Quay project deployment - please don't us it for now


apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: quay-enterprise-{{ template "cluster_name" . }}
  namespace: {{ .Values.argocdNamespace }}
spec:
  destination:
    namespace: {{ .Values.spec.destination.namespace }}
    server: {{ .Values.spec.destination.server }}
  project: {{ .Values.spec.project }}
  source:
    path: argocdod/apps/quay-enterprise
    repoURL: {{ .Values.spec.source.repoURL }}
    targetRevision: {{ .Values.spec.source.targetRevision }}
    helm:
      valueFiles:
        - values.yaml
