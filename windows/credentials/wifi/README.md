# Stealing Windows Wi-Fi Passwords using PowerShell 

## Overview 
This repository contains a PowerShell script (`Get-WifiPasswords.ps1`) designed to retrieve clear text Wi-Fi passwords stored on Windows systems.  
This technique exploits the way Windows manages and stores Wi-Fi profiles.  

## How It Works 
Windows stores Wi-Fi profiles, including passwords, in a plaintext format in its configuration.  
These profiles can be accessed via administrative commands provided by `netsh`.  
The script utilizes these commands to gather Wi-Fi profile names and retrieve their associated passwords in clear text.  

### Key Steps: 
 
1. **Retrieve Wi-Fi Profiles** : The script first fetches all Wi-Fi profiles configured on the system using `netsh wlan show profiles`.  
 
2. **Extract Profile Names** : It then extracts the names of these profiles from the output using PowerShell's string manipulation capabilities.  
 
3. **Retrieve Passwords** : For each Wi-Fi profile name, the script utilizes `netsh wlan show profile` command with the `key=clear` option to reveal the password in plaintext.  
 
4. **Display Results** : Finally, it displays the collected Wi-Fi profile names and their corresponding passwords in a formatted table using PowerShell's `Format-Table` cmdlet.  

## Why It's Possible 
Windows stores Wi-Fi passwords in plaintext within its configuration files (`XML` format) under `C:\ProgramData\Microsoft\Wlansvc\Profiles\Interfaces\{Interface GUID}\`.  
This makes it feasible for administrative tools like `netsh` to access and retrieve these passwords directly, assuming the script runs with appropriate administrative privileges.  

## Using the Script 
To use the `Get-WifiPasswords.ps1` script:  
- Open PowerShell with administrative privileges.  
 
- Navigate to the directory where `Get-WifiPasswords.ps1` is located.  
 
- Execute the script by running `.\Get-WifiPasswords.ps1`.  


### Example Output: 


```console
ProfileName         Password
-----------         --------
WiFiNetwork1        Password123
GuestWiFi           N/A (if no password is set)
```  

**Note** : Ensure you have appropriate permissions to run PowerShell scripts and access Wi-Fi profile information on the system.  
