# Social Media Analytics Fetcher

A suite of three Python scripts for tracking social media performance and online mentions of GIPF Namibia (Government Institutions Pension Fund).

---

## Scripts Overview

| Script | Purpose | Admin Access Required? |
|---|---|---|
| `Social Media Fetcher` | Fetch followers, engagements, mentions & sentiment from your own accounts | Yes |
| `GIPF_Audience_Analysis` | Deep audience analysis for any public account (default: `@gipfnamibia`) | No |
| `GIPF_Internet_Search.py` | Search the public internet for news, stories, and mentions of GIPF | No |

---

## Requirements

```
pip install requests tweepy google-api-python-client textblob feedparser python-dotenv
```

---

## Credentials Setup (.env)

All credentials are stored in a single `.env` file in the project root. Copy the template below, fill in your values, and save it as `.env`. The scripts will load it automatically.

```
# Facebook / Instagram (Meta Graph API)
FB_ACCESS_TOKEN=your_long_lived_page_access_token_here
FB_PAGE_ID=your_facebook_page_id_here
IG_USER_ID=your_instagram_business_account_id_here

# Twitter / X (API v2)
TW_BEARER_TOKEN=your_twitter_bearer_token_here
TW_USERNAME=YourHandleWithoutAt

# YouTube (Data API v3)
YT_API_KEY=your_youtube_data_api_key_here
YT_CHANNEL_ID=UCxxxxxxxxxxxxxxxxxxxxxxxx

# LinkedIn (Marketing API)
LI_ACCESS_TOKEN=your_linkedin_access_token_here
LI_ORG_ID=your_organization_id_number_here

# NewsAPI (GIPF Internet Search)
NEWSAPI_KEY=your_newsapi_key_here
```

The `.env` file is listed in `.gitignore` and will not be committed to git.

---

## Script 1: Social Media Fetcher

Fetches followers, engagements, mentions, and sentiment from Facebook, Instagram, Twitter/X, YouTube, and LinkedIn for accounts you manage. Outputs results to a CSV file.

### Where to Get Your Credentials

#### Facebook & Instagram (Meta Graph API)

- Go to https://developers.facebook.com
- Create an app → **Business** type
- Add **Facebook Login** and **Instagram Graph API** products
- Use the **Graph API Explorer** to generate a long-lived Page Access Token
- `FB_PAGE_ID`: go to your Facebook Page → **About** → scroll to the bottom
- `IG_USER_ID`: use Graph API Explorer → query `me/accounts` → then query the IG business account linked to your page

#### Twitter / X (API v2)

- Go to https://developer.twitter.com
- Apply for a developer account → create a **Project + App**
- Under your app's **Keys and Tokens** tab → copy the **Bearer Token**
- `TW_USERNAME`: your handle without the `@`

#### YouTube (Data API v3)

- Go to https://console.cloud.google.com
- Create a project → **APIs & Services** → Enable **YouTube Data API v3**
- **Credentials** → **Create API Key** → copy it
- `YT_CHANNEL_ID`: on YouTube, go to your channel → **About** → **Share** → **Copy channel ID** (starts with `UC...`)

#### LinkedIn (Marketing API)

- Go to https://www.linkedin.com/developers
- Create an app → associate it with a **LinkedIn Page**
- Request the **r_organization_social** permission
- Use OAuth 2.0 to generate an access token
- `LI_ORG_ID`: go to your LinkedIn Page → the number in the URL (e.g. `linkedin.com/company/123456789`)

### Usage

```
python "Social Media Fetcher"
```

Output is saved to `SocialMedia_<year>.csv`:

| Platform | Year | Number of Followers | Number of Engagements | Number of Mentions | Perception |
|----------|------|--------------------|-----------------------|--------------------|------------|

---

## Script 2: GIPF Audience Analysis

Performs deeper audience analysis for any public social media account (default: `@gipfnamibia`). Does not require account ownership or admin access.

### Credentials needed

| Platform | Credential | Where to get it |
|---|---|---|
| Twitter/X | Bearer Token | developer.twitter.com — free tier |
| YouTube | API Key | console.cloud.google.com — free tier |
| Facebook / Instagram / LinkedIn | None | Numbers entered manually at runtime |

Credentials (`TW_BEARER_TOKEN`, `YT_API_KEY`, `TW_USERNAME`, `YT_CHANNEL_ID`) are loaded from `.env`. For Facebook, Instagram, and LinkedIn the script will prompt you to enter the publicly visible numbers from each profile page at runtime.

### Usage

```
python "GIPF_Audience_Analysis"
```

Output is saved to `GIPF_Audience_Analysis_<year>.csv`:

| Platform | Year | Followers | Following | EngagementRate% | AvgEngagementPerPost | PostsPerMonth | FollowerGrade | AudienceQualityScore | Sentiment | TopPost |
|---|---|---|---|---|---|---|---|---|---|---|

### Engagement Grade key

| Grade | Engagement Rate |
|---|---|
| A+ | >= 6% |
| A  | >= 3% |
| B  | >= 1% |
| C  | >= 0.5% |
| D  | < 0.5% |

### Audience Quality Score (0–100)

- **60%** engagement rate — higher means more real, active followers
- **40%** follower/following ratio — higher means more organic growth

---

## Script 3: GIPF Internet Search

Searches the public internet for any news, stories, posts, events, or mentions of GIPF Namibia across multiple sources. No account ownership required.

**Keywords searched:** `gipfnamibia`, `GIPF Namibia`, `Government Institutions Pension Fund Namibia`

**Sources:**

| Source | Key Required? |
|---|---|
| Google News RSS | No |
| Bing News RSS | No |
| Reddit (public API) | No |
| NewsAPI | Yes — free key at newsapi.org |
| Twitter/X | Yes — Bearer Token (free dev tier) |

### Credentials needed

| Credential | Where to get it |
|---|---|
| `NEWSAPI_KEY` | https://newsapi.org/register — free developer account |
| `TW_BEARER_TOKEN` | https://developer.twitter.com — free tier |

Google News RSS, Bing News RSS, and Reddit require no credentials and will run automatically.

Credentials (`NEWSAPI_KEY`, `TW_BEARER_TOKEN`) are loaded from `.env`. If either is missing, that source is skipped and the rest still run.

### Usage

```
python GIPF_Internet_Search.py
```

Output is saved to `GIPF_Internet_Search_<year>.csv`:

| Source | Date | Title | URL | Summary | Topics | Sentiment |
|---|---|---|---|---|---|---|

The script also prints a summary to the console showing total results, top topics, overall sentiment breakdown, and results per source.

### Topic tags

Topics are automatically detected from article text and can include: Pension, Retirement, Investment, Fund, Namibia, Event, Seminar/Event, AGM, Benefits, Contributions, Members, Governance, Annual Report, Financial Results, Fraud/Risk, Death Benefits, Housing Loan, Social Media, Stories.

### Sentiment values

| Value | Meaning |
|---|---|
| Positive | Polarity score > 0.1 |
| Neutral | Polarity score between -0.1 and 0.1 |
| Negative | Polarity score < -0.1 |
