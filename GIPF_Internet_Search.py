"""
GIPF Internet Search & Story Aggregator
=========================================
Searches the public internet for any news, stories, posts, events,
or mentions of GIPF Namibia across multiple sources.

Keywords searched:
    - gipfnamibia
    - GIPF
    - Government Institutions Pension Fund

Sources:
    1. Google News RSS       -- free, no key required
    2. NewsAPI               -- free developer key (newsapi.org)
    3. Reddit                -- public JSON API, no key required
    4. Twitter/X             -- Bearer Token (developer.twitter.com free tier)
    5. Bing News RSS         -- free, no key required

Output:
    GIPF_Internet_Search_YYYY.csv
    Columns: Source | Date | Title | URL | Summary | Topics | Sentiment

Requirements:
    pip install requests feedparser textblob
"""

import csv
import time
import html
import re
from datetime import datetime, timezone
from urllib.parse import quote_plus

import requests

try:
    import feedparser
except ImportError:
    feedparser = None

try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None

try:
    import tweepy
except ImportError:
    tweepy = None


# ──────────────────────────────────────────────────────────────────────────────
# CREDENTIALS
# ──────────────────────────────────────────────────────────────────────────────

# NewsAPI — get a free key at https://newsapi.org/register
NEWSAPI_KEY = "your_newsapi_key_here"

# Twitter/X Bearer Token — developer.twitter.com (free tier)
TW_BEARER_TOKEN = "your_twitter_bearer_token_here"

# ──────────────────────────────────────────────────────────────────────────────

KEYWORDS = [
    "gipfnamibia",
    "GIPF Namibia",
    "Government Institutions Pension Fund Namibia",
]

YEAR        = datetime.now().year
OUTPUT_FILE = f"GIPF_Internet_Search_{YEAR}.csv"
FIELDNAMES  = ["Source", "Date", "Title", "URL", "Summary", "Topics", "Sentiment"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; GIPFResearchBot/1.0; "
        "+https://github.com/research)"
    )
}


# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def clean(text: str) -> str:
    """Strip HTML tags and normalise whitespace."""
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def get_sentiment(text: str) -> str:
    if not TextBlob or not text:
        return "N/A"
    score = TextBlob(text).sentiment.polarity
    if score > 0.1:
        return "Positive"
    elif score < -0.1:
        return "Negative"
    return "Neutral"


def guess_topics(text: str) -> str:
    """
    Rough topic tagging based on keyword presence.
    Returns a comma-separated string of matched topics.
    """
    text_lower = text.lower()
    topic_map = {
        "pension":        "Pension",
        "retirement":     "Retirement",
        "investment":     "Investment",
        "fund":           "Fund",
        "namibia":        "Namibia",
        "event":          "Event",
        "seminar":        "Seminar/Event",
        "workshop":       "Seminar/Event",
        "indaba":         "Seminar/Event",
        "agm":            "AGM",
        "annual general": "AGM",
        "benefit":        "Benefits",
        "contribution":   "Contributions",
        "member":         "Members",
        "governance":     "Governance",
        "trustee":        "Governance",
        "board":          "Governance",
        "annual report":  "Annual Report",
        "financial":      "Financial Results",
        "dividend":       "Financial Results",
        "interest rate":  "Financial Results",
        "fraud":          "Fraud/Risk",
        "scam":           "Fraud/Risk",
        "warning":        "Fraud/Risk",
        "death benefit":  "Death Benefits",
        "housing":        "Housing Loan",
        "loan":           "Housing Loan",
        "social media":   "Social Media",
        "story":          "Stories",
    }
    found = []
    seen  = set()
    for kw, label in topic_map.items():
        if kw in text_lower and label not in seen:
            found.append(label)
            seen.add(label)
    return ", ".join(found) if found else "General"


def make_row(source, date, title, url, summary):
    full_text = f"{title} {summary}"
    return {
        "Source":    source,
        "Date":      date,
        "Title":     clean(title),
        "URL":       url,
        "Summary":   clean(summary)[:500],
        "Topics":    guess_topics(full_text),
        "Sentiment": get_sentiment(clean(full_text)),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 1. GOOGLE NEWS RSS  (no key required)
# ──────────────────────────────────────────────────────────────────────────────

def search_google_news() -> list:
    if not feedparser:
        print("  [Google News] feedparser not installed — skipping.")
        print("  Run: pip install feedparser")
        return []

    results = []
    for kw in KEYWORDS:
        url = f"https://news.google.com/rss/search?q={quote_plus(kw)}&hl=en&gl=NA&ceid=NA:en"
        print(f"  [Google News] Searching: {kw}")
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                pub = entry.get("published", "")
                try:
                    date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d %H:%M")
                except Exception:
                    date = pub
                results.append(make_row(
                    source  = "Google News",
                    date    = date,
                    title   = entry.get("title", ""),
                    url     = entry.get("link", ""),
                    summary = entry.get("summary", ""),
                ))
            print(f"    Found {len(feed.entries)} articles")
            time.sleep(1)
        except Exception as e:
            print(f"    Error: {e}")

    return results


# ──────────────────────────────────────────────────────────────────────────────
# 2. BING NEWS RSS  (no key required)
# ──────────────────────────────────────────────────────────────────────────────

def search_bing_news() -> list:
    if not feedparser:
        print("  [Bing News] feedparser not installed — skipping.")
        return []

    results = []
    for kw in KEYWORDS:
        url = f"https://www.bing.com/news/search?q={quote_plus(kw)}&format=rss"
        print(f"  [Bing News] Searching: {kw}")
        try:
            feed = feedparser.parse(url, request_headers=HEADERS)
            for entry in feed.entries:
                pub = entry.get("published", "")
                try:
                    date = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d %H:%M")
                except Exception:
                    date = pub
                results.append(make_row(
                    source  = "Bing News",
                    date    = date,
                    title   = entry.get("title", ""),
                    url     = entry.get("link", ""),
                    summary = entry.get("summary", ""),
                ))
            print(f"    Found {len(feed.entries)} articles")
            time.sleep(1)
        except Exception as e:
            print(f"    Error: {e}")

    return results


# ──────────────────────────────────────────────────────────────────────────────
# 3. NEWSAPI  (free key — newsapi.org/register)
# ──────────────────────────────────────────────────────────────────────────────

def search_newsapi() -> list:
    if NEWSAPI_KEY == "your_newsapi_key_here":
        print("  [NewsAPI] No key set — skipping. Get a free key at newsapi.org")
        return []

    results = []
    for kw in KEYWORDS:
        print(f"  [NewsAPI] Searching: {kw}")
        try:
            r = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q":        kw,
                    "sortBy":   "publishedAt",
                    "language": "en",
                    "pageSize": 50,
                    "apiKey":   NEWSAPI_KEY,
                },
                timeout=15,
            )
            r.raise_for_status()
            articles = r.json().get("articles", [])
            for a in articles:
                date = (a.get("publishedAt") or "")[:16].replace("T", " ")
                results.append(make_row(
                    source  = f"NewsAPI ({a.get('source', {}).get('name', 'Unknown')})",
                    date    = date,
                    title   = a.get("title", ""),
                    url     = a.get("url", ""),
                    summary = a.get("description") or a.get("content") or "",
                ))
            print(f"    Found {len(articles)} articles")
            time.sleep(1)
        except Exception as e:
            print(f"    Error: {e}")

    return results


# ──────────────────────────────────────────────────────────────────────────────
# 4. REDDIT  (public JSON API — no key required)
# ──────────────────────────────────────────────────────────────────────────────

def search_reddit() -> list:
    results = []
    for kw in KEYWORDS:
        print(f"  [Reddit] Searching: {kw}")
        try:
            r = requests.get(
                "https://www.reddit.com/search.json",
                params={"q": kw, "sort": "new", "limit": 50, "t": "all"},
                headers=HEADERS,
                timeout=15,
            )
            r.raise_for_status()
            posts = r.json().get("data", {}).get("children", [])
            for post in posts:
                d = post.get("data", {})
                ts   = d.get("created_utc", 0)
                date = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M") if ts else ""
                results.append(make_row(
                    source  = f"Reddit r/{d.get('subreddit', 'unknown')}",
                    date    = date,
                    title   = d.get("title", ""),
                    url     = "https://reddit.com" + d.get("permalink", ""),
                    summary = d.get("selftext", "")[:400],
                ))
            print(f"    Found {len(posts)} posts")
            time.sleep(2)  # Reddit rate limit is strict
        except Exception as e:
            print(f"    Error: {e}")

    return results


# ──────────────────────────────────────────────────────────────────────────────
# 5. TWITTER / X  (Bearer Token — free dev tier)
# ──────────────────────────────────────────────────────────────────────────────

def search_twitter() -> list:
    if TW_BEARER_TOKEN == "your_twitter_bearer_token_here":
        print("  [Twitter/X] No Bearer Token set — skipping.")
        return []
    if not tweepy:
        print("  [Twitter/X] tweepy not installed — run: pip install tweepy")
        return []

    results  = []
    client   = tweepy.Client(bearer_token=TW_BEARER_TOKEN, wait_on_rate_limit=True)

    queries  = [
        "gipfnamibia",
        '"GIPF" Namibia',
        '"Government Institutions Pension Fund"',
    ]

    for q in queries:
        print(f"  [Twitter/X] Searching: {q}")
        try:
            resp = client.search_recent_tweets(
                query       = f"{q} -is:retweet lang:en",
                max_results = 100,
                tweet_fields= ["created_at", "text", "public_metrics", "author_id"],
            )
            tweets = resp.data or []
            for t in tweets:
                date = t.created_at.strftime("%Y-%m-%d %H:%M") if t.created_at else ""
                m    = t.public_metrics or {}
                eng  = (m.get("like_count", 0) + m.get("retweet_count", 0) +
                        m.get("reply_count", 0) + m.get("quote_count", 0))
                summary = (f"Likes:{m.get('like_count',0)} "
                           f"Retweets:{m.get('retweet_count',0)} "
                           f"Replies:{m.get('reply_count',0)} "
                           f"Quotes:{m.get('quote_count',0)} "
                           f"| {t.text[:300]}")
                results.append(make_row(
                    source  = "Twitter/X",
                    date    = date,
                    title   = t.text[:140],
                    url     = f"https://twitter.com/i/web/status/{t.id}",
                    summary = summary,
                ))
            print(f"    Found {len(tweets)} tweets")
            time.sleep(2)
        except Exception as e:
            print(f"    Error: {e}")

    return results


# ──────────────────────────────────────────────────────────────────────────────
# DEDUPLICATION
# ──────────────────────────────────────────────────────────────────────────────

def deduplicate(rows: list) -> list:
    """Remove duplicate URLs; keep first occurrence."""
    seen = set()
    out  = []
    for row in rows:
        key = row["URL"].split("?")[0]   # strip query params
        if key not in seen and key:
            seen.add(key)
            out.append(row)
    return out


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 62)
    print("  GIPF Internet Search & Story Aggregator")
    print(f"  Keywords: gipfnamibia | GIPF | Gov. Institutions Pension Fund")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 62)

    all_rows = []

    print("\n--- Google News RSS ---")
    all_rows += search_google_news()

    print("\n--- Bing News RSS ---")
    all_rows += search_bing_news()

    print("\n--- NewsAPI ---")
    all_rows += search_newsapi()

    print("\n--- Reddit ---")
    all_rows += search_reddit()

    print("\n--- Twitter/X ---")
    all_rows += search_twitter()

    # Sort newest first, deduplicate
    all_rows = deduplicate(all_rows)
    all_rows.sort(key=lambda r: r["Date"], reverse=True)

    # Save to CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(all_rows)

    # Summary
    print(f"\n{'=' * 62}")
    print(f"  Total unique results: {len(all_rows)}")
    print(f"  Saved to: {OUTPUT_FILE}")
    print(f"{'=' * 62}")

    # Topic breakdown
    from collections import Counter
    topic_counts = Counter()
    for row in all_rows:
        for t in row["Topics"].split(", "):
            topic_counts[t.strip()] += 1

    print("\nTop Topics Found:")
    for topic, count in topic_counts.most_common(15):
        print(f"  {topic:<28} {count:>4} mentions")

    # Sentiment breakdown
    sentiments = Counter(row["Sentiment"] for row in all_rows)
    print("\nOverall Sentiment:")
    for s, c in sentiments.items():
        print(f"  {s:<12} {c:>4}")

    # Source breakdown
    source_counts = Counter(row["Source"] for row in all_rows)
    print("\nBy Source:")
    for src, c in source_counts.most_common():
        print(f"  {src:<40} {c:>4}")

    print()


if __name__ == "__main__":
    main()
