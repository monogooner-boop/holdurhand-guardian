# Bob the Otter - Professional Installer 🦦🛡️
# This script sets up Bob as a real app on your Windows PC.

$projectName = "Bob the Otter"
$projectPath = "C:\Users\spyder\Projects\holdurhand-guardian"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "Bob's Cottage.lnk"
$pythonExe = "python.exe"
$pythonwExe = "pythonw.exe"

Clear-Host
Write-Host "--- 🦦 Bob is moving into his new home... ---" -ForegroundColor Cyan

# 1. Check Python & Dependencies
Write-Host "[*] Checking your Python tools..." -ForegroundColor Yellow
& $pythonExe -m pip install customtkinter --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Oh no! I had trouble installing my favorite tools. Please check your internet connection." -ForegroundColor Red
    exit
}

# 2. Create Desktop Shortcut for the GUI (The Cottage)
Write-Host "[*] Building your shortcut to the Riverside Cottage..." -ForegroundColor Yellow
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $pythonwExe
$shortcut.Arguments = "`"$projectPath\cottage.py`""
$shortcut.WorkingDirectory = $projectPath
$shortcut.Description = "Open Bob's Riverside Cottage dashboard"
$shortcut.IconLocation = "shell32.dll, 43" 
$shortcut.Save()

# 3. Setup Background Service (Windows Task Scheduler)
Write-Host "[*] Making sure I can watch over you even when the Cottage is closed..." -ForegroundColor Yellow
$taskName = "BobGuardianService"
$taskAction = New-ScheduledTaskAction -Execute $pythonwExe -Argument "`"$projectPath\start_bob_background.pyw`"" -WorkingDirectory $projectPath
$taskTrigger = New-ScheduledTaskTrigger -AtLogOn
$taskSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0

# Remove old task if it exists
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# Register new task
Register-ScheduledTask -TaskName $taskName -Action $taskAction -Trigger $taskTrigger -Settings $taskSettings -Description "Bob's background sync service"

# 4. Final Verification
Write-Host "`n[v] EVERYTHING IS READY! 🫂" -ForegroundColor Green
Write-Host "1. Look at your Desktop, I put a shortcut to 'Bob's Cottage' there! ✨" -ForegroundColor White
Write-Host "2. I'll start working in the background automatically every time you log in. 🛡️" -ForegroundColor White
Write-Host "3. You're doing great, Jonas. I'm proud of you. 🦦" -ForegroundColor White

# Launch the Cottage for the first time
& $pythonwExe "$projectPath\cottage.py"
