# Hermes Agent — Docker Setup & Configuration Guide

End-to-end guide: run Hermes in Docker, configure email (AgentMail) and Telegram via the web UI.

---

## Prerequisites

| Tool | Version | Check |
|------|---------|-------|
| Docker | 24+ | `docker --version` |
| Docker Compose | 2+ | `docker compose version` |
| ngrok | any | `ngrok --version` |

API keys you'll need (all free tier):

- **OpenRouter** — LLM inference → [openrouter.ai](https://openrouter.ai)
- **AgentMail** — email inbox for the agent → [agentmail.to](https://agentmail.to)
- **Tavily** (optional) — live web search → [app.tavily.com](https://app.tavily.com)
- **Telegram Bot Token** (optional) — Telegram channel → [@BotFather](https://t.me/BotFather)

---

## Part 1 — Run Hermes in Docker

### Step 1: Clone the repo

```bash
git clone <repo-url>
cd hermes-agent-workshop
```

### Step 2: Create your `.env` file

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```env
# Required
OPENROUTER_API_KEY=sk-or-...
AGENTMAIL_API_KEY=am_...
AGENTMAIL_INBOX=hermes@yourdomain.agentmail.to

# Optional — enables live web search
TAVILY_API_KEY=tvly-...

# Optional — enables Telegram channel
TELEGRAM_BOT_TOKEN=123456789:AAF...
```

> **Model choice:** default model is `nvidia/nemotron-3-super-120b-a12b:free` (free, no credit card).  
> To use Claude directly, set `ANTHROPIC_API_KEY=sk-ant-...` instead and comment out `OPENROUTER_API_KEY`.

### Step 3: Start Hermes

```bash
docker compose up -d
```

Verify it started:

```bash
docker compose ps
# hermes   running   0.0.0.0:8642->8642/tcp, 0.0.0.0:9119->9119/tcp
```

Check health:

```bash
curl http://localhost:8642/health
# {"status":"ok","model":"nvidia/nemotron-3-super-120b-a12b:free"}
```

Watch logs:

```bash
docker compose logs -f hermes
```

### Step 4: Open the Web Dashboard

Navigate to **http://localhost:9119** in your browser.

The dashboard lets you:
- View active integrations (email, Telegram)
- Monitor incoming messages and agent replies
- Check model and API key status

---

## Part 2 — Configure Email (AgentMail)

### Step 1: Create AgentMail account

1. Go to [agentmail.to](https://agentmail.to)
2. Sign up with email or GitHub
3. Verify your email address

### Step 2: Create an inbox

1. Dashboard → **Inboxes** → **New Inbox**
2. Pick a subdomain, e.g. `hermes` → gives you `hermes@yourdomain.agentmail.to`
3. Click **Create**

Copy the full inbox address into your `.env`:
```env
AGENTMAIL_INBOX=hermes@yourdomain.agentmail.to
```

### Step 3: Get an API key

1. AgentMail Dashboard → **Settings** → **API Keys**
2. Click **Generate New Key**
3. Copy the key (shown only once)

Add to `.env`:
```env
AGENTMAIL_API_KEY=am_...
```

Restart Hermes to pick up new env values:
```bash
docker compose up -d --force-recreate hermes
```

### Step 4: Expose Hermes to the internet (ngrok)

AgentMail needs a public URL to deliver emails to your local container.

**Install ngrok** (if not installed):
```bash
# Mac
brew install ngrok/ngrok/ngrok

# Linux
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

Authenticate ngrok (one-time, get token from [dashboard.ngrok.com](https://dashboard.ngrok.com)):
```bash
ngrok config add-authtoken <your-token>
```

Start tunnel (keep this terminal open):
```bash
ngrok http 8642
```

Output will show:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:8642
```

Copy that `https://` URL.

> **Note:** Free ngrok URLs change on every restart. Update AgentMail each time you restart ngrok.  
> Paid ngrok plans offer static domains.

### Step 5: Set webhook in AgentMail

1. AgentMail Dashboard → **Inboxes** → your inbox → **Settings**
2. **Webhook URL** field → paste your ngrok URL + `/webhook/email`:
   ```
   https://abc123.ngrok-free.app/webhook/email
   ```
3. Click **Save**

### Step 6: Test email

Send an email to your AgentMail inbox address:

```
To: hermes@yourdomain.agentmail.to
Subject: Test
Body: Hello Hermes! What can you do?
```

Hermes replies within ~10 seconds.

Monitor traffic:
```bash
docker compose logs -f hermes
# Also check ngrok inspector at http://localhost:4040
```

---

## Part 3 — Configure Telegram

### Step 1: Create a Telegram bot

1. Open Telegram, search for **@BotFather**
2. Send `/newbot`
3. Enter a display name, e.g. `Hermes Agent`
4. Enter a username, e.g. `hermes_agent_bot` (must end in `bot`)
5. BotFather sends a token — copy it

### Step 2: Add token to `.env`

```env
TELEGRAM_BOT_TOKEN=123456789:AAF...
```

### Step 3: Get your Telegram chat ID

1. In Telegram, open your new bot and click **Start**
2. Send any message (e.g. `hi`)
3. Open this URL in your browser (replace `<TOKEN>` with your bot token):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
4. Find `"chat":{"id": 123456789}` in the JSON response — copy that number

Add to `.env`:
```env
TELEGRAM_CHAT_ID=123456789
```

### Step 4: Restart Hermes

```bash
docker compose up -d --force-recreate hermes
```

### Step 5: Test Telegram

Send a message to your bot in Telegram:
```
What AI stocks should I watch this week?
```

Hermes replies within ~10 seconds.

How it works:
- Hermes polls Telegram every 2 seconds for new messages
- Keywords like `stock`, `news`, `search`, `latest` trigger a Tavily web search before replying
- Runs alongside email — both channels active at the same time

---

## Part 4 — Enable Web Search (Tavily)

Tavily gives Hermes real-time web search for emails and Telegram messages containing keywords like `stock`, `news`, `search`, `research`, `latest`, `today`, `market`, `price`, `trend`.

### Step 1: Get API key

1. Go to [app.tavily.com](https://app.tavily.com)
2. Sign up (free, no credit card)
3. Copy your key from the dashboard (starts with `tvly-`)

### Step 2: Add to `.env`

```env
TAVILY_API_KEY=tvly-...
```

### Step 3: Restart Hermes

```bash
docker compose up -d --force-recreate hermes
```

### Step 4: Test

Send this email to your inbox:
```
Subject: AI stock research
Body: What are the top AI-related stocks to watch this week? Search for recent news.
```

Hermes searches the web and replies with a summary.

---

## Ports Reference

| Port | Purpose |
|------|---------|
| `8642` | API / webhook endpoint (exposed to internet via ngrok) |
| `9119` | Web dashboard (local only) |

---

## Troubleshooting

**Hermes not replying to emails**
- Check webhook is reachable: `curl https://abc123.ngrok-free.app/webhook/email` (should get a response)
- ngrok still running? Check terminal / `http://localhost:4040`
- Correct API key? `docker compose logs hermes | grep -i error`

**"OPENROUTER_API_KEY not set" error on start**
- `.env` file missing or not in the same directory as `docker-compose.yml`
- Run `docker compose down && docker compose up -d` from the `hermes-agent-workshop/` directory

**Model errors / rate limits**
- Switch model in `.env`: `OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free`
- Check quota at [openrouter.ai](https://openrouter.ai) dashboard

**Telegram not responding**
- Confirm `TELEGRAM_BOT_TOKEN` in `.env` is correct (no spaces)
- Make sure you sent at least one message to the bot before checking `getUpdates`
- `docker compose logs -f hermes` — look for Telegram polling errors

**Dashboard not loading at port 9119**
- Confirm `HERMES_DASHBOARD=1` is set in `docker-compose.yml` (it is by default)
- `docker compose ps` — container must show `running`

**Full reset**
```bash
docker compose down -v
docker compose up -d
```

---

## Data Persistence

Hermes stores state in `~/.hermes` on your host machine (mounted as `/opt/data` in the container). Data survives container restarts.

To wipe all state:
```bash
docker compose down
rm -rf ~/.hermes
docker compose up -d
```
