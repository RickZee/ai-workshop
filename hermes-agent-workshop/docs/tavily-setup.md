# Tavily Search API Setup Guide

Gives Hermes live web search — used for real-time data like stock analysis, news, and research.

## Step 1: Create Account

1. Go to [app.tavily.com](https://app.tavily.com)
2. Sign up with GitHub or Google (no credit card required)
3. API key shown immediately on dashboard

## Step 2: Copy API Key

From the dashboard, copy your key (starts with `tvly-...`).

## Step 3: Add to .env

```bash
TAVILY_API_KEY=tvly-...
```

## Free Tier Limits

- 1,000 queries/month
- No credit card required
- AI-optimized results (cleaner than raw search)

## Step 4: Restart Hermes

```bash
docker compose up -d hermes-email
```

## Test It

Send an email to your AgentMail inbox:

```
Subject: AI stock research
Body: What are the top AI-related stocks to watch this week? Search for recent news.
```

Hermes will search the web, summarize findings, and reply with analysis.
