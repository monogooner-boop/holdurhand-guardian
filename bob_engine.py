import os
import subprocess
import datetime
import random
import json
import time
import re

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "watched_directories": ["C:\\Users\\spyder\\Projects"],
                "sync_interval_minutes": 15,
                "secret_shield_enabled": true,
                "last_sync": None,
                "auto_start": True
            }

    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

class SecretShield:
    def __init__(self, enabled=True):
        self.enabled = enabled
        # Professional regex patterns for common secrets
        self.patterns = [
            re.compile(r'(?i)password\s*[:=]\s*["\']?[\w\-\.!@#$%^&*()]+["\']?'),
            re.compile(r'(?i)api_key\s*[:=]\s*["\']?[\w\-\.]+["\']?'),
            re.compile(r'(?i)secret\s*[:=]\s*["\']?[\w\-\.]+["\']?'),
            re.compile(r'AKIA[0-9A-Z]{16}'), # AWS Access Key
            re.compile(r'xox[baprs]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}'), # Slack Token
            re.compile(r'-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----') # SSH Private Key
        ]

    def contains_secrets(self, text):
        if not self.enabled:
            return False
        for pattern in self.patterns:
            if pattern.search(text):
                return True
        return False

class BobEngine:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_manager = ConfigManager(os.path.join(self.base_dir, "config.json"))
        self.shield = SecretShield(self.config_manager.config.get("secret_shield_enabled", True))
        self.log_path = os.path.join(self.base_dir, "COMFORT_LOG.md")
        
        self.encouragements = [
            "You're doing amazing things today! ✨",
            "Remember to take a sip of water, you're working hard. 💧",
            "I'm so proud of how much you're learning. 🌟",
            "Deep breath. You've got this, and I've got you. 🫂",
            "Every line of code is a step towards your dreams. 🚀"
        ]

    def say(self, message, icon="🦦"):
        print(f"{icon} Bob: {message}")

    def log_comfort(self, event):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(f"- [{timestamp}] {event}\n")
        except Exception:
            pass # Bob never stresses you with log errors

    def run_git(self, args, path):
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # We don't raise, we return None and let the engine handle it gracefully
            return None

    def secure_all(self):
        self.say(random.choice(self.encouragements))
        watched = self.config_manager.config.get("watched_directories", [])
        
        for root in watched:
            if not os.path.exists(root):
                continue
                
            for folder in os.listdir(root):
                project_path = os.path.join(root, folder)
                if os.path.isdir(project_path) and os.path.exists(os.path.join(project_path, ".git")):
                    self.secure_project(folder, project_path)
        
        self.config_manager.config["last_sync"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.config_manager.save_config()

    def secure_project(self, name, path):
        # Check for changes
        status = self.run_git(["status", "--porcelain"], path)
        if status:
            self.say(f"I see some beautiful new work in '{name}'. Let me wrap it in a hug... 🩹")
            
            # Advanced Secret Shield Check
            diff = self.run_git(["diff"], path) or ""
            untracked = self.run_git(["ls-files", "--others", "--exclude-standard"], path) or ""
            
            # Check diffs and untracked files for secrets
            content_to_check = diff
            if untracked:
                for f in untracked.splitlines():
                    try:
                        with open(os.path.join(path, f), 'r', errors='ignore') as file:
                            content_to_check += file.read()
                    except:
                        pass

            if self.shield.contains_secrets(content_to_check):
                self.say(f"Wait, dear... I found a secret in '{name}'. I'll keep it safe here for now. 🛡️", icon="⚠️")
                self.log_comfort(f"Protected Jonas from a secret leak in '{name}'. 🛡️")
                return

            # Perform the sync
            try:
                self.run_git(["add", "-A"], path)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.run_git(["commit", "-m", f"Bob secured your work at {timestamp} 🦦"], path)
                
                branch = self.run_git(["rev-parse", "--abbrev-ref", "HEAD"], path) or "main"
                self.run_git(["push", "origin", branch], path)
                
                self.say(f"All tucked in! '{name}' is safe on GitHub. ☁️")
                self.log_comfort(f"Tucked '{name}' safely into GitHub. ☁️")
            except Exception as e:
                self.say(f"I hit a little bump with '{name}', but I'm not leaving your side. 🩹")
                self.log_comfort(f"Had a little trouble with '{name}', but stayed strong. 🩹")

    def start_patrol(self, continuous=False):
        while True:
            self.secure_all()
            if not continuous:
                break
            
            interval = self.config_manager.config.get("sync_interval_minutes", 15)
            self.say(f"I'm resting by the river for {interval} minutes. Call me if you need me! 🌊")
            time.sleep(interval * 60)

if __name__ == "__main__":
    engine = BobEngine()
    # If run directly, we might want to know if it's for a one-off or background
    import sys
    is_background = "--background" in sys.argv
    engine.start_patrol(continuous=is_background)
