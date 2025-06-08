# x_post.py
import requests

def post_to_x(bearer_token, kofi_url, comment=None):
    if not bearer_token or not kofi_url:
        print("X bearer token and Ko-fi URL required.")
        return

    message = f"Check out my latest Ko-fi post: {kofi_url}"
    if comment:
        message += f"\n\n{comment}"

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": message
    }

    try:
        response = requests.post("https://api.twitter.com/2/tweets", headers=headers, json=payload)
        response.raise_for_status()
        print("Posted to X.")
    except Exception as e:
        print(f"Failed to post to X: {e}")
