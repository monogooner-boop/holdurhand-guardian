# 🦦 Bob: The Hug That Shields (Core Engine)
# "You're doing amazing, Jonas. I've got your back."

$rootPath = "C:\Users\spyder\Projects"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$secretKeywords = @("password", "api_key", "secret", "token", "auth_token", "key_")

$encouragements = @(
    "You're doing amazing things today! ✨",
    "Remember to take a sip of water, you're working hard. 💧",
    "I'm so proud of how much you're learning. 🌟",
    "Coding is a superpower, and you're getting stronger every day! 💪",
    "Deep breath. You've got this, and I've got you. 🫂"
)

function Say-Bob ($message, $color = "Cyan") {
    Write-Host "🦦 Bob: $message" -ForegroundColor $color
}

# Bob's warm welcome
$randomEncouragement = $encouragements | Get-Random
Say-Bob "Hello Jonas! I'm here to hold your hand while you create. $randomEncouragement" "Yellow"

$projects = Get-ChildItem -Path $rootPath -Directory

foreach ($project in $projects) {
    $projectPath = $project.FullName
    $projectName = $project.Name
    
    Set-Location -Path $projectPath
    
    if (Test-Path ".git") {
        $status = git status --porcelain
        
        if ($status) {
            Say-Bob "I see some beautiful new work in '$projectName'. Let me wrap it in a warm hug and keep it safe... 🫂" "Green"
            
            # 👵 Wise Oversight (Secret Shield)
            $leaks = git diff | Select-String -Pattern $secretKeywords
            if ($leaks) {
                Say-Bob "Wait a second, dear... I think I see a secret in '$projectName'. I'll keep this one right here so the world doesn't see it. You're safe with me. 🛡️" "Red"
                continue
            }

            # 🦦 Otter Strength (Sync)
            try {
                git add -A
                git commit -m "Bob: The Hug That Shields - Secured at $timestamp 🦦"
                $branch = git rev-parse --abbrev-ref HEAD
                git push origin $branch
                Say-Bob "All tucked in! '$projectName' is safe and sound in the cloud. ☁️" "Magenta"
            } catch {
                Say-Bob "I hit a little bump with '$projectName', but don't you worry. I'm staying right here until it's fixed. 🩹" "Gray"
            }
        }
    }
}

Say-Bob "Patrol complete! You can relax now, knowing everything is secured. See you soon! 🧡" "Yellow"
Set-Location -Path $rootPath
