import json
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import ttkbootstrap as tb
#from discord_post import post_to_discord
#from mastodon_post import post_to_mastodon
#from devto_post import post_to_devto
#from linkedin_post import post_to_linkedin
#from x_post import post_to_x

CONFIG_FILE = "crosspost_config.json"

class CrossPostApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crosspost Tool")
        self.root.geometry("1100x800")  # Increased window width
        self.style = tb.Style("superhero")
        self.selected_image_path = None
        self.config = self.load_config()

        main_frame = tb.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.kofi_label = tb.Label(main_frame, "Ko-fi Post URL:")
        self.kofi_entry = tb.Entry(main_frame)
        self.desc_label = tb.Label(main_frame, text="Short Description:")
        self.desc_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
        self.desc_text = tk.Text(main_frame, height=4, width=100)
        self.desc_text.grid(row=2, column=0, columnspan=2, pady=5)

        self.img_button = tb.Button(main_frame, text="Select Image", command=self.select_image)
        self.img_button.grid(row=3, column=0, pady=5, sticky="w")
        self.image_label = tb.Label(main_frame)
        self.image_label.grid(row=3, column=1, pady=5, sticky="w")



        # 2-column layout for API tokens
        self.mastodon_url_entry = self.create_labeled_entry(main_frame, "Mastodon Instance URL:", 9, 0)
        self.mastodon_token_entry = self.create_labeled_entry(main_frame, "Mastodon Access Token:", 9, 1, password=True)
        self.devto_key_entry = self.create_labeled_entry(main_frame, "Dev.to API Key:", 10, 0)
        self.linkedin_token_entry = self.create_labeled_entry(main_frame, "LinkedIn Token:", 10, 1, password=True)
        self.x_token_entry = self.create_labeled_entry(main_frame, "X (Twitter) Token:", 11, 0)

        self.post_button = tb.Button(main_frame, text="Post to All Platforms", bootstyle="success", command=self.post_to_all)
        self.post_button.grid(row=12, column=0, pady=10, sticky="w")

        self.save_button = tb.Button(main_frame, text="Save Config", bootstyle="info", command=self.save_config)
        self.save_button.grid(row=12, column=1, pady=10, sticky="w")

        self.log_text = tk.Text(main_frame, height=8, width=120, state='disabled')
        self.log_text.grid(row=13, column=0, columnspan=2, pady=5)

        self.populate_fields()




        self.webhook_entries = [self.create_labeled_entry(main_frame, f"Discord Webhook URL {i + 1}:", 4 + i, 0, 2) for i in range(5)]        

    def create_labeled_entry(self, parent, label_text, row, column, columnspan=1, password=False):
        label = tb.Label(parent, text=label_text)
        label.grid(row=row, column=column, sticky="w", pady=2)
        entry = tb.Entry(parent, width=60, show="*" if password else "")
        entry.grid(row=row, column=column + 1 if columnspan == 1 else column, columnspan=columnspan, pady=2, sticky="w")
        return entry

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_config(self):
        data = {
            "discord_webhooks": [e.get().strip() for e in self.webhook_entries],
            "mastodon_url": self.mastodon_url_entry.get().strip(),
            "mastodon_token": self.mastodon_token_entry.get().strip(),
            "devto_api_key": self.devto_key_entry.get().strip(),
            "linkedin_token": self.linkedin_token_entry.get().strip(),
            "x_token": self.x_token_entry.get().strip(),
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
        self.log("✅ Config saved.")

    def populate_fields(self):
        for i, entry in enumerate(self.webhook_entries):
            try:
                entry.insert(0, self.config.get("discord_webhooks", [])[i])
            except IndexError:
                continue
        self.mastodon_url_entry.insert(0, self.config.get("mastodon_url", ""))
        self.mastodon_token_entry.insert(0, self.config.get("mastodon_token", ""))
        self.devto_key_entry.insert(0, self.config.get("devto_api_key", ""))
        self.linkedin_token_entry.insert(0, self.config.get("linkedin_token", ""))
        self.x_token_entry.insert(0, self.config.get("x_token", ""))

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(image)
            self.selected_image_path = file_path
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            self.log("✅ Image selected and scaled.")

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def post_to_all(self):
        kofi_link = self.kofi_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        message = f"{description}\n{kofi_link}" if kofi_link else description

        for i, entry in enumerate(self.webhook_entries):
            url = entry.get().strip()
            if url:
                result = post_to_discord(url, message, self.selected_image_path)
                self.log(f"Discord {i+1}: {result}")

        result = post_to_mastodon(
            self.mastodon_url_entry.get().strip(),
            self.mastodon_token_entry.get().strip(),
            message
        )
        self.log(f"Mastodon: {result}")

        result = post_to_devto(
            self.devto_key_entry.get().strip(),
            "Ko-fi Update",
            description,
            kofi_link
        )
        self.log(f"Dev.to: {result}")

        result = post_to_linkedin(
            self.linkedin_token_entry.get().strip(),
            message
        )
        self.log(f"LinkedIn: {result}")

        result = post_to_x(
            self.x_token_entry.get().strip(),
            message
        )
        self.log(f"X: {result}")

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = CrossPostApp(root)
    root.mainloop()





        # !Discord Channel Posts
        discord_label_frame = ttk.LabelFrame(self.root,text="Discord Channels", borderwidth=4, bootstyle="primary")
        discord_label_frame.grid(column=1)
        self.webhook_entries = [self.create_webhook_entry(discord_label_frame, f"Discord Webhhok URL {i + 1}:",7 + i) for i in range(6)]




        #dev.to

        #LinkedIn

        # X/twitter

        # Post to all button

        # Save Config

        # Autofill - Send to all - Log  


#Add custom styles to increase the sizr of the text on the label frame

        title_label = ttk.Label(self.root, text="Barbarossa Lives Posting Tool", font=("Arial", 20),justify="center")
        title_label.grid(row=1,column=0, columnspan=2)
        
        main_frame_label = ttk.LabelFrame(self.root,text="Posting Data", borderwidth=10, bootstyle="primary")
        main_frame_label.grid(row=2,column=0, sticky="e",padx=20)



        # Original Ko-fi URL to cross post
        kofi_label= ttk.Label(main_frame_label, text= "KO-FI Post URL:", bootstyle="primary")
        kofi_label.pack(pady=10)
        kofi_entry = ttk.Entry(main_frame_label, text="KO-FI post address", width=75, bootstyle= "primary")
        kofi_entry.pack()

        # additional or original text to add to the post
        post_text_label = ttk.Label(main_frame_label,text= " Post Text", bootstyle = "primary" )
        post_text_label.pack(pady=10)
        post_text_entry = ttk.Text(main_frame_label, width= 55, height=3)
        post_text_entry.pack(pady=10)

        #Additional or original picture
        select_image_button = ttk.Button(main_frame_label, text="Select Image", command="", bootstyle="primary")
        select_image_button.pack(pady=10)
        select_image_selection = ttk.Text(main_frame_label,height=1, width = 55)
        select_image_selection.pack(pady=10)

        # !Discord Channel Posts
        discord_label_frame = ttk.LabelFrame(self.root,text="Discord Channels", borderwidth=4, bootstyle="primary")
        discord_label_frame.grid(row=2,column=1,padx=10)
        self.webhook_entries = [self.create_webhook_entry(discord_label_frame, f"Discord Webhhok URL {i + 1}:",7 + i) for i in range(6)]


        # Other Posting Site Addresses
        other_platforms_label = ttk.LabelFrame(self.root,text="Other posting sites", borderwidth=4,bootstyle="primary")
        other_platforms_label.grid(row=2,column=1 )

        # Mastodon
        mastodon_url_label = ttk.Label(discord_label_frame, text="Mastodon URL:",bootstyle="primary")
        mastodon_url_label.pack(pady=4)
        mastodon_url_entry = ttk.Entry(discord_label_frame, width= 45, bootstyle="primary")
        mastodon_url_entry.pack(pady=4)
        mastondon_token_label = ttk.Label(discord_label_frame, text="Mastodon Token:", bootstyle="primary")
        mastondon_token_label.pack(pady=4)
        mastodon_url_entry.pack()


    def create_webhook_entry(self, parent, label_text, row, password = False):
        label = ttk.Label(parent, text=label_text)
        label.grid(row = row, column=0, sticky="w", pady=2)
        entry = ttk.Entry(parent, width=45, show="*" if 
        password else "")
        entry.grid(row=row, column=1,padx=20, pady=11, sticky="w")
        return entry

