from requests_oauthlib import OAuth1Session

# Replace with your credentials
consumer_key = "wmNy2tD7GaMTNiit6guyo8TLI"
consumer_secret = "1G95URKoPqreRBQPVgkFGhCzccvFXrlPPSzuoMgbAN3MK6rHDc"
access_token = "1704865127877562368-EchBf0RrFpDjLnT9sKuu9ruQ3IRhgg"
access_token_secret = "QbK61oAocRgwgJeKewFrL1b8T3GCaSe54fUtRh7n5OPrR"

tweet_text = "This is a test tweet sent from Python via Twitter API v1.1. #crosspost"

twitter = OAuth1Session(
    client_key=consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret
)

response = twitter.post(
    "https://api.twitter.com/1.1/statuses/update.json",
    params={"status": tweet_text}
)

print("Status Code:", response.status_code)
print("Response:", response.text)
