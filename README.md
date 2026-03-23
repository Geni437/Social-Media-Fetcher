# Social Media Analytics Fetcher

Fetches followers, engagements, mentions, and sentiment perception from Facebook, Instagram, Twitter/X, YouTube, and LinkedIn. Outputs results to a CSV file.

---

## Requirements

```
pip install requests tweepy google-api-python-client textblob
```

---

## Setup — Where to Get Your Credentials

### Facebook & Instagram (Meta Graph API)

- Go to https://developers.facebook.com
- Create an app → **Business** type
- Add **Facebook Login** and **Instagram Graph API** products
- Use the **Graph API Explorer** to generate a long-lived Page Access Token
- `FB_PAGE_ID`: go to your Facebook Page → **About** → scroll to the bottom
- `IG_USER_ID`: use Graph API Explorer → query `me/accounts` → then query the IG business account linked to your page

### Twitter / X (API v2)

- Go to https://developer.twitter.com
- Apply for a developer account → create a **Project + App**
- Under your app's **Keys and Tokens** tab → copy the **Bearer Token**
- `TW_USERNAME`: your handle without the `@`

### YouTube (Data API v3)

- Go to https://console.cloud.google.com
- Create a project → **APIs & Services** → Enable **YouTube Data API v3**
- **Credentials** → **Create API Key** → copy it
- `YT_CHANNEL_ID`: on YouTube, go to your channel → **About** → **Share** → **Copy channel ID** (starts with `UC...`)

### LinkedIn (Marketing API)

- Go to https://www.linkedin.com/developers
- Create an app → associate it with a **LinkedIn Page**
- Request the **r_organization_social** permission
- Use OAuth 2.0 to generate an access token
- `LI_ORG_ID`: go to your LinkedIn Page → the number in the URL (e.g. `linkedin.com/company/123456789`)

---

## Configuration

Open `Social Media Fetcher` and fill in your credentials at the top of the file:

```python
FB_ACCESS_TOKEN = "your_long_lived_page_access_token_here"
FB_PAGE_ID      = "your_facebook_page_id_here"
IG_USER_ID      = "your_instagram_business_account_id_here"

TW_BEARER_TOKEN = "your_twitter_bearer_token_here"
TW_USERNAME     = "YourHandleWithoutAt"

YT_API_KEY      = "your_youtube_data_api_key_here"
YT_CHANNEL_ID   = "UCxxxxxxxxxxxxxxxxxxxxxxxx"

LI_ACCESS_TOKEN = "your_linkedin_access_token_here"
LI_ORG_ID       = "your_organization_id_number_here"
```

---

## Usage

```
python "Social Media Fetcher"
```

Output is saved to `SocialMedia_<year>.csv` with the columns:

| Platform | Year | Number of Followers | Number of Engagements | Number of Mentions | Perception |
|----------|------|--------------------|-----------------------|--------------------|------------|
