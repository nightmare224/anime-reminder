{{/*
Expand the name of the chart.
*/}}
{{- define "anime-reminder.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "anime-reminder.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "anime-reminder.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "anime-reminder.labels" -}}
helm.sh/chart: {{ include "anime-reminder.chart" . }}
{{ include "anime-reminder.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "anime-reminder.selectorLabels" -}}
app.kubernetes.io/name: {{ include "anime-reminder.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "anime-reminder.ui" -}}
  {{- printf "ar-ui" -}}
{{- end -}}

{{- define "anime-reminder.api" -}}
  {{- printf "ar-api" -}}
{{- end -}}

{{- define "anime-reminder.keycloak" -}}
  {{- printf "ar-keycloak" -}}
{{- end -}}

{{- define "anime-reminder.postgresql" -}}
  {{- printf "ar-postgresql" -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "anime-reminder.ui.serviceAccountName" -}}
{{- if .Values.ui.serviceAccount.create }}
{{- default (include "anime-reminder.ui" .) .Values.ui.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.ui.serviceAccount.name }}
{{- end }}
{{- end }}

{{- define "anime-reminder.api.serviceAccountName" -}}
{{- if .Values.api.serviceAccount.create }}
{{- default (include "anime-reminder.api" .) .Values.api.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.api.serviceAccount.name }}
{{- end }}
{{- end }}


{{- define "anime-reminder.keycloak.serviceAccountName" -}}
{{- if .Values.keycloak.serviceAccount.create }}
{{- default (include "anime-reminder.keycloak" .) .Values.keycloak.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.keycloak.serviceAccount.name }}
{{- end }}
{{- end }}
