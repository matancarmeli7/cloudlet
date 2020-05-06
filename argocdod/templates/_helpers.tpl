{{- define "cluster_name" -}}
{{- $matches := split "." ( .Values.spec.destination.server | toString ) -}}
{{- $matches._1 -}}
{{- end -}}

{{- define "cluster_fqdn" -}}
{{- $matches := split "api." ( .Values.spec.destination.server | toString ) -}}
{{- $matches := split ":" $matches -}}
{{- $matches._0 -}}
{{- end -}}
