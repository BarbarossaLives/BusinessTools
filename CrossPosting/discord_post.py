import requests

def post_to_discord(webhook_url, message, image_path=None):
    """
    Post a message (and optional image) to a Discord channel using a webhook URL.
    """
    data = {"content": message}
    files = {}

    if image_path:
        try:
            files["file"] = open(image_path, "rb")
        except Exception as e:
            return f"⚠️ Error opening image: {e}"

    try:
        response = requests.post(webhook_url, data=data, files=files if files else None)
        if response.status_code == 204:
            return "✅ Posted successfully."
        else:
            return f"❌ Discord error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Request failed: {e}"
