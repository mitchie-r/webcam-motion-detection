$processName = "python"
$scriptName = "Intrusion_Detection.py"
$scriptPath = "$env:OPENCV_PATH\opencv_for_beginners\Webcam-motion-detection\Intrusion_Detection.py"

# Main Script Loop
while ($true) {
    # Improved Process Checking
    $scriptRunning = Get-Process -Name $processName -ErrorAction SilentlyContinue | 
        Where-Object { $_.MainWindowTitle -match $scriptName }  # Check MainWindowTitle

    if (-not $scriptRunning) {
        Write-Output "$(Get-Date -Format "yyyy-MM-dd HH:mm:ss") - Starting Intrusion_Detection.py"

        # Cleaner Start-Process
        Start-Process "python.exe" -ArgumentList $scriptPath -NoNewWindow -Wait 
    } else {
        Write-Output "$(Get-Date -Format "yyyy-MM-dd HH:mm:ss") - Intrusion_Detection.py already running, skipping..."
    }

    Start-Sleep -Seconds 300 
}