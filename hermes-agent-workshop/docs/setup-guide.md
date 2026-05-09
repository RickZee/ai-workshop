# Hermes Setup Guide

Everything needed to run Hermes locally: Docker, email (AgentMail), Telegram, and live web search.

---

## Prerequisites

| Tool | Version | Check |
|------|---------|-------|
| [Docker](https://docs.docker.com/get-docker/) | 24+ | `docker --version` |
| [Docker Compose](https://docs.docker.com/compose/install/) | 2+ | `docker compose version` |
| [ngrok](https://ngrok.com/download) | any | `ngrok --version` |

API keys (all free tier, no credit card):

| Service | Purpose | URL |
|---------|---------|-----|
| [OpenRouter](https://openrouter.ai) | LLM inference | [openrouter.ai](https://openrouter.ai) |
| [AgentMail](https://agentmail.to) | Email inbox for agent | [agentmail.to](https://agentmail.to) |
| [ngrok](https://ngrok.com) | Public webhook tunnel | [dashboard.ngrok.com](https://dashboard.ngrok.com) |
| [Tavily](https://app.tavily.com) | Live web search (optional) | [app.tavily.com](https://app.tavily.com) |
| [Telegram BotFather](https://t.me/BotFather) | Telegram channel (optional) | [@BotFather](https://t.me/BotFather) |

---

## Part 1 — Docker Setup

### Step 1: Clone and configure

```bash
git clone <repo-url>
cd hermes-agent-workshop
cp .env.example .env
```

Edit `.env`:

```env
# Required
OPENROUTER_API_KEY=sk-or-...
AGENTMAIL_API_KEY=am_...
AGENTMAIL_INBOX=hermes@yourdomain.agentmail.to
TAVILY_API_KEY=tvly-...
TELEGRAM_BOT_TOKEN=123456789:AAF...
```

> **Model:** default is `nvidia/nemotron-3-super-120b-a12b:free` — free, no credit card, supports tool use.  
> To use Claude directly: set `ANTHROPIC_API_KEY=sk-ant-...` and remove `OPENROUTER_API_KEY`.

### Step 2: Start Hermes

```bash
docker compose up -d
```

Verify:

```bash
docker compose ps
# hermes   running   0.0.0.0:8642->8642/tcp, 0.0.0.0:9119->9119/tcp

curl http://localhost:8642/health
# {"status":"ok","model":"nvidia/nemotron-3-super-120b-a12b:free"}
```

### Step 3: Open the web dashboard

**http://localhost:9119** — shows active integrations, message log, model status.

Watch logs:

```bash
docker compose logs -f hermes
```

---

## Part 2 — Email via AgentMail

### Step 1: Create account and inbox

1. Go to [agentmail.to](https://agentmail.to) → sign up
2. Dashboard → **Inboxes** → **New Inbox**
3. Pick subdomain, e.g. `hermes` → gives `hermes@yourdomain.agentmail.to`
4. Click **Create**

### Step 2: Get API key

1. AgentMail Dashboard → **Settings** → **API Keys** → **Generate New Key**
2. Copy the key (shown once)

Update `.env`:

```env
AGENTMAIL_API_KEY=am_...
AGENTMAIL_INBOX=hermes@yourdomain.agentmail.to
```

Restart to pick up new values:

```bash
docker compose up -d --force-recreate hermes
```

### Step 3: Expose Hermes via ngrok

AgentMail needs a public HTTPS URL to deliver emails to your local container.

**Install ngrok:**

```bash
# Mac
brew install ngrok/ngrok/ngrok

# Linux
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

Authenticate (one-time, token from [dashboard.ngrok.com](https://dashboard.ngrok.com)):

```bash
ngrok config add-authtoken <your-token>
```

Start tunnel (keep this terminal open):

```bash
ngrok http 8642
```

Output:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:8642
```

Copy that `https://` URL.

> **Note:** Free ngrok URLs change on every restart — update AgentMail webhook each time.

### Step 4: Set webhook in AgentMail

1. AgentMail Dashboard → **Inboxes** → your inbox → **Settings**
2. **Webhook URL** → paste ngrok URL + `/webhook/email`:
   ```
   https://abc123.ngrok-free.app/webhook/email
   ```
3. **Save**

### Step 5: Test

Send an email to your inbox:

```
To: hermes@yourdomain.agentmail.to
Subject: Test
Body: Hello Hermes! What can you do?
```

Hermes replies within ~10 seconds. Check ngrok inspector at **http://localhost:4040** for request/response detail.

---

## Part 3 — Telegram

### Step 1: Create a bot

1. Open Telegram → search **@BotFather** → send `/newbot`
2. Enter display name, e.g. `Hermes Agent`
3. Enter username, e.g. `hermes_agent_bot` (must end in `bot`)
4. Copy the token BotFather sends

### Step 2: Add to `.env`

```env
TELEGRAM_BOT_TOKEN=123456789:AAF...
```

### Step 3: Find your chat ID

1. Open your new bot in Telegram → click **Start** → send any message
2. Visit in browser (replace `<TOKEN>`):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
3. Find `"chat":{"id": 123456789}` → copy that number

```env
TELEGRAM_CHAT_ID=123456789
```

### Step 4: Restart and test

```bash
docker compose up -d --force-recreate hermes
```

Send a message to your bot in Telegram:

```
What AI stocks should I watch this week?
```

Reply arrives within ~10 seconds. Hermes polls Telegram every 2 seconds and runs alongside email simultaneously.

---

## Part 4 — Live Web Search (Tavily)

Triggers automatically when email or Telegram message contains keywords: `stock`, `news`, `search`, `research`, `latest`, `today`, `market`, `price`, `trend`.

### Step 1: Get API key

1. Go to [app.tavily.com](https://app.tavily.com) → sign up (free, no credit card)
2. Copy key from dashboard (starts with `tvly-`)

### Step 2: Add to `.env` and restart

```env
TAVILY_API_KEY=tvly-...
```

```bash
docker compose up -d --force-recreate hermes
```

### Step 3: Test

```
Subject: AI stock research
Body: What are the top AI-related stocks to watch this week? Search for recent news.
```

Hermes searches the web and replies with a sourced summary.

---

## Ports Reference

| Port | Purpose |
|------|---------|
| `8642` | API / webhook endpoint (expose this via ngrok) |
| `9119` | Web dashboard (local only) |

---

## Troubleshooting

**Hermes not replying to emails**
- ngrok still running? Check http://localhost:4040
- Webhook reachable? `curl https://abc123.ngrok-free.app/webhook/email`
- `docker compose logs hermes | grep -i error`

**Container fails to start**
- `.env` missing required keys — `OPENROUTER_API_KEY` and `AGENTMAIL_API_KEY` are required
- Run from `hermes-agent-workshop/` directory: `docker compose down && docker compose up -d`

**Model errors or rate limits**
- Switch model: `OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free` in `.env`
- Check quota at [openrouter.ai](https://openrouter.ai)

**Telegram not responding**
- Confirm token has no trailing spaces
- Send at least one message to bot before checking `getUpdates`
- `docker compose logs -f hermes` — look for polling errors

**Full reset**
```bash
docker compose down -v
rm -rf ~/.hermes
docker compose up -d
```
