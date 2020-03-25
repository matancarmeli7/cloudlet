
# Linux

## Prerequisites:
1.	A Linux machine that you can SSH into and connect to its console when the network is misconfigured.

## 1. Background
1. Add the following abilities to the ```history``` command **for the root user only**:
	* Date will be shown next to each command.
	* The commands `ls`,`pwd`,`top` will never be shown.
	* Consecutive duplicates will be shown once.
2.  Run the following command: ```exec top``` in your terminal and after a bit press ```q```.
     **What happened? Why?**

## 2. Boot Process
1. Using the console, change root's password **as if u don't already know it**.
> **Understand what you did, it isn't worth much just following the guide you found in Google.**	
## 3. Time management
1. Configure your machine's clock so it synchronizes against the organization's NTP servers.
	* Use ```chrony```.
## 4. Package management

1. Download ```Ansible``` rpms locally to your server.
2. Setup a ```YUM``` repository with those rpms.
3. Provision another Linux server and configure it to use the ```YUM``` repository that you just created.
4. List all the versions of ```Ansible``` that you can download.
5. Download ```Ansible``` in any version that you want, using the repository that you created.

## 5. Logs
1. Choose a word that you like.
2. From now on, every log in the system that contains your word should be sent to the file ```/var/log/theweeknd.log```. 
> Hint: ```rsyslog```
3. Find a way to create logs and make sure they show up in the file. 

## 6. LVM
1. Add a 1GB disk to your server.
2. Using LVM, create a filesystem of type ```XFS``` from your disk and mount it on ```/stromae```, afterwards make it so that the filesystem is mounted automatically on system boot.
> Make sure you mounted the filesystem properly using ```df -h```.
3. Add another 1GB disk to your server and extend the new filesystem's underlying LV with it.
	* Run ```df -h``` and see if your filesystem is now 2GB. If not - understand why it happened and fix it.
	* 
## 7. Virtual filesystems
1. Find out what is the size of ```/proc``` and ```/sys```.
	* Why is that so?
	* What do these filesystems do?	

## 8. Key management
1. Make the following command work **without it requesting a password** - ```ssh root@localhost```.
	* Read about ```ssh-copy-id``` and use it.
2. Make it that you can SSH to your machine using your SSH client(e.g ```PuTTY```) as root **without it requesting a password**.

## 9. Bash scripting
Write a script in BASH that gets a **UID as input** and prints the following about the user:
- Username
- Home folder
- Default shell
- Groups (including GID)
- Last 10 times he logged in to the server

The script should run in a loop untill STEPHANE_LEGAR is passed as input.
If the UID does not match any user in the system the script should output ```"a user with this uid does not exist, try again"```.

## 10. Kickstart
```
Ask if relevant
```


>  ### Good Luck! :poop: :poop: :poop:
> ### Created by Matan and Ori :smile::alien::basketball::yum::gun::hocho::boom: 
> &copy; Cloudlet 2020
