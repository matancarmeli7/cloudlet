{{- define "cluster_name" -}}
{{- $matches := split "." ( .Values.spec.destination.server | toString ) -}}
{{- $matches._1 -}}
{{- end -}}

{{- define "cluster_fqdntemp" -}}
{{- $matches := split "api." ( .Values.spec.destination.server | toString ) -}}
{{- $matches -}}
{{- end -}}

{{- define "cluster_fqdn" -}}
{{- $matches := split ":" ( .Values.cluster_fqdntemp | toString ) -}}
{{- $matches._0 -}}
{{- end -}}
