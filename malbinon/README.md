docker run -d -p 555:80 -e "HOST_IP=malbinon.cloudlet-dev.com" -e "REDHAT_USER=hayom" -e "REDHAT_PASSWORD=purim" -v /var/run/docker.sock:/var/run/docker.sock --restart always --name malbinon malbinon:latest

if used behind a load balancer (HAProxy), make sure the timeout configured there is high enough for the operation to complete.
