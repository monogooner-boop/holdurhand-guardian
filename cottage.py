import customtkinter as ctk
import os
import subprocess
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
        self.geometry("700x500")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Tabview ---
        self.tabview = ctk.CTkTabview(self, corner_radius=15)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.tab_home = self.tabview.add("Home 🏡")
        self.tab_settings = self.tabview.add("Settings ⚙️")
        self.tab_diary = self.tabview.add("Diary 📖")

        self.setup_home_tab()
        self.setup_settings_tab()
        self.setup_diary_tab()

    def setup_home_tab(self):
        self.tab_home.grid_columnconfigure(0, weight=1)
        self.tab_home.grid_columnconfigure(1, weight=1)
        
        # Header
        self.header_label = ctk.CTkLabel(self.tab_home, text="Welcome Home, Jonas!", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        # Status Box
        self.status_frame = ctk.CTkFrame(self.tab_home, corner_radius=10, fg_color="#34495E")
        self.status_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        
        last_sync = self.engine.config_manager.config.get("last_sync") or "Never"
        self.status_label = ctk.CTkLabel(self.status_frame, text=f"Status: Guarding your dreams\nLast Sync: {last_sync}", font=ctk.CTkFont(size=14))
        self.status_label.pack(padx=20, pady=20)

        # Quick Actions
        self.hug_btn = ctk.CTkButton(self.tab_home, text="🫂 Give me a hug\n(Secure Projects Now)", 
                                     font=ctk.CTkFont(size=16, weight="bold"),
                                     height=80,
                                     command=self.hug_action)
        self.hug_btn.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        self.shield_info = ctk.CTkLabel(self.tab_home, text="🛡️ Secret Shield is ACTIVE\nNo passwords will leak today.", text_color="#2ECC71")
        self.shield_info.grid(row=2, column=1, padx=20, pady=20)

    def setup_settings_tab(self):
        self.tab_settings.grid_columnconfigure(0, weight=1)
        
        self.settings_label = ctk.CTkLabel(self.tab_settings, text="Bob's Preferences", font=ctk.CTkFont(size=20, weight="bold"))
        self.settings_label.pack(pady=20)

        # Watched Directories
        self.dir_label = ctk.CTkLabel(self.tab_settings, text="Watching these folders:")
        self.dir_label.pack(pady=(10, 0))
        
        watched_dirs = ", ".join(self.engine.config_manager.config.get("watched_directories", []))
        self.dir_entry = ctk.CTkEntry(self.tab_settings, width=400)
        self.dir_entry.insert(0, watched_dirs)
        self.dir_entry.pack(pady=5)

        # Sync Interval
        self.interval_label = ctk.CTkLabel(self.tab_settings, text="Sync every X minutes:")
        self.interval_label.pack(pady=(10, 0))
        
        self.interval_slider = ctk.CTkSlider(self.tab_settings, from_=5, to=60, number_of_steps=11)
        self.interval_slider.set(self.engine.config_manager.config.get("sync_interval_minutes", 15))
        self.interval_slider.pack(pady=5)

        # Save Button
        self.save_btn = ctk.CTkButton(self.tab_settings, text="Save Settings", command=self.save_settings)
        self.save_btn.pack(pady=30)

    def setup_diary_tab(self):
        self.tab_diary.grid_columnconfigure(0, weight=1)
        self.tab_diary.grid_rowconfigure(1, weight=1)

        self.diary_label = ctk.CTkLabel(self.tab_diary, text="Recent Comfort Logs", font=ctk.CTkFont(size=20, weight="bold"))
        self.diary_label.grid(row=0, column=0, pady=10)

        self.log_text = ctk.CTkTextbox(self.tab_diary, width=600, height=300)
        self.log_text.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        self.refresh_logs()

        self.open_file_btn = ctk.CTkButton(self.tab_diary, text="Open Diary in Notepad", command=self.open_diary_file)
        self.open_file_btn.grid(row=2, column=0, pady=10)

    def refresh_logs(self):
        try:
            with open(self.engine.log_path, "r", encoding="utf-8") as f:
                logs = f.readlines()
                self.log_text.delete("1.0", "end")
                self.log_text.insert("1.0", "".join(logs[-20:])) # Show last 20 entries
        except:
            self.log_text.insert("1.0", "No logs yet. Bob is waiting...")

    def hug_action(self):
        self.hug_btn.configure(state="disabled", text="🦦 Bob is hugging...")
        self.update()
        self.engine.secure_all()
        self.hug_btn.configure(state="normal", text="🫂 Give me a hug\n(Secure Projects Now)")
        self.status_label.configure(text=f"Status: Guarding your dreams\nLast Sync: {self.engine.config_manager.config['last_sync']}")
        self.refresh_logs()
        messagebox.showinfo("Bob says...", "🫂 *Squeeze*\n\nAll your work is tucked in safely on GitHub.")

    def save_settings(self):
        dirs = [d.strip() for d in self.dir_entry.get().split(",")]
        self.engine.config_manager.config["watched_directories"] = dirs
        self.engine.config_manager.config["sync_interval_minutes"] = int(self.interval_slider.get())
        self.engine.config_manager.save_config()
        messagebox.showinfo("Bob", "Settings saved! I'll remember this.")

    def open_diary_file(self):
        try:
            os.startfile(self.engine.log_path)
        except:
            messagebox.showerror("Error", "Could not open the log file.")

if __name__ == "__main__":
    app = BobsCottage()
    app.mainloop()
