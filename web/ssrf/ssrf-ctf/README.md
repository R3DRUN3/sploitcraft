# SSRF CTF

PoC implementation of a SSRF-based web Capture the Flag.  



## Challenge Description
**This website is currently under construction but can reach other internal webservices on the same host, are you able to find the flag?**  




## Instructions
Build the container with the following command:  
```sh
docker build -t ssrf-pivot-challenge .
```  

Run the ctf environment with the following command:  
```sh
docker run -d -p 80:80 ssrf-pivot-challenge
```  

Go to *http://localhost* and try to find the flag!!  

**If you are stuck, follow the [walkthrough](./walkthrough/README.md)**.  



