import customtkinter as ctk
from tkinter import messagebox

class StyleGallery(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bob's Style Gallery 🦦🎨")
        self.geometry("900x600")
        
        # Define our 6 Cute Palettes
        self.styles = {
            "1. Peach Mochi 🍑": {
                "bg": "#FFF9F0", "card": "#FFD1BA", "btn": "#FF8B94", "text": "#4A3F3F", "accent": "#FFF5BA"
            },
            "2. Strawberry Milk 🍓": {
                "bg": "#FFF4E0", "card": "#FFC0CB", "btn": "#FFB7B2", "text": "#4A3F3F", "accent": "#E57373"
            },
            "3. Sunset Cafe ☕": {
                "bg": "#FEF9EF", "card": "#FFD8B1", "btn": "#FFB347", "text": "#6D4C41", "accent": "#D4A373"
            },
            "4. Minty River 🌿": {
                "bg": "#F0FFF4", "card": "#C6F6D5", "btn": "#81E6D9", "text": "#2C7A7B", "accent": "#B2F5EA"
            },
            "5. Lavender Dream 💜": {
                "bg": "#FAF5FF", "card": "#E9D8FD", "btn": "#B794F4", "text": "#553C9A", "accent": "#D6BCFA"
            },
            "6. Golden Hour ☀️": {
                "bg": "#FFFDF0", "card": "#FEFCBF", "btn": "#F6AD55", "text": "#744210", "accent": "#FBD38D"
            }
        }

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Left Sidebar for Buttons
        self.sidebar = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.sidebar, text="Kies een sfeer:", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        for name in self.styles.keys():
            btn = ctk.CTkButton(self.sidebar, text=name, command=lambda n=name: self.apply_style(n),
                                 height=40, corner_radius=10)
            btn.pack(pady=10, padx=20, fill="x")

        # Right Preview Area
        self.preview_area = ctk.CTkFrame(self, corner_radius=30)
        self.preview_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.sample_card = ctk.CTkFrame(self.preview_area, corner_radius=25, width=400, height=300)
        self.sample_card.place(relx=0.5, rely=0.4, anchor="center")
        
        self.otter_label = ctk.CTkLabel(self.sample_card, text="🦦", font=ctk.CTkFont(size=80))
        self.otter_label.pack(pady=(30, 10))
        
        self.title_label = ctk.CTkLabel(self.sample_card, text="Hi Jonas! Ik ben Bob.", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack()
        
        self.msg_label = ctk.CTkLabel(self.sample_card, text="Zal ik je vandaag een knuffel geven?", font=ctk.CTkFont(size=14, slant="italic"))
        self.msg_label.pack(pady=10)
        
        self.action_btn = ctk.CTkButton(self.sample_card, text="Geef een knuffel 🫂", corner_radius=15, font=ctk.CTkFont(weight="bold"))
        self.action_btn.pack(pady=20, padx=40, fill="x")

        self.apply_style("1. Peach Mochi 🍑")

    def apply_style(self, name):
        s = self.styles[name]
        self.preview_area.configure(fg_color=s["bg"])
        self.sample_card.configure(fg_color=s["card"])
        self.otter_label.configure(text_color=s["text"])
        self.title_label.configure(text_color=s["text"])
        self.msg_label.configure(text_color=s["text"])
        self.action_btn.configure(fg_color=s["btn"], text_color="#FFFFFF" if name != "3. Sunset Cafe ☕" else s["text"])

if __name__ == "__main__":
    app = StyleGallery()
    app.mainloop()
