Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Get all screens
$screens = [System.Windows.Forms.Screen]::AllScreens

# Loop through each screen
foreach ($screen in $screens) {
    # Create a bitmap object to store the screenshot for this screen
    $screenshot = New-Object System.Drawing.Bitmap($screen.Bounds.Width, $screen.Bounds.Height)

    # Create a graphics object from the bitmap
    $graphics = [System.Drawing.Graphics]::FromImage($screenshot)

    # Capture the screen
    $graphics.CopyFromScreen($screen.Bounds.Location, [System.Drawing.Point]::Empty, $screen.Bounds.Size)

    # Dispose the graphics object
    $graphics.Dispose()

    # Define the output file path for this screen
    $outputFile = "C:\temp\Screenshot_$($screen.DeviceName.Replace('\', '_')).jpg"

    # Save the screenshot to a file
    $screenshot.Save($outputFile, [System.Drawing.Imaging.ImageFormat]::Jpeg)

    # Dispose the screenshot object
    $screenshot.Dispose()

    Write-Output "Screenshot saved to $outputFile"
}
