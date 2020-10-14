# app argo

Service that checks argocd runs as a cronjob in toston

1. Checks if url argo up

2. Checks if the cluster he is running from currently exists in his list of clusters

3. Check that the cluster is connected to the Argo

4. Check that the repo is connected to the Argo

if all this is correct he shows that the test passed successfully

if something in the way falls he presents the error relevant to what he failed at
