import customtkinter as ctk
import os
import subprocess
import random
from tkinter import messagebox
from bob_engine import BobEngine

# Set the appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BobsCottage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.engine = BobEngine()
        self.title("Bob's Riverside Cottage 🦦")
        self.geometry("800x600")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar / Navigation ---
        self.tabview = ctk.CTkTabview(self, corner_radius=20, fg_color="#1B2631")
        self.tabview.grid(row=0, column=0, padx=25, pady=25, sticky="nsew")
        
        self.tab_home = self.tabview.add("Home 🏡")
        self.tab_settings = self.tabview.add("Settings ⚙️")
        self.tab_diary = self.tabview.add("Diary 📖")

        self.setup_home_tab()
        self.setup_settings_tab()
        self.setup_diary_tab()

    def setup_home_tab(self):
        self.tab_home.grid_columnconfigure(0, weight=1)
        
        # Friendly Header
        self.welcome_label = ctk.CTkLabel(self.tab_home, text=f"Welcome back, Jonas! 🦦", font=ctk.CTkFont(size=28, weight="bold"))
        self.welcome_label.pack(pady=(30, 10))
        
        self.vibe_label = ctk.CTkLabel(self.tab_home, text=random.choice(self.engine.hugs), font=ctk.CTkFont(size=16, slant="italic"), text_color="#ABB2B9")
        self.vibe_label.pack(pady=(0, 30))

        # Bento Status Box
        self.status_frame = ctk.CTkFrame(self.tab_home, corner_radius=20, fg_color="#2E4053", height=150)
        self.status_frame.pack(padx=40, pady=10, fill="x")
        
        self.status_icon = ctk.CTkLabel(self.status_frame, text="🛡️", font=ctk.CTkFont(size=40))
        self.status_icon.pack(side="left", padx=30, pady=20)
        
        last_sync = self.engine.config_manager.config.get("last_sync") or "Resting by the river"
        self.status_text = ctk.CTkLabel(self.status_frame, text=f"Bob is watching over your dreams.\nLast secure sync: {last_sync}", font=ctk.CTkFont(size=16), justify="left")
        self.status_text.pack(side="left", padx=10)

        # Main Action Button (The Hug)
        self.hug_btn = ctk.CTkButton(self.tab_home, text="🫂 Give me a hug\n(Secure my work now)", 
                                     font=ctk.CTkFont(size=20, weight="bold"),
                                     fg_color="#1ABC9C", hover_color="#16A085",
                                     height=100, corner_radius=20,
                                     command=self.hug_action)
        self.hug_btn.pack(padx=40, pady=40, fill="x")

        # Live Progress Label
        self.progress_label = ctk.CTkLabel(self.tab_home, text="", font=ctk.CTkFont(size=14), text_color="#5DADE2")
        self.progress_label.pack(pady=10)

    def setup_settings_tab(self):
        self.tab_settings.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.tab_settings, text="Bob's Preferences", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        # Watched Directories Section
        self.dir_frame = ctk.CTkFrame(self.tab_settings, corner_radius=15)
        self.dir_frame.pack(padx=40, pady=10, fill="x")
        
        ctk.CTkLabel(self.dir_frame, text="Where should I look for your work? (Folders separated by commas)", font=ctk.CTkFont(size=14)).pack(pady=(15, 5), padx=20, anchor="w")
        
        watched_dirs = ", ".join(self.engine.config_manager.config.get("watched_directories", []))
        self.dir_entry = ctk.CTkEntry(self.dir_frame, width=500, height=40, corner_radius=10)
        self.dir_entry.insert(0, watched_dirs)
        self.dir_entry.pack(pady=(0, 15), padx=20, fill="x")

        # Sync Interval Section
        self.timer_frame = ctk.CTkFrame(self.tab_settings, corner_radius=15)
        self.timer_frame.pack(padx=40, pady=10, fill="x")
        
        self.interval_val = self.engine.config_manager.config.get("sync_interval_minutes", 15)
        self.timer_label = ctk.CTkLabel(self.timer_frame, text=f"How often should I check? (Every {self.interval_val} minutes)", font=ctk.CTkFont(size=14))
        self.timer_label.pack(pady=(15, 5), padx=20, anchor="w")
        
        self.interval_slider = ctk.CTkSlider(self.timer_frame, from_=5, to=60, number_of_steps=11, command=self.update_timer_label)
        self.interval_slider.set(self.interval_val)
        self.interval_slider.pack(pady=(0, 20), padx=20, fill="x")

        # Secret Shield Toggle
        self.shield_var = ctk.BooleanVar(value=self.engine.config_manager.config.get("secret_shield_enabled", True))
        self.shield_switch = ctk.CTkSwitch(self.tab_settings, text="Enable Secret Shield (Recommended) 🛡️", variable=self.shield_var)
        self.shield_switch.pack(pady=20)

        # Save Button
        self.save_btn = ctk.CTkButton(self.tab_settings, text="Save & Update Bob", font=ctk.CTkFont(weight="bold"), 
                                      height=45, corner_radius=10, command=self.save_settings)
        self.save_btn.pack(pady=20)

    def setup_diary_tab(self):
        self.tab_diary.grid_columnconfigure(0, weight=1)
        self.tab_diary.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.tab_diary, text="Bob's Daily Thoughts 🦦📖", font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, pady=20)

        self.log_text = ctk.CTkTextbox(self.tab_diary, corner_radius=15, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_text.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        
        self.refresh_logs()

        self.btn_frame = ctk.CTkFrame(self.tab_diary, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, pady=20)

        ctk.CTkButton(self.btn_frame, text="Refresh Diary", command=self.refresh_logs).pack(side="left", padx=10)
        ctk.CTkButton(self.btn_frame, text="Open Full Log File", command=self.open_diary_file).pack(side="left", padx=10)

    def update_timer_label(self, val):
        self.timer_label.configure(text=f"How often should I check? (Every {int(val)} minutes)")

    def refresh_logs(self):
        try:
            if os.path.exists(self.engine.log_path):
                with open(self.engine.log_path, "r", encoding="utf-8") as f:
                    logs = f.readlines()
                    self.log_text.delete("1.0", "end")
                    # Show the most recent thoughts first
                    self.log_text.insert("1.0", "".join(logs[-50:]))
            else:
                self.log_text.insert("1.0", "No thoughts yet. Let's make some memories today!")
        except:
            self.log_text.insert("1.0", "I'm having a little trouble reading my diary. But I'm sure it's full of happy things!")

    def hug_action(self):
        self.hug_btn.configure(state="disabled", text="🦦 Bob is hugging...")
        self.progress_label.configure(text="Starting my rounds... 🚶‍♂️")
        self.update()
        
        # We pass a callback to the engine to update the UI progress
        def update_progress(msg):
            self.progress_label.configure(text=msg)
            self.update()

        self.engine.secure_all(progress_callback=update_progress)
        
        self.hug_btn.configure(state="normal", text="🫂 Give me a hug\n(Secure my work now)")
        self.status_text.configure(text=f"Bob is watching over your dreams.\nLast secure sync: {self.engine.config_manager.config['last_sync']}")
        self.refresh_logs()
        messagebox.showinfo("Bob says...", "🫂 *Squeeze*\n\nEverything is safe, Jonas. You're doing amazing today!")

    def save_settings(self):
        dirs = [d.strip() for d in self.dir_entry.get().split(",") if d.strip()]
        self.engine.config_manager.config["watched_directories"] = dirs
        self.engine.config_manager.config["sync_interval_minutes"] = int(self.interval_slider.get())
        self.engine.config_manager.config["secret_shield_enabled"] = self.shield_var.get()
        self.engine.config_manager.save_config()
        messagebox.showinfo("Bob", "I've updated my notes! I'll follow your new schedule now. 🦦✨")

    def open_diary_file(self):
        try: os.startfile(self.engine.log_path)
        except: messagebox.showerror("Oops", "I can't find my diary right now. Maybe it's hidden under a rock?")

if __name__ == "__main__":
    app = BobsCottage()
    app.mainloop()
