oc process -f cloudlet/rh-sso-with-db/vanilla/sso74-x509-postgresql-external.yaml \
 -p SSO_ADMIN_USERNAME="admin" \
 -p SSO_ADMIN_PASSWORD="redhat" \
 -p SSO_REALM="demorealm" \
 -p PG_STORAGE_CLASS="managed-premium" | oc create -f -
