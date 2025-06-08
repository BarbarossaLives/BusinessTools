import os,json
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from PIL import Image
from discord_post import post_to_discord
from devto_post import post_to_devto
from mastadon_post import post_to_mastodon
from linkedin_post import share_on_linkedin
import webbrowser
from urllib.parse import quote
import pyperclip
from config_manager import load_config, save_config

from x_post import post_to_x



class CrossPostApp:
    def handle_post(self):
        print("Button Pushed")
        kofi_url = self.kofi_url_entry.get().strip()
        comment = self.comments_entry.get().strip()
        image_path = self.selected_image_path

        webhooks = [
            self.webhook_1_entry.get(),
            self.webhook_2_entry.get(),
            self.webhook_3_entry.get(),
            self.webhook_4_entry.get(),
            self.webhook_5_entry.get()
        ]

        post_to_discord(kofi_url, comment, webhooks)

        message_parts = [f"Check out my latest post on Ko-fi!\n{kofi_url}"]
        if comment:
            message_parts.append(comment)
        message = "\n\n".join(message_parts)

        # Call Mastodon posting function
        mastodon_url = self.mastodon_url_entry.get().strip()
        mastodon_token = self.mastodon_token_entry.get().strip()
        post_to_mastodon(mastodon_url, mastodon_token, message, image_path)

        # Dev.to posting 
        devto_key = self.devto_key_entry.get().strip()
        post_to_devto(devto_key, kofi_url, comment, image_path)

        share_on_linkedin(kofi_url, comment)

    CONFIG_FILE = "crosspost_cofig,json" 

    def load_configuration(self):
        config = load_config()
        if not config:
            return

        self.kofi_url_entry.delete(0, 'end')
        self.kofi_url_entry.insert(0, config.get("kofi_url", ""))

        self.comments_entry.delete(0, 'end')
        self.comments_entry.insert(0, config.get("comment", ""))

        self.mastodon_token_entry.delete(0, 'end')
        self.mastodon_token_entry.insert(0, config.get("mastodon_token", ""))
        self.mastodon_url_entry.delete(0, 'end')
        self.mastodon_url_entry.insert(0, config.get("mastodon_url", ""))

        self.devto_key_entry.delete(0, 'end')
        self.devto_key_entry.insert(0, config.get("devto_token", ""))

        

        for i in range(5):
            getattr(self, f"webhook_{i+1}_entry").delete(0, 'end')
            getattr(self, f"webhook_{i+1}_entry").insert(0, config.get(f"webhook_{i+1}", ""))

    def save_configuration(self):
        config = {
            "kofi_url": self.kofi_url_entry.get().strip(),
            "comment": self.comments_entry.get().strip(),
            "mastodon_token": self.mastodon_token_entry.get().strip(),
            "mastodon_url": self.mastodon_url_entry.get().strip(),
            "devto_token": self.devto_key_entry.get().strip(),

        }

        for i in range(5):
            config[f"webhook_{i+1}"] = getattr(self, f"webhook_{i+1}_entry").get().strip()

        save_config(config)



    def handle_image_upload(self):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif *.webp"), ("All files", "*.*")]
        filepath = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        if filepath:
            self.selected_image_path = filepath
            self.image_uploaded_label.config(text=f"Selected: {os.path.basename(filepath)}")


    def __init__(self):         
        self.root = root
        self.root.title("Crosspost Tools")
        self.root.geometry("1000x800")
        self.style = ttk.Style("cyborg")
        self.selected_image_path = None
        #self.cong = self.load_config()
       

        style = ttk.Style()
        style.configure(
            "large.TLabel",
            font=("Georgia", 24,"bold"),
            foreground="cyan",
            justify="center"
        )

        style = ttk.Style()
        style.configure(
            "normal.TLabel",
            font=("Georgia", 14)
            
        )

        style = ttk.Style()
        style.configure(
            "success.TButton",
            font=("Georgia", 24, "bold")
        )

        root.grid_columnconfigure(0,minsize=150)
        root.grid_columnconfigure(1,minsize=350)
        root.grid_columnconfigure(2,minsize=150)
        root.grid_columnconfigure(3,minsize=350)


        main_title = ttk.Label(self.root, text="Cross Posting Tool", style="large.TLabel")
        main_title.grid(row=0, column=0, columnspan=4, sticky="",pady=5)

        kofi_url_label = ttk.Label(self.root, text="KO-FI URL: ", style="normal.TLabel")
        kofi_url_label.grid(row=1, column=0, columnspan=2,pady=5)
        kofi_url_entry = ttk.Entry(self.root,bootstyle="primary")
        kofi_url_entry.grid(row=2, column=0, columnspan=2, pady=5)
        self.kofi_url_entry = kofi_url_entry

        discord_webhooks_label= ttk.Label(self.root,text="Discord Webhooks per Channel",style="normal.TLabel")
        discord_webhooks_label.grid(row=1,column=2, columnspan=2,pady=5)

        webhook_1_label = ttk.Label(self.root,text="Webhook 1:",style="normal.TLabel")
        webhook_1_label.grid(row=2, column=2,pady=5)
        webhook_1_entry = ttk.Entry(self.root,bootstyle="primary")
        webhook_1_entry.grid(row=2,column=3,pady=5)
        self.webhook_1_entry = webhook_1_entry

        webhook_2_label = ttk.Label(self.root,text="Webhook 2:",style="normal.TLabel")
        webhook_2_label.grid(row=3, column=2, pady=5)
        webhook_2_entry = ttk.Entry(self.root,bootstyle="primary")
        webhook_2_entry.grid(row=3,column=3, pady=5)
        self.webhook_2_entry = webhook_2_entry

        webhook_3_label = ttk.Label(self.root,text="Webhook 3:",style="normal.TLabel")
        webhook_3_label.grid(row=4, column=2, pady=5)
        webhook_3_entry = ttk.Entry(self.root,bootstyle="primary")
        webhook_3_entry.grid(row=4,column=3, pady=5)
        self.webhook_3_entry = webhook_3_entry

        webhook_4_label = ttk.Label(self.root,text="Webhook 4:",style="normal.TLabel")
        webhook_4_label.grid(row=5, column=2, pady=5)
        webhook_4_entry = ttk.Entry(self.root,bootstyle="primary")
        webhook_4_entry.grid(row=5,column=3, pady=5)
        self.webhook_4_entry = webhook_4_entry

        webhook_5_label = ttk.Label(self.root,text="Webhook 5:",style="normal.TLabel")
        webhook_5_label.grid(row=6, column=2, pady=5)
        webhook_5_entry = ttk.Entry(self.root,bootstyle="primary")
        webhook_5_entry.grid(row=6,column=3, pady=5)
        self.webhook_5_entry = webhook_5_entry

        comments_label = ttk.Label(self.root, text="Post Comments", style="normal.TLabel")
        comments_label.grid(row=3, column=0,columnspan=2,pady=5)
        comments_entry = ttk.Entry(self.root, bootstyle="primary")
        comments_entry.grid(row=4,column=0, columnspan=2,pady=5)
        self.comments_entry = comments_entry

        image_import_buttom = ttk.Button(self.root, text="Upload Image", bootstyle="primary", command=self.handle_image_upload)
        image_import_buttom.grid(row=5,column=0,columnspan=2,pady=5)

        image_uploaded_label = ttk.Label(self.root, text="image source", style="normal.TLabel")
        image_uploaded_label.grid(row=6, column=0, columnspan=2, pady=5)
        self.image_uploaded_label = image_uploaded_label

        blank_1 = ttk.Frame(self.root, height=50).grid(row=7,column=0,columnspan=4)

        mastodon_url_label = ttk.Label(self.root, text="Mastodon URL",style="normal.TLabel")
        mastodon_url_label.grid(row=8, column=0,pady=5)
        mastodon_url_entry = ttk.Entry(self.root,bootstyle="primary")
        mastodon_url_entry.grid(row=8, column=1,pady=5)
        self.mastodon_url_entry = mastodon_url_entry
        mastodon_token_label = ttk.Label(self.root, text="Mastodon Token",style="normal.TLabel")
        mastodon_token_label.grid(row=9, column=0,pady=5)
        mastodon_token_entry = ttk.Entry(self.root,bootstyle="primary")
        mastodon_token_entry.grid(row=9, column=1,pady=5)
        self.mastodon_token_entry = mastodon_token_entry

        devto_key_label = ttk.Label(self.root, text="Dev.to Key",style="normal.TLabel")
        devto_key_label.grid(row=10, column=0,pady=5)
        devto_key_entry = ttk.Entry(self.root, bootstyle = "primary")
        devto_key_entry.grid(row=10,column=1,pady=5)
        self.devto_key_entry = devto_key_entry

        linkedin_token_label = ttk.Label(self.root, text="LinkedIn doesn't all remote posting.  the tool will open a webbrowser with the message ready to post to LinkenIn",style="normal.TLabel", wraplength=550)
        linkedin_token_label.grid(row=11, column=0, columnspan=2,padx=5,pady=5)


        x_token_label = ttk.Label(self.root, text="X Posting to X from a outside tool requires a Paid account.  This account is $100 or more",wraplength=550,style="normal.TLabel")
        x_token_label.grid(row=12, column=0, columnspan=2, padx=5,pady=5)


        load_configuration_button = ttk.Button(self.root, text= "Load Config", command=self.load_configuration, bootstyle="primary")
        load_configuration_button.grid(row=8, column=2, columnspan=2)

        save_configuration_button = ttk.Button(self.root, text="Save Config",command=self.save_configuration, bootstyle="primary")
        save_configuration_button.grid(row=10, column=2, columnspan=2)

        post_button = ttk.Button(self.root, text="POST", style="success.TButton")
        post_button.grid(row=12, column=2, columnspan=2)
        post_button.configure(command=self.handle_post)

if __name__ == "__main__":
    root = ttk.Window(themename="cyborg")
    app = CrossPostApp()
    root.mainloop()
