# Get all Wi-Fi profiles
$profiles = netsh wlan show profiles

# Extract profile names
$profileNames = $profiles | Select-String -Pattern "All User Profile\s*:\s*(.*)$" | ForEach-Object { $_.Matches.Groups[1].Value }

# Initialize an empty array to store Wi-Fi credentials
$wifiCredentials = @()

# Iterate over each profile name to get the Wi-Fi key (password)
foreach ($profileName in $profileNames) {
    $profileDetails = netsh wlan show profile name="$profileName" key=clear
    $keyContent = $profileDetails | Select-String -Pattern "Key Content\s*:\s*(.*)$"
    
    if ($keyContent) {
        $wifiPassword = $keyContent.Matches.Groups[1].Value
    } else {
        $wifiPassword = "N/A"
    }
    
    $wifiCredentials += [PSCustomObject]@{
        ProfileName = $profileName
        Password    = $wifiPassword
    }
}

# Display the Wi-Fi credentials
$wifiCredentials | Format-Table -AutoSize
