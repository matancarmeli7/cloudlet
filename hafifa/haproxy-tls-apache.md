# HAProxy - TLS - Apache
> **Important notice!** 
> Stopping firewalld or disabling SELinux is a major crime that will result in a Saturday in the base.
> Be warned.
## Prerequisites:
#### Setup and implement the following servers:
1.	DNS Server
2.	Simple PKI - a custom ROOT CA with no SUB-CA's (use the DNS server).

## 1. Setup webservers
1. Provision 2 Linux machines - both need to use your DNS server and trust your ROOT CA, create a DNS A record for both.
2.  Install the web server software - one using **httpd** and the other **NGINX**.
3. Each of the servers should show the following pages, replace SERVER_HOSTNAME with the corresponding server's hostname:
	*	**On port 443**  - ```"Ori The Gever from port 443 SERVER_HOSTNAME"```
	*	**On port 8443** - ```"Matan The Gever from port 8443 SERVER_HOSTNAME" ```
	> **Notice the port numbers suggest you need to use TLS - for that matter create certificates signed by your ROOT CA for your webservers!!**
4. Check if it works by using ```curl``` between the   machines to request the webpages.
	*	For example ```curl https://web-01:443``` should respond with ```Ori The Gever from port 443 web-01```.
	*	Make sure it works without skipping certificate validation (i.e ```curl``` with the ```-k``` flag is not allowed).

## 2. Setup HAProxy
1. Provision another Linux machine - the machine shoud use your DNS server and trust your ROOT CA, create a DNS A record for it.
2. Install **HAProxy**.
3. Configure it so the following happens:
	* When a request hits the HAProxy on port 443 it forwards it to one of your webservers on port 443.
	* When a request hits the HAProxy on port 8443 it forwards it to one of your webservers on port 8443
	* HAProxy should forward the requests using round-robin.
	> **Once again -  the port numbers suggest you need to use TLS. For that matter create a certificate signed by your ROOT CA for your HAProxy server.**
4. Check if it works by using ```curl```  to request the webpage from the HAProxy.
	*	For example ```curl https://HAProxy:8443``` should respond with ```Matan The Gever from port 8443 web-02```.
	*	Make sure it works without skipping certificate validation (i.e ```curl``` with the ```-k``` flag is not allowed).
## 3. Wildcard certificates
1. Create 2 CNAME DNS records - ori.your.domain and matan.your.domain both referencing your HAProxy A Record.
2. Configure HAProxy so the following happens:
	* When a request hits https://ori.your.domain:5555 the HAProxy should forward the request to one of the webservers on port 443.
	* When a request hits https://matan.your.domain:5555 the HAProxy should forward the request to one of the webservers on port 8443.
	* > **Important -  although the port number isnt a typical HTTPS port you still need to use TLS. In addition - the HAProxy needs to use only 1 certificate to handle these requests. *Think wildcard*.**
3.	Check if it works by using ```curl```  to request the webpage from the HAProxy.
	*	For example ```curl https://ori.your.domain:5555``` should respond with ```Ori The Gever from port 443 web-02```.
	*	Make sure it works without skipping certificate validation (i.e ```curl``` with the ```-k``` flag is not allowed).
## 4. Keepalived
1. Setup another HAProxy server with the same configurations as the one you already set up.
2. Create keepalived between them so each time a different server responds.



## Notes
>  ### Good Luck! :poop: :poop: :poop:
> ### Created by Matan and Ori :smile::alien::basketball::yum::gun::hocho::boom: 
> &copy; Cloudlet 2020
