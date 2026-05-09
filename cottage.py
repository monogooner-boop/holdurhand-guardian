import customtkinter as ctk
import os
import subprocess
from tkinter import messagebox

# Set the appearance mode and color theme
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class BobsCottage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bob's Riverside Cottage 🦦")
        self.geometry("600x450")
        self.resizable(False, False)

        # Configure grid layout (Bento Grid Style)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Header Section (Spans both columns) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Bob 🦦", font=ctk.CTkFont(size=32, weight="bold"))
        self.title_label.pack(anchor="w")
        
        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="The Hug That Shields. You are safe here.", font=ctk.CTkFont(size=14, slant="italic"), text_color="gray")
        self.subtitle_label.pack(anchor="w")

        # --- Bento Box 1: The Hug (Sync) ---
        self.hug_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#2E4053") # Darker teal
        self.hug_frame.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")
        
        self.hug_btn = ctk.CTkButton(self.hug_frame, text="🫂 Give me a hug\n(Secure my work)", 
                                     font=ctk.CTkFont(size=16, weight="bold"), 
                                     fg_color="transparent", hover_color="#1ABC9C", text_color="white",
                                     command=self.hug_action)
        self.hug_btn.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Bento Box 2: The Diary ---
        self.diary_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#D4AC0D") # Warm orange/yellow
        self.diary_frame.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")
        
        self.diary_btn = ctk.CTkButton(self.diary_frame, text="📖 Read my diary\n(Comfort Logs)", 
                                       font=ctk.CTkFont(size=16, weight="bold"), 
                                       fg_color="transparent", hover_color="#F1C40F", text_color="#17202A",
                                       command=self.diary_action)
        self.diary_btn.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Bento Box 3: The AI / Shield ---
        self.shield_frame = ctk.CTkFrame(self, corner_radius=15)
        self.shield_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="nsew")
        
        self.shield_btn = ctk.CTkButton(self.shield_frame, text="🛡️ Watch over me (AI Shield & Setup)", 
                                        font=ctk.CTkFont(size=16),
                                        command=self.watch_action)
        self.shield_btn.pack(expand=True, fill="both", padx=10, pady=10)

    def hug_action(self):
        # Eventually calls bob-engine.py
        messagebox.showinfo("Bob says...", "🫂 *Squeeze*\n\nI am holding your hand. Everything is safe, Jonas. You're doing amazing today.")
        
    def diary_action(self):
        log_path = r"C:\Users\spyder\Projects\holdurhand-guardian\COMFORT_LOG.md"
        try:
            os.startfile(log_path)
        except:
            messagebox.showinfo("Bob's Diary", "📖 Today was a good day. I kept your dreams safe.")
        
    def watch_action(self):
        messagebox.showinfo("Bob's Shield", "🛡️ I'm guarding the perimeter! No secrets will leak. Also, the mobile AI chat is coming soon!")

if __name__ == "__main__":
    app = BobsCottage()
    app.mainloop()
