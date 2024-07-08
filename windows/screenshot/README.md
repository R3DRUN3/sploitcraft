# Capturing Screenshots from Windows Screens using PowerShell 

## Overview 
This repository contains a PowerShell script (`Capture-Screenshots.ps1`) designed to capture screenshots from all connected screens on a Windows system.  
The script utilizes the .NET framework to interact with screen properties and graphics to capture the screenshots.  
## How It Works 
The script employs the `System.Windows.Forms.Screen` and `System.Drawing` namespaces to achieve its functionality.  
It iterates through each connected screen, creates a bitmap object to store the screenshot, captures the screen using graphics objects, and saves the screenshots as JPEG files.  
### Key Steps: 
 
1. **Get All Screens** :
The script retrieves information about all connected screens using `System.Windows.Forms.Screen::AllScreens`.  
 
2. **Capture Screenshots** :
For each screen detected, a bitmap object is created to store the screenshot: the script uses `System.Drawing.Graphics` to capture the screen and save it as a JPEG file.  
 
3. **Save Screenshots** :
Each screenshot is saved to a specified directory (`C:\temp\`) with a filename that includes the screen's device name.  
 
4. **Display Output** :
After saving each screenshot, the script outputs the path where the screenshot is saved.  

## Why It's Possible 
Windows provides extensive support for screen capture through its .NET framework libraries.  
This allows PowerShell scripts like `Capture-Screenshots.ps1` to programmatically capture screens with high fidelity.  
## Using the Script 
To use the `Capture-Screenshots.ps1` script: 
- Open PowerShell with administrative privileges.  
 
- Navigate to the directory where `Capture-Screenshots.ps1` is located.  
 
- Execute the script by running `.\Capture-Screenshots.ps1`.  

### Example Output: 


```console
Screenshot saved to C:\temp\Screenshot___._DISPLAY1.jpg
Screenshot saved to C:\temp\Screenshot___._DISPLAY2.jpg
Screenshot saved to C:\temp\Screenshot___._DISPLAY3.jpg
```
**Note** : Ensure the script runs with appropriate permissions to access screen information and save files in the specified directory.