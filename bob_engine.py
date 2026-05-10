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
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        # Default safe config
        return {
            "watched_directories": ["C:\\Users\\spyder\\Projects"],
            "sync_interval_minutes": 15,
            "secret_shield_enabled": True,
            "last_sync": None,
            "auto_start": True,
            "vibe": "The Hug That Shields 🦦🫂"
        }

    def save_config(self):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception:
            pass

class SecretShield:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.patterns = [
            re.compile(r'(?i)password\s*[:=]\s*["\']?[\w\-\.!@#$%^&*()]+["\']?'),
            re.compile(r'(?i)api_key\s*[:=]\s*["\']?[\w\-\.]+["\']?'),
            re.compile(r'(?i)secret\s*[:=]\s*["\']?[\w\-\.]+["\']?'),
            re.compile(r'AKIA[0-9A-Z]{16}'),
            re.compile(r'xox[baprs]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}'),
            re.compile(r'-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----')
        ]

    def scan(self, text):
        if not self.enabled: return None
        for pattern in self.patterns:
            match = pattern.search(text)
            if match:
                return match.group(0)
        return None

class BobEngine:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_manager = ConfigManager(os.path.join(self.base_dir, "config.json"))
        self.shield = SecretShield(self.config_manager.config.get("secret_shield_enabled", True))
        self.log_path = os.path.join(self.base_dir, "COMFORT_LOG.md")
        
        self.hugs = [
            "You're doing amazing things today! ✨",
            "Remember to take a sip of water, you're working hard. 💧",
            "I'm so proud of how much you're learning. 🌟",
            "Deep breath. You've got this, and I've got you. 🫂",
            "Every line of code is a step towards your dreams. 🚀"
        ]

    def log_comfort(self, event):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(f"- [{timestamp}] {event}\n")
        except: pass

    def run_git(self, args, path):
        try:
            # Check if Git is even installed first
            result = subprocess.run(["git"] + args, cwd=path, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def secure_all(self, progress_callback=None):
        if progress_callback: progress_callback("Checking your work... 🦦")
        
        watched = self.config_manager.config.get("watched_directories", [])
        for root in watched:
            if not os.path.exists(root): continue
            for folder in os.listdir(root):
                project_path = os.path.join(root, folder)
                if os.path.isdir(project_path) and os.path.exists(os.path.join(project_path, ".git")):
                    if progress_callback: progress_callback(f"Giving '{folder}' a hug... 🫂")
                    self.secure_project(folder, project_path)
        
        self.config_manager.config["last_sync"] = datetime.datetime.now().strftime("%H:%M:%S")
        self.config_manager.save_config()
        if progress_callback: progress_callback("All safe and sound! ✨")

    def secure_project(self, name, path):
        status = self.run_git(["status", "--porcelain"], path)
        if status:
            # Check for secrets before adding
            diff = self.run_git(["diff"], path) or ""
            untracked = self.run_git(["ls-files", "--others", "--exclude-standard"], path) or ""
            
            content_to_check = diff
            if untracked:
                for f in untracked.splitlines():
                    try:
                        with open(os.path.join(path, f), 'r', errors='ignore') as file:
                            content_to_check += file.read()
                    except: pass

            found_secret = self.shield.scan(content_to_check)
            if found_secret:
                self.log_comfort(f"⚠️ Bob blocked a potential secret leak in '{name}'.")
                return f"secret_found:{name}"

            # If safe, proceed
            try:
                self.run_git(["add", "-A"], path)
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.run_git(["commit", "-m", f"Bob secured your work at {ts} 🦦"], path)
                branch = self.run_git(["rev-parse", "--abbrev-ref", HEAD], path) or "main"
                self.run_git(["push", "origin", branch], path)
                self.log_comfort(f"☁️ Tucked '{name}' safely into GitHub.")
            except:
                self.log_comfort(f"🩹 Had a little trouble syncing '{name}', but I'm still here.")

    def start_patrol(self):
        while True:
            self.secure_all()
            interval = self.config_manager.config.get("sync_interval_minutes", 15)
            time.sleep(interval * 60)

if __name__ == "__main__":
    BobEngine().start_patrol()
