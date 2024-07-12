# LOCAL FILE INCLUSION 
*Local File Inclusion (LFI)* is a security vulnerability found in web applications that allows attackers to include files on a server through the web browser.  
This can lead to various attacks, including data exposure, code execution, and escalation of privileges.  
There are two main types of LFI attacks:  
 
1. **Direct LFI** , where the attacker directly manipulates the URL or request parameters to include a file from the server's local filesystem.  
 
2. **Remote Code Execution via LFI** , where the attacker exploits the LFI vulnerability to execute code by including files that contain malicious code or sensitive information, potentially leading to full server compromise.  

LFI exploits typically target server files like configuration files, log files, and other sensitive information stored on the server.  
By exploiting LFI, an attacker can read these files and potentially gain further access to the system.  