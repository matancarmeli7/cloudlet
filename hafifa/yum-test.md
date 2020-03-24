# Package management
## 1. Setup Yum repository server
1. Provision a Linux server and download locally Ansible rpm files to it.
2. Setup with those rpm files a yum repository.
## 2.  Use the yum repository
1. Provision another Linux server and use it as a client server that will use this Yum repository.
2. Configure the client server to use the Yum repository that you created.
3. List all the versions of Ansible that you can download.
4. Download Ansible in any version that you want, use the Repository that you created.