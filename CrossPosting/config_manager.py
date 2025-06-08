# config_manager.py

import json
import os

# Always store the config in the same folder as the running script
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(APP_DIR, "config.json")


def save_config(data: dict, filename: str = DEFAULT_CONFIG_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Configuration saved to {filename}")
    except Exception as e:
        print(f"❌ Failed to save config: {e}")

def load_config(filename: str = DEFAULT_CONFIG_FILE) -> dict:
    if not os.path.exists(filename):
        print(f"⚠️ Config file {filename} not found. Returning empty config.")
        return {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        return {}
