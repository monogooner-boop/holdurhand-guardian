import tkinter as tk
from tkinter import messagebox
import os
import subprocess

class BobsCottage:
    def __init__(self, root):
        self.root = root
        self.root.title("Bob's Riverside Cottage 🦦")
        self.root.geometry("450x350")
        self.root.configure(bg="#F0F4F8") # Soft, calming light blue/grey background
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Title
        title_label = tk.Label(root, text="Welcome to Bob's Cottage 🦦", font=("Segoe UI", 16, "bold"), bg="#F0F4F8", fg="#2C3E50")
        title_label.pack(pady=(25, 5))
        
        # Subtitle
        subtitle_label = tk.Label(root, text="Take a deep breath. You are safe here.", font=("Segoe UI", 10, "italic"), bg="#F0F4F8", fg="#7F8C8D")
        subtitle_label.pack(pady=(0, 20))
        
        # Buttons with warm terminology
        self.create_button("Give me a hug (Secure my work) 🫂", "#A3E4D7", self.hug_action)
        self.create_button("Read my diary 📖", "#F9E79F", self.diary_action)
        self.create_button("Watch over me 🛡️", "#FAD7A1", self.watch_action)
        
        # Footer
        footer_label = tk.Label(root, text="Bob is silently watching over your PC. No stress allowed.", font=("Segoe UI", 8), bg="#F0F4F8", fg="#BDC3C7")
        footer_label.pack(side="bottom", pady=15)

    def create_button(self, text, color, command):
        btn = tk.Button(self.root, text=text, font=("Segoe UI", 11), bg=color, fg="#2C3E50", 
                        activebackground="#FFFFFF", relief="flat", padx=10, pady=5, cursor="hand2", command=command)
        btn.pack(fill="x", padx=50, pady=8)

    def hug_action(self):
        # In the future, this will trigger bob-engine.py
        messagebox.showinfo("Bob says...", "🫂 *Squeeze*\n\nI am holding your hand. Everything is safe, Jonas. You're doing amazing today.")
        
    def diary_action(self):
        log_path = r"C:\Users\spyder\Projects\holdurhand-guardian\COMFORT_LOG.md"
        try:
            os.startfile(log_path) # Opens the file in the default text editor
        except:
            messagebox.showinfo("Bob's Diary", "📖 Today was a good day. I kept your dreams safe.")
        
    def watch_action(self):
        messagebox.showinfo("Bob's Shield", "🛡️ I'm guarding the perimeter! No secrets will leak, and no work will be lost on my watch. You just focus on creating.")

if __name__ == "__main__":
    root = tk.Tk()
    # A small trick to make it look a bit more modern on Windows
    try:
        root.attributes("-alpha", 0.98) # Slight transparency
    except:
        pass
    app = BobsCottage(root)
    root.mainloop()
