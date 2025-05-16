# IMPORTANT: Before running execute this command ==> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Log function
function Log {
    param([string]$msg)
    Write-Host "[INFO] $msg"
}

# Define download URL and installer path
$url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
$installerPath = "$env:TEMP\VSCodeSetup.exe"

Log "Downloading VS Code from: $url"
Start-BitsTransfer -Source $url -Destination $installerPath
Log "Download completed to: $installerPath"

# Install VS Code silently
Log "Starting silent installation..."
Start-Process -FilePath $installerPath -ArgumentList "/silent" -Wait
Log "Installation completed."

# Clean up installer
Remove-Item $installerPath -Force
Log "Installer removed."

# Check if VS Code CLI is in PATH
$codePath = "$env:LOCALAPPDATA\Programs\Microsoft VS Code\bin"
$currentPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")

if ($currentPath -notlike "*$codePath*") {
    Log "Adding VS Code bin folder to PATH: $codePath"
    [System.Environment]::SetEnvironmentVariable("PATH", "$currentPath;$codePath", "User")
} else {
    Log "VS Code bin path is already in PATH."
}

# Try to verify the CLI is now accessible
$codeExe = Join-Path $codePath "code.cmd"
if (Test-Path $codeExe) {
    Log "VS Code CLI installed successfully at: $codeExe"
    Log "You may need to restart PowerShell or log out/in to use the 'code' command."
} else {
    Log "WARNING: 'code' CLI not found at expected location."
}
