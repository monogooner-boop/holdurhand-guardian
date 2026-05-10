import customtkinter as ctk
import os
import random
from tkinter import messagebox
from bob_engine import BobEngine

# --- Strawberry Milk Theme Palette ---
THEME = {
    "bg": "#FFF4E0",
    "card": "#FFC0CB",
    "btn": "#FFB7B2",
    "btn_hover": "#FF8B94",
    "text": "#4A3F3F",
    "accent": "#E57373",
    "white": "#FFFFFF"
}

class BobsCottage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.engine = BobEngine()
        self.title("Bob's Riverside Cottage 🦦")
        self.geometry("850x650")
        self.configure(fg_color=THEME["bg"])
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Check for onboarding
        if not self.engine.config_manager.config.get("onboarding_complete", False):
            self.show_onboarding()
        else:
            self.show_main_app()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- ONBOARDING FLOW ---
    def show_onboarding(self):
        self.clear_screen()
        self.onboarding_frame = ctk.CTkFrame(self, corner_radius=30, fg_color=THEME["card"])
        self.onboarding_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.7)
        
        self.step = 1
        self.ob_otter = ctk.CTkLabel(self.onboarding_frame, text="🦦", font=ctk.CTkFont(size=100))
        self.ob_otter.pack(pady=(40, 10))
        
        self.ob_title = ctk.CTkLabel(self.onboarding_frame, text="Hi! I'm Bob.", font=ctk.CTkFont(size=32, weight="bold"), text_color=THEME["text"])
        self.ob_title.pack()
        
        self.ob_msg = ctk.CTkLabel(self.onboarding_frame, text="I'm here to hold your hand while you code.\nFirst, let's pick a language!", font=ctk.CTkFont(size=16), text_color=THEME["text"])
        self.ob_msg.pack(pady=20)

        self.ob_btn_frame = ctk.CTkFrame(self.onboarding_frame, fg_color="transparent")
        self.ob_btn_frame.pack(pady=20)

        self.btn_en = ctk.CTkButton(self.ob_btn_frame, text="English 🇬🇧", fg_color=THEME["btn"], text_color=THEME["text"], hover_color=THEME["btn_hover"], command=lambda: self.set_ob_lang("en"))
        self.btn_en.pack(side="left", padx=10)
        
        self.btn_nl = ctk.CTkButton(self.ob_btn_frame, text="Nederlands 🇳🇱", fg_color=THEME["btn"], text_color=THEME["text"], hover_color=THEME["btn_hover"], command=lambda: self.set_ob_lang("nl"))
        self.btn_nl.pack(side="left", padx=10)

    def set_ob_lang(self, lang):
        self.engine.config_manager.config["language"] = lang
        self.next_ob_step()

    def next_ob_step(self):
        self.step += 1
        lang = self.engine.config_manager.config["language"]
        
        if self.step == 2:
            self.btn_en.destroy()
            self.btn_nl.destroy()
            title = "What's your name?" if lang == "en" else "Hoe heet je?"
            self.ob_title.configure(text=title)
            self.ob_msg.configure(text="")
            self.name_entry = ctk.CTkEntry(self.onboarding_frame, placeholder_text="Name...", width=300, height=40, corner_radius=15)
            self.name_entry.pack(pady=20)
            self.ob_next = ctk.CTkButton(self.onboarding_frame, text="Next →", fg_color=THEME["btn"], text_color=THEME["text"], hover_color=THEME["btn_hover"], command=self.save_ob_name)
            self.ob_next.pack(pady=10)
            
        elif self.step == 3:
            self.name_entry.destroy()
            self.ob_next.destroy()
            msg = "How much experience do you have?" if lang == "en" else "Hoeveel ervaring heb je?"
            self.ob_title.configure(text=msg)
            
            self.btn_beg = ctk.CTkButton(self.onboarding_frame, text="Beginner 🐣", fg_color=THEME["btn"], text_color=THEME["text"], hover_color=THEME["btn_hover"], command=lambda: self.save_ob_exp("beginner"))
            self.btn_beg.pack(pady=10)
            self.btn_pro = ctk.CTkButton(self.onboarding_frame, text="Professional 🚀", fg_color=THEME["btn"], text_color=THEME["text"], hover_color=THEME["btn_hover"], command=lambda: self.save_ob_exp("pro"))
            self.btn_pro.pack(pady=10)

        elif self.step == 4:
            self.btn_beg.destroy()
            self.btn_pro.destroy()
            msg = "Final step: How often should I hug your work?" if lang == "en" else "Laatste stap: Hoe vaak zal ik je werk knuffelen?"
            self.ob_title.configure(text=msg)
            
            self.btn_a = ctk.CTkButton(self.onboarding_frame, text="Always (Every 5m) 🫂", fg_color=THEME["btn"], text_color=THEME["text"], hover_color=THEME["btn_hover"], command=lambda: self.finish_ob(5))
            self.btn_a.pack(pady=10)
            self.btn_o = ctk.CTkButton(self.onboarding_frame, text="Often (Every 15m) ✨", fg_color=THEME["btn"], text_color=THEME["text"], hover_color=THEME["btn_hover"], command=lambda: self.finish_ob(15))
            self.btn_o.pack(pady=10)

    def save_ob_name(self):
        name = self.name_entry.get() or "Friend"
        self.engine.config_manager.config["user_name"] = name
        self.next_ob_step()

    def save_ob_exp(self, exp):
        self.engine.config_manager.config["experience_level"] = exp
        self.next_ob_step()

    def finish_ob(self, interval):
        self.engine.config_manager.config["sync_interval_minutes"] = interval
        self.engine.config_manager.config["onboarding_complete"] = True
        self.engine.config_manager.save_config()
        self.show_main_app()

    # --- MAIN APPLICATION ---
    def show_main_app(self):
        self.clear_screen()
        self.configure(fg_color=THEME["bg"])
        
        # --- Sidebar Navigation ---
        self.nav_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=THEME["card"], width=200)
        self.nav_frame.pack(side="left", fill="y")
        
        self.nav_otter = ctk.CTkLabel(self.nav_frame, text="🦦", font=ctk.CTkFont(size=60))
        self.nav_otter.pack(pady=30)
        
        self.btn_home = ctk.CTkButton(self.nav_frame, text="Home 🏡", fg_color="transparent", text_color=THEME["text"], font=ctk.CTkFont(weight="bold"), anchor="w", command=lambda: self.show_tab("home"))
        self.btn_home.pack(pady=10, padx=20, fill="x")
        
        self.btn_diary = ctk.CTkButton(self.nav_frame, text="Diary 📖", fg_color="transparent", text_color=THEME["text"], font=ctk.CTkFont(weight="bold"), anchor="w", command=lambda: self.show_tab("diary"))
        self.btn_diary.pack(pady=10, padx=20, fill="x")
        
        self.btn_settings = ctk.CTkButton(self.nav_frame, text="Settings ⚙️", fg_color="transparent", text_color=THEME["text"], font=ctk.CTkFont(weight="bold"), anchor="w", command=lambda: self.show_tab("settings"))
        self.btn_settings.pack(pady=10, padx=20, fill="x")

        # --- Content Area ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        
        self.show_tab("home")

    def show_tab(self, tab):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        if tab == "home": self.draw_home()
        elif tab == "diary": self.draw_diary()
        elif tab == "settings": self.draw_settings()

    def draw_home(self):
        name = self.engine.config_manager.config.get("user_name", "Jonas")
        lang = self.engine.config_manager.config.get("language", "en")
        
        welcome = f"Welcome back, {name}! 🦦" if lang == "en" else f"Welkom terug, {name}! 🦦"
        ctk.CTkLabel(self.content_frame, text=welcome, font=ctk.CTkFont(size=32, weight="bold"), text_color=THEME["text"]).pack(pady=(0, 10), anchor="w")
        
        vibe = random.choice(self.engine.translations[lang]["encouragements"])
        ctk.CTkLabel(self.content_frame, text=vibe, font=ctk.CTkFont(size=18, slant="italic"), text_color=THEME["accent"]).pack(pady=(0, 40), anchor="w")

        # Bento Status
        status_box = ctk.CTkFrame(self.content_frame, corner_radius=25, fg_color=THEME["card"], height=120)
        status_box.pack(fill="x", pady=10)
        
        last_sync = self.engine.config_manager.config.get("last_sync") or ("Resting" if lang == "en" else "Rusten")
        sync_txt = f"Last secure sync: {last_sync}" if lang == "en" else f"Laatste beveiliging: {last_sync}"
        
        ctk.CTkLabel(status_box, text="🛡️", font=ctk.CTkFont(size=40)).pack(side="left", padx=30)
        ctk.CTkLabel(status_box, text=f"Bob is watching over you.\n{sync_txt}", font=ctk.CTkFont(size=16), text_color=THEME["text"], justify="left").pack(side="left")

        # Action Button
        btn_txt = "🫂 Give me a hug\n(Secure work now)" if lang == "en" else "🫂 Geef een knuffel\n(Werk nu beveiligen)"
        self.hug_btn = ctk.CTkButton(self.content_frame, text=btn_txt, font=ctk.CTkFont(size=22, weight="bold"), 
                                     fg_color=THEME["btn"], text_color=THEME["text"], hover_color=THEME["btn_hover"],
                                     height=120, corner_radius=25, command=self.hug_action)
        self.hug_btn.pack(fill="x", pady=30)
        
        self.prog_lbl = ctk.CTkLabel(self.content_frame, text="", font=ctk.CTkFont(size=14), text_color=THEME["accent"])
        self.prog_lbl.pack()

    def draw_diary(self):
        lang = self.engine.config_manager.config.get("language", "en")
        title = "Bob's Thoughts 📖" if lang == "en" else "Bob's Gedachten 📖"
        ctk.CTkLabel(self.content_frame, text=title, font=ctk.CTkFont(size=28, weight="bold"), text_color=THEME["text"]).pack(pady=(0, 20), anchor="w")
        
        self.log_box = ctk.CTkTextbox(self.content_frame, corner_radius=20, fg_color=THEME["card"], text_color=THEME["text"], font=ctk.CTkFont(family="Consolas", size=13))
        self.log_box.pack(fill="both", expand=True)
        
        try:
            if os.path.exists(self.engine.log_path):
                with open(self.engine.log_path, "r", encoding="utf-8") as f:
                    logs = f.readlines()
                    self.log_box.insert("1.0", "".join(logs[-50:]))
            else:
                self.log_box.insert("1.0", "No memories yet..." if lang == "en" else "Nog geen herinneringen...")
        except: pass

    def draw_settings(self):
        lang = self.engine.config_manager.config.get("language", "en")
        ctk.CTkLabel(self.content_frame, text="Preferences ⚙️" if lang == "en" else "Voorkeuren ⚙️", font=ctk.CTkFont(size=28, weight="bold"), text_color=THEME["text"]).pack(pady=(0, 20), anchor="w")
        
        # Directories
        ctk.CTkLabel(self.content_frame, text="Watched Folders:" if lang == "en" else "Bewaakte mappen:", text_color=THEME["text"]).pack(anchor="w")
        dirs = ", ".join(self.engine.config_manager.config.get("watched_directories", []))
        self.dir_ent = ctk.CTkEntry(self.content_frame, width=500, height=40, corner_radius=10, fg_color=THEME["card"], text_color=THEME["text"])
        self.dir_ent.insert(0, dirs)
        self.dir_ent.pack(pady=(5, 20), fill="x")
        
        # Shield Toggle
        self.shield_var = ctk.BooleanVar(value=self.engine.config_manager.config.get("secret_shield_enabled", True))
        ctk.CTkSwitch(self.content_frame, text="Secret Shield ACTIVE 🛡️", variable=self.shield_var, text_color=THEME["text"], progress_color=THEME["accent"]).pack(pady=10, anchor="w")
        
        ctk.CTkButton(self.content_frame, text="Save Settings" if lang == "en" else "Opslaan", fg_color=THEME["btn"], text_color=THEME["text"], corner_radius=10, command=self.save_settings).pack(pady=30)

    def hug_action(self):
        self.hug_btn.configure(state="disabled")
        def update_p(m):
            self.prog_lbl.configure(text=m)
            self.update()
        self.engine.secure_all(progress_callback=update_p)
        self.hug_btn.configure(state="normal")
        messagebox.showinfo("Bob", "Squeeze! Everything is tucked in. 🫂" if self.engine.config_manager.config["language"] == "en" else "Knuffel! Alles is veilig opgeborgen. 🫂")
        self.show_tab("home")

    def save_settings(self):
        dirs = [d.strip() for d in self.dir_ent.get().split(",") if d.strip()]
        self.engine.config_manager.config["watched_directories"] = dirs
        self.engine.config_manager.config["secret_shield_enabled"] = self.shield_var.get()
        self.engine.config_manager.save_config()
        messagebox.showinfo("Bob", "I've remembered your choices! 🦦")

if __name__ == "__main__":
    app = BobsCottage()
    app.mainloop()
