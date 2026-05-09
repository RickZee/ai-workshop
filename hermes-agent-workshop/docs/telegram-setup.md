# Telegram Bot Setup Guide

Connect Hermes to Telegram — message the bot, Hermes replies in chat.

## Step 1: Create Telegram Bot

1. Open Telegram, search for **@BotFather**
2. Send `/newbot`
3. Choose a name (e.g. `Hermes Agent`)
4. Choose a username (e.g. `hermes_agent_bot`)
5. BotFather sends you a token — copy it

## Step 2: Add to .env

```bash
TELEGRAM_BOT_TOKEN=123456789:AAF...
```

## Step 3: Get Your Chat ID

1. Start a chat with your bot (search username, click Start)
2. Send any message to it
3. Visit this URL in your browser (replace TOKEN):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
4. Find `"chat":{"id":...}` in the response — copy that number

Add to `.env`:
```bash
TELEGRAM_CHAT_ID=123456789
```

## Step 4: Restart Hermes

```bash
docker compose up -d --build hermes-email
```

## How It Works

- Hermes polls Telegram every 2 seconds for new messages
- Your message → LLM (+ web search if needed) → reply in Telegram
- Works alongside email webhook — both channels active simultaneously

## Test It

Open Telegram, message your bot:
```
What AI stocks should I watch this week?
```

Hermes replies directly in Telegram within ~10 seconds.
