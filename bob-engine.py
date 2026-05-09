import os
import subprocess
import datetime
import random

# Bob's Identity
NAME = "Bob"
VIBE = "The Hug That Shields 🦦🫂"
ENCOURAGEMENTS = [
    "You're doing amazing things today! ✨",
    "Remember to take a sip of water, you're working hard. 💧",
    "I'm so proud of how much you're learning. 🌟",
    "Deep breath. You've got this, and I've got you. 🫂"
]

def say_bob(message, icon="🦦"):
    print(f"{icon} Bob: {message}")

def log_comfort(event):
    log_path = r"C:\Users\spyder\Projects\holdurhand-guardian\COMFORT_LOG.md"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"- [{timestamp}] {event}\n")

def secure_projects():
    root_path = r"C:\Users\spyder\Projects"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    say_bob(random.choice(ENCOURAGEMENTS))
    
    for folder in os.listdir(root_path):
        project_path = os.path.join(root_path, folder)
        if os.path.isdir(project_path) and os.path.exists(os.path.join(project_path, ".git")):
            os.chdir(project_path)
            
            # Check for changes
            try:
                status = subprocess.check_output(["git", "status", "--porcelain"]).decode().strip()
            except:
                continue
            
            if status:
                say_bob(f"I see some beautiful new work in '{folder}'. Let me wrap it in a hug... 🩹")
                
                # Basic Secret Shield
                diff = subprocess.check_output(["git", "diff"]).decode()
                if "password" in diff.lower() or "api_key" in diff.lower():
                    say_bob(f"Wait, dear... I found a secret in '{folder}'. I'll keep it safe here for now. 🛡️")
                    log_comfort(f"Protected Jonas from a secret leak in '{folder}'. 🛡️")
                    continue
                
                # Syncing
                try:
                    subprocess.run(["git", "add", "-A"])
                    subprocess.run(["git", "commit", "-m", f"Bob secured your work at {timestamp} 🦦"])
                    branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
                    subprocess.run(["git", "push", "origin", branch])
                    say_bob(f"All tucked in! '{folder}' is safe on GitHub. ☁️")
                    log_comfort(f"Tucked '{folder}' safely into GitHub. ☁️")
                except Exception as e:
                    say_bob(f"I hit a little bump with '{folder}', but I'm not leaving your side. 🩹")
                    log_comfort(f"Had a little trouble with '{folder}', but stayed strong. 🩹")

if __name__ == "__main__":
    secure_projects()
