### 🔄 What Gets Posted

When you click **POST**, your content is cross-posted to:

- 🧵 Up to 5 Discord channels via webhooks
- ✍️ Dev.to
- 🐘 Mastodon
- 🐦 X (Twitter)
- 💼 LinkedIn

**Message Structure:**

- ✅ Ko-fi URL (required)
- 💬 Comment (optional, adds personal context)
- 🖼️ Image (optional, uploaded if attached)


🔗 Setting Up Discord Webhooks
To use the Discord integration in the Cross Posting Tool, follow these steps:

Open Your Discord Server Settings:

Right-click on your server name and select "Server Settings" > "Integrations".

Create a Webhook:

Click on "Create Webhook".

Give it a name, select the channel, and copy the Webhook URL.

Paste the Webhook into the App:

In the "Discord Webhooks per Channel" section of the app, paste your webhook URL into one of the five fields.

Repeat:

You can create and paste up to 5 webhooks (one per channel if desired).

Once configured, clicking the POST button will send your post (including comments and optionally an image) to all listed webhooks.


Get Your Access Token:

Go to your Mastodon instance (e.g., https://mastodon.social).

Go to Settings → Development → New application.

Check write:statuses and save.

Copy the access token.

Fill in the App:

Paste the token into the Mastodon Token field.

Enter your instance URL (e.g., https://mastodon.social) in Mastodon URL.

Click POST:

Your Ko-fi post, comment, and image (if any) will be published to your Mastodon timeline.



✍️ Dev.to Integration Setup
To post updates to your Dev.to blog:

Get Your API Key:

Log in to Dev.to.

Visit your settings at https://dev.to/settings/account.

Scroll to the DEV API Keys section.

Generate and copy a new key.

Fill in the App:

Paste the API key into the Dev.to Key field.

Click POST:

The app will publish a post with:

The Ko-fi post link.

Your optional comment.

Your image, if uploaded (referenced as markdown, must be hosted manually for display).




💼 LinkedIn Integration Setup


🐦 X (Twitter) Integration Setup
To post to your X (Twitter) feed:

Get Your Bearer Token:

Go to developer.twitter.com and create a developer project/app.

Generate a Bearer Token for API v2 with tweet.write permission.

Paste the Token:

Copy your Bearer Token and paste it into the X Token field in the app.

Click POST:

The app will tweet the Ko-fi URL and your comment (if provided).



🐦 X (Twitter) Integration Setup
To post to your X (Twitter) feed:

Get Your Bearer Token:

Go to developer.twitter.com and create a developer project/app.

Generate a Bearer Token for API v2 with tweet.write permission.

Paste the Token:

Copy your Bearer Token and paste it into the X Token field in the app.

Click POST:

The app will tweet the Ko-fi URL and your comment (if provided).