import os,json
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from PIL import Image

CONFIG_FILE = "crosspost_cofig,json" 

class CrossPostApp:
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

        style.configure(
            "normal.TLabel",
            font=("Georgia", 14),
            
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

        discord_webhooks_label= ttk.Label(self.root,text="Discord Webhooks per Channel",style="normal.TLabel")
        discord_webhooks_label.grid(row=1,column=2, columnspan=2,pady=5)

        webhook_1_label = ttk.Label(self.root,text="Webhook 1:",style="normal.TLabel")
        webhook_1_label.grid(row=2, column=2,pady=5)
        webhook_1_entry = ttk.Entry(self.root,bootstyle="primary")
        webhook_1_entry.grid(row=2,column=3,pady=5)

        webhook_2_label = ttk.Label(self.root,text="Webhook 2:",style="normal.TLabel")
        webhook_2_label.grid(row=3, column=2, pady=5)
        webhook_2_entry = ttk.Entry(self.root,bootstyle="primary")
        webhook_2_entry.grid(row=3,column=3, pady=5)

        webhook_3_label = ttk.Label(self.root,text="Webhook 3:",style="normal.TLabel")
        webhook_3_label.grid(row=4, column=2, pady=5)
        webhook_3_entry = ttk.Entry(self.root,bootstyle="primary")
        webhook_3_entry.grid(row=4,column=3, pady=5)

        webhook_4_label = ttk.Label(self.root,text="Webhook 4:",style="normal.TLabel")
        webhook_4_label.grid(row=5, column=2, pady=5)
        webhook_4_entry = ttk.Entry(self.root,bootstyle="primary")
        webhook_4_entry.grid(row=5,column=3, pady=5)

        webhook_5_label = ttk.Label(self.root,text="Webhook 5:",style="normal.TLabel")
        webhook_5_label.grid(row=6, column=2, pady=5)
        webhook_5_entry = ttk.Entry(self.root,bootstyle="primary")
        webhook_5_entry.grid(row=6,column=3, pady=5)

        comments_label = ttk.Label(self.root, text="Post Comments", style="normal.TLabel")
        comments_label.grid(row=3, column=0,columnspan=2,pady=5)
        comments_entry = ttk.Entry(self.root, bootstyle="primary")
        comments_entry.grid(row=4,column=0, columnspan=2,pady=5)

        image_import_buttom = ttk.Button(self.root, text="Upload Image")
        image_import_buttom.grid(row=5,column=0,columnspan=2,pady=5)
        image_uploaded_label = ttk.Label(self.root, text="image source")
        image_uploaded_label.grid(row=6, column=0, columnspan=2, pady=5)

        blank_1 = ttk.Frame(self.root, height=50).grid(row=7,column=0,columnspan=4)

        mastodon_url_label = ttk.Label(self.root, text="Mastodon URL")
        mastodon_url_label.grid(row=8, column=0,pady=5)
        mastodon_url_entry = ttk.Entry(self.root,bootstyle="primary")
        mastodon_url_entry.grid(row=8, column=1,pady=5)
        mastodon_token_label = ttk.Label(self.root, text="Mastodon Token")
        mastodon_token_label.grid(row=9, column=0,pady=5)
        mastodon_token_entry = ttk.Entry(self.root,bootstyle="primary")
        mastodon_token_entry.grid(row=9, column=1,pady=5)

        devto_key_label = ttk.Label(self.root, text="Dev,to Key")
        devto_key_label.grid(row=9, column=0,pady=5)


if __name__ == "__main__":
    root = ttk.Window(themename="cyborg")
    app = CrossPostApp()
    root.mainloop()
