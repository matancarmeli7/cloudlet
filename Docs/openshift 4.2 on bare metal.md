# openshift 4.2 on bare metal

Follow the next instructions for installing openshift 4.2 on bare metal:

Prerequisites:

1. Open firewall ports for master, installer and bootstrap servers. Look for openshift full documentation.
2. Make sure that the destination addresses are in the correct vlan.
3. Deploy the installer server and copy to it the openshift-install and oc client binaries.
4. Install httpd installer server.
5. Issue certificates for your cluster(add doc link).
6. Create dns records.

Installation:

1. Use the install-config.yaml on bare metal template. (add link to template).
2. Create ssh-key with the next command: (command for ssh key), and add to ssh agent.
3. Edit the next fields in the install-config:
- base domain
- name
- ssh-key
- certificates (if needed)
4. Create a directory and copy the install-config to it. save a backup copy outside your install directory.
5. Run openshift-install command for creating manifests.(add manifests command)
6. Run openshift-install command for creating ignition files.(add ignition command)
7. Copy the master.ign to your httpd directory.
8. Now for the bootstrap.ign there are two possibilities:
  - If you use bare metal bootstrap just put bootstrap.ign file in httpd directory.
  - If you use bootstrap vm you can base64(base64 -w0 < bootstrap.ign > bootstrap.64) your ignition file and we can use it later. Or use an append file - this file will tell RHCOS where to download the bootstrap.ign file to configure itself for the OpenShift cluster.(link for append template ).
9. Now you need to install the bootstrap server:
  a. Bare metal - you need the installer iso file and the uefi\bios installation file. Boot The server from the installer iso file and press tab to insert the parameters for rhcos, here is an example config:
  ip=192.168.1.116::192.168.1.1:255.255.255.0:bootstrap.openshift4.example.com:ens192:none
  nameserver=192.168.1.2
  coreos.inst.install_dev=sda
  coreos.inst.image_url=http://192.168.1.110:8080/install/bios.raw.gz
  coreos.inst.ignition_url=http://192.168.1.110:8080/ignition/append-bootstrap.ign
  b. For vm bootstrap look for anoel documentation.
10. After bootstrap is up do the same bare metal installation for master server.
11. If you did everything ok you should have a running cluster after 30m top. In the installer server run the openshift-install wait for bootstrap complete command and you can see the progress there. From this point just follow anoel documentation.
