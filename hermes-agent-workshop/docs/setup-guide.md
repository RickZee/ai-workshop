# Hermes Setup Guide

Everything needed to run Hermes locally in Docker: model, email (AgentMail), Telegram, and web search.

---

## Prerequisites

| Tool | Version | Check |
|------|---------|-------|
| [Docker](https://docs.docker.com/get-docker/) | 24+ | `docker --version` |
| [Docker Compose](https://docs.docker.com/compose/install/) | 2+ | `docker compose version` |

API keys needed:

| Service | Purpose | URL |
|---------|---------|-----|
| [OpenRouter](https://openrouter.ai) | LLM inference (free tier available) | [openrouter.ai](https://openrouter.ai) |
| [AgentMail](https://agentmail.to) | Agent-owned email inbox | [console.agentmail.to](https://console.agentmail.to) |
| [Telegram BotFather](https://t.me/BotFather) | Telegram channel (optional) | [@BotFather](https://t.me/BotFather) |
| [Tavily](https://app.tavily.com) | Live web search (optional) | [app.tavily.com](https://app.tavily.com) |

---

## Part 1 — Docker Setup

### Step 0: Install Docker

**Mac:**
```bash
brew install --cask docker
open /Applications/Docker.app
```
Or download [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/).

**Windows:**
Download and run [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/). Enable WSL2 backend when prompted.

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

Verify:
```bash
docker --version
docker compose version
```

---

### Step 1: Clone and configure

Mac/Linux:
```bash
git clone <repo-url>
cd hermes-agent-workshop
cp .env.example .env
```

Windows:
```cmd
git clone <repo-url>
cd hermes-agent-workshop
copy .env.example .env
```

Edit `.env` — fill in your keys:

```env
OPENROUTER_API_KEY=sk-or-...
AGENTMAIL_API_KEY=am_...
```

Telegram and Tavily are optional — add when you get to those sections.

---

### Step 2: Configure Hermes

Hermes reads `~/.hermes/config.yaml` for model and integration settings. Create it from the example:

Mac/Linux:
```bash
mkdir -p ~/.hermes
cp config.yaml.example ~/.hermes/config.yaml
```

Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.hermes"
Copy-Item config.yaml.example "$env:USERPROFILE\.hermes\config.yaml"
```

The example config sets up:
- OpenRouter free model for LLM
- Google Gemini Flash for vision (images/PDFs)
- AgentMail as MCP skill for email

> **Switch models:** edit `~/.hermes/config.yaml` → change `default:`. Browse free models at [openrouter.ai/models](https://openrouter.ai/models).

---

### Step 3: Start Hermes

```bash
docker compose up -d
```

Verify:
```bash
docker compose ps
# hermes   running   0.0.0.0:8642->8642/tcp, 0.0.0.0:9119->9119/tcp
```

Open the web dashboard: **http://localhost:9119**

Watch logs:
```bash
docker compose logs -f hermes
```

---

## Part 2 — Email via AgentMail

AgentMail gives Hermes its own dedicated email address (e.g. `hermes@yourdomain.agentmail.to`) — no SMTP/IMAP setup, no personal inbox needed. It connects as an MCP skill.

### Step 1: Create account and get API key

1. Go to [console.agentmail.to](https://console.agentmail.to) → sign up (free)
2. Copy your API key (starts with `am_`)

### Step 2: Add key to `.env`

```env
AGENTMAIL_API_KEY=am_...
```

The key is already wired through `docker-compose.yml` into the container environment, and `config.yaml.example` passes it into the AgentMail MCP server.

### Step 3: Restart and create an inbox

```bash
docker compose up -d --force-recreate hermes
```

Hermes creates and manages inboxes via the AgentMail tools. On first use, tell Hermes:

```
Create an inbox called "hermes" for me
```

It replies with the inbox address, e.g. `hermes@yourdomain.agentmail.to`.

### Step 4: Test

Send an email to that address from your personal email:

```
To: hermes@yourdomain.agentmail.to
Subject: Test
Body: Hello Hermes! What can you do?
```

Hermes polls for new messages and replies. Check logs:

```bash
docker compose logs -f hermes
```

---

## Part 3 — Telegram

### Step 1: Create a bot

1. Open Telegram → search **[@BotFather](https://t.me/BotFather)** → send `/newbot`
2. Enter display name, e.g. `Hermes Agent`
3. Enter username, e.g. `hermes_agent_bot` (must end in `bot`)
4. Copy the token BotFather sends

### Step 2: Get your user ID

Message **[@userinfobot](https://t.me/userinfobot)** — it replies with your numeric user ID (e.g. `123456789`).

### Step 3: Add to `.env`

```env
TELEGRAM_BOT_TOKEN=123456789:AAF...
TELEGRAM_ALLOWED_USERS=123456789
```

> **`TELEGRAM_ALLOWED_USERS`** — comma-separated numeric user IDs. Without it, the gateway denies all users.
> Multiple users: `TELEGRAM_ALLOWED_USERS=123456789,987654321`

### Step 4: Restart and test

```bash
docker compose up -d --force-recreate hermes
```

Open your bot in Telegram → send a message:

```
What can you do?
```

Reply arrives within a few seconds.

### Group chats

Telegram privacy mode is **on** by default — bots only see `/` commands. To fix:

1. Message @BotFather → `/mybots` → your bot → **Bot Settings → Group Privacy → Turn off**
2. Remove and re-add the bot to any existing groups

---

## Part 4 — Live Web Search (Tavily)

### Step 1: Get API key

1. Go to [app.tavily.com](https://app.tavily.com) → sign up (free, no credit card)
2. Copy key (starts with `tvly-`)

### Step 2: Add to `.env` and restart

```env
TAVILY_API_KEY=tvly-...
```

```bash
docker compose up -d --force-recreate hermes
```

### Test

Send via email or Telegram:

```
What are the top AI stories this week?
```

---

## Data & Persistence

Docker containers are stateless — anything written inside disappears on restart. Hermes persists everything to `~/.hermes/` on your host, mounted into the container at `/opt/data`.

```
Your machine          Container
~/.hermes/    ←——→   /opt/data/
```

Key files:

| Host path | Contents |
|-----------|---------|
| `~/.hermes/config.yaml` | Model, MCP servers, display settings |
| `~/.hermes/.env` | API keys (used by `hermes` CLI — Docker uses its own `.env`) |
| `~/.hermes/memories/` | Persistent agent memory across sessions |
| `~/.hermes/sessions/` | Conversation history |
| `~/.hermes/cron/` | Scheduled task definitions |

Windows path: `%USERPROFILE%\.hermes\`

Files survive `docker compose down` + `docker compose up`. Only `rm -rf ~/.hermes` clears everything.

---

## Ports Reference

| Port | Purpose |
|------|---------|
| `8642` | OpenAI-compatible API server + gateway |
| `9119` | Web dashboard (local only) |

---

## Troubleshooting

**Hermes not replying to emails**
- Confirm `AGENTMAIL_API_KEY` is set and starts with `am_`
- Check MCP server started: `docker compose logs hermes | grep -i agentmail`
- Verify inbox exists in [console.agentmail.to](https://console.agentmail.to)

**Container fails to start**
- `OPENROUTER_API_KEY` is the only strictly required key
- Run from `hermes-agent-workshop/` directory: `docker compose down && docker compose up -d`

**Model errors or rate limits**
- Edit `~/.hermes/config.yaml` → change `default:` to another free model → restart
- Check quota at [openrouter.ai](https://openrouter.ai)

**Telegram not responding**
- `TELEGRAM_ALLOWED_USERS` must be a numeric user ID, not a username
- `docker compose logs -f hermes` — look for gateway errors

**Full reset**
```bash
docker compose down -v
rm -rf ~/.hermes
docker compose up -d
```
