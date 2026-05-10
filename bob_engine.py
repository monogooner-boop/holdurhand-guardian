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
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except: pass
        return {
            "user_name": None,
            "experience_level": "beginner", # beginner, pro
            "language": "en", # en, nl
            "hand_holding": "often", # always, often, occasional
            "watched_directories": ["C:\\Users\\spyder\\Projects"],
            "sync_interval_minutes": 15,
            "secret_shield_enabled": True,
            "last_sync": None,
            "onboarding_complete": False,
            "theme": "strawberry_milk"
        }

    def save_config(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except: pass

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
            if match: return match.group(0)
        return None

class BobEngine:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_manager = ConfigManager(os.path.join(self.base_dir, "config.json"))
        self.shield = SecretShield(self.config_manager.config.get("secret_shield_enabled", True))
        self.log_path = os.path.join(self.base_dir, "COMFORT_LOG.md")
        
        self.translations = {
            "en": {
                "checking": "Checking your work... 🦦",
                "hugging": "Giving '{}' a hug... 🫂",
                "safe": "All safe and sound! ✨",
                "secret_blocked": "⚠️ Bob blocked a potential secret leak in '{}'.",
                "tucked": "☁️ Tucked '{}' safely into GitHub.",
                "bump": "🩹 Had a little trouble syncing '{}', but I'm still here.",
                "encouragements": [
                    "You're doing amazing things today! ✨",
                    "Remember to take a sip of water. 💧",
                    "I'm so proud of how much you're learning. 🌟",
                    "Deep breath. You've got this. 🫂"
                ]
            },
            "nl": {
                "checking": "Je werk controleren... 🦦",
                "hugging": "'{}' een knuffel geven... 🫂",
                "safe": "Alles is veilig en wel! ✨",
                "secret_blocked": "⚠️ Bob heeft een geheim lek voorkomen in '{}'.",
                "tucked": "☁️ '{}' veilig opgeborgen op GitHub.",
                "bump": "🩹 Klein bobbeltje bij '{}', maar ik wijk niet van je zijde.",
                "encouragements": [
                    "Je doet geweldige dingen vandaag! ✨",
                    "Vergeet niet een slokje water te nemen. 💧",
                    "Ik ben trots op hoeveel je leert. 🌟",
                    "Haal adem. Je kunt dit. 🫂"
                ]
            }
        }

    def get_msg(self, key):
        lang = self.config_manager.config.get("language", "en")
        return self.translations.get(lang, self.translations["en"]).get(key)

    def log_comfort(self, event):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(f"- [{timestamp}] {event}\n")
        except: pass

    def run_git(self, args, path):
        try:
            result = subprocess.run(["git"] + args, cwd=path, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except: return None

    def secure_all(self, progress_callback=None):
        lang = self.config_manager.config.get("language", "en")
        msgs = self.translations[lang]
        
        if progress_callback: progress_callback(msgs["checking"])
        
        watched = self.config_manager.config.get("watched_directories", [])
        for root in watched:
            if not os.path.exists(root): continue
            for folder in os.listdir(root):
                project_path = os.path.join(root, folder)
                if os.path.isdir(project_path) and os.path.exists(os.path.join(project_path, ".git")):
                    if progress_callback: progress_callback(msgs["hugging"].format(folder))
                    self.secure_project(folder, project_path, msgs)
        
        self.config_manager.config["last_sync"] = datetime.datetime.now().strftime("%H:%M:%S")
        self.config_manager.save_config()
        if progress_callback: progress_callback(msgs["safe"])

    def secure_project(self, name, path, msgs):
        status = self.run_git(["status", "--porcelain"], path)
        if status:
            diff = self.run_git(["diff"], path) or ""
            untracked = self.run_git(["ls-files", "--others", "--exclude-standard"], path) or ""
            
            content_to_check = diff
            if untracked:
                for f in untracked.splitlines():
                    try:
                        with open(os.path.join(path, f), 'r', errors='ignore') as file:
                            content_to_check += file.read()
                    except: pass

            if self.shield.scan(content_to_check):
                self.log_comfort(msgs["secret_blocked"].format(name))
                return

            try:
                self.run_git(["add", "-A"], path)
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.run_git(["commit", "-m", f"Bob secured your work at {ts} 🦦"], path)
                branch = self.run_git(["rev-parse", "--abbrev-ref", "HEAD"], path) or "main"
                self.run_git(["push", "origin", branch], path)
                self.log_comfort(msgs["tucked"].format(name))
            except:
                self.log_comfort(msgs["bump"].format(name))

    def start_patrol(self):
        while True:
            self.secure_all()
            interval = self.config_manager.config.get("sync_interval_minutes", 15)
            time.sleep(interval * 60)

if __name__ == "__main__":
    BobEngine().start_patrol()
