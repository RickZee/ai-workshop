# Use Cases — Setup Requirements

Hermes is a pre-built Docker image. All configuration is done via `.env`, `docker-compose.yml`, and `~/.hermes/config.yaml`. No code editing needed.

**Base stack** (required for everything) → see [setup-guide.md](setup-guide.md):
- Docker + Hermes running
- AgentMail configured (`AGENTMAIL_API_KEY` + `config.yaml`)
- Telegram bot configured (Telegram use cases)

After any `.env` change:
```bash
docker compose up -d --force-recreate hermes
```

After any `~/.hermes/config.yaml` change:
```bash
docker compose restart hermes
```

---

## Tool Requirements by Use Case

| # | Use Case | Extra needed |
|---|----------|-------------|
| 1 | Image Analysis | Vision model in `config.yaml` |
| 2 | PDF Processing | none |
| 3 | Voice Message | none (built-in STT via OpenRouter) |
| 4 | Screenshot Debugging | Vision model in `config.yaml` |
| 5 | Receipt & Expense | Vision model in `config.yaml` |
| 6 | Video Summary | `TAVILY_API_KEY` |
| 7–8 | Customer / Invoice | none |
| 9 | Support Ticket Routing | `SLACK_BOT_TOKEN` (optional) |
| 10–13 | SMB scenarios | none |
| 11 | Appointment Booking | `GOOGLE_CALENDAR_*` vars |
| 14–18 | Developer Tools | none (Telegram) |
| 19–23 | Personal Assistant | none (Telegram) |
| 24 | Travel Assistant | `TAVILY_API_KEY` + trip config file |
| 25–27 | Local Files | filesystem MCP (already in `config.yaml.example`) |

---

## Vision (Image Analysis)

Needed for: #1, #4, #5.

Set in `~/.hermes/config.yaml`:
```yaml
auxiliary:
  vision:
    provider: openrouter
    model: google/gemini-2.5-flash
```

| Model | Cost | Notes |
|-------|------|-------|
| `google/gemini-2.5-flash` | Free tier | Recommended |
| `meta-llama/llama-3.2-11b-vision-instruct:free` | Free | Decent |
| `openai/gpt-4o-mini` | ~$0.15/M tokens | Reliable |

No extra API key — all go through `OPENROUTER_API_KEY`.

---

## Voice Transcription

Needed for: #3.

Hermes has built-in STT. Default uses a local Whisper model (no API key needed). Configure in `~/.hermes/config.yaml`:

```yaml
stt:
  provider: local      # no key needed
  local:
    model: base        # tiny | base | small | medium | large-v3
```

For better accuracy via OpenRouter-compatible endpoint, switch provider to `openai` and set `OPENAI_API_KEY` — but `local` works for the workshop.

---

## Slack Notifications

Needed for: #9 (optional).

**Step 1 — Create Slack app:**
1. [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From Scratch**
2. **OAuth & Permissions** → Bot Token Scopes: `chat:write`, `channels:read`
3. **Install to Workspace** → copy **Bot User OAuth Token** (`xoxb-...`)
4. In Slack: `/invite @YourBot` in `#support`

**Step 2 — Add to `.env`:**
```env
SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL=#support
```

**Step 3 — Add to `docker-compose.yml` under `environment`:**
```yaml
- SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}
- SLACK_CHANNEL=${SLACK_CHANNEL}
```

---

## Google Calendar

Needed for: #11.

**Step 1 — Create OAuth credentials:**
1. [console.cloud.google.com](https://console.cloud.google.com) → new project
2. **APIs & Services** → enable **Google Calendar API**
3. **Credentials** → **Create OAuth client ID** → Desktop app
4. Copy `client_id` and `client_secret`

**Step 2 — Add to `.env`:**
```env
GOOGLE_CALENDAR_CLIENT_ID=...apps.googleusercontent.com
GOOGLE_CALENDAR_CLIENT_SECRET=GOCSPX-...
GOOGLE_CALENDAR_REFRESH_TOKEN=...
```

**Step 3 — Get refresh token (one-time):**
```bash
pip install google-auth-oauthlib
python3 -c "
from google_auth_oauthlib.flow import InstalledAppFlow
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/calendar'])
creds = flow.run_local_server(port=0)
print('Refresh token:', creds.refresh_token)
"
```

**Step 4 — Add to `docker-compose.yml` under `environment`:**
```yaml
- GOOGLE_CALENDAR_CLIENT_ID=${GOOGLE_CALENDAR_CLIENT_ID}
- GOOGLE_CALENDAR_CLIENT_SECRET=${GOOGLE_CALENDAR_CLIENT_SECRET}
- GOOGLE_CALENDAR_REFRESH_TOKEN=${GOOGLE_CALENDAR_REFRESH_TOKEN}
```

---

## Scheduled Travel Assistant

Needed for: #24.

Hermes has a **built-in cron scheduler** — no external cron needed. The gateway ticks every 60 seconds and runs any due jobs in isolated agent sessions.

**How it works:**
1. Tell Hermes your trip details once (via Telegram or email)
2. Hermes creates a cron job internally and saves it to `~/.hermes/cron/`
3. Each morning it calls Tavily for live flight/weather data and pushes a Telegram update
4. Silent when nothing needs attention — only messages when there's something actionable

**Setup — tell Hermes your trip:**

Via Telegram:
```
I'm flying to Lisbon on May 20. Flight TAP 351, departs 10:40 from YYZ, arrives 22:15.
Hotel: Marriott Downtown, check-in May 20, checkout May 24.
Set up a daily morning briefing — weather, flight status, local tips.
```

Hermes creates the cron job and confirms. You can also manage jobs directly:

```
/cron list
/cron run <job_id>    # test immediately
```

**Or create manually via Telegram:**
```
/cron add "0 8 * * *" "Check flight TAP351 status and Lisbon weather. Send morning travel brief to Telegram. If nothing urgent, reply [SILENT]." --deliver telegram --name "Lisbon trip brief"
```

**Requires:**
- `TAVILY_API_KEY` in `.env` for live flight/weather data
- `TELEGRAM_BOT_TOKEN` + `TELEGRAM_ALLOWED_USERS` configured
- Hermes container running (`docker compose up -d`)

---

## Filesystem MCP (Local Files)

Needed for: #25–27.

Gives Hermes read/write access to `./data/` in the repo. Uses the official [MCP filesystem server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) running via `npx` inside the container.

**Already configured** in `config.yaml.example` and `docker-compose.yml` — no extra steps if you copied the example config.

### How it works

```
./data/          (your machine)
   ↕  docker-compose volume mount
/workspace/data  (inside container)
   ↕  MCP server
Hermes agent     (reads/writes via filesystem MCP tools)
```

Files you drop in `./data/` on your machine are immediately visible to Hermes. Files Hermes writes appear instantly in `./data/` on your machine.

### Verify it's active

After `docker compose up -d`, ask Hermes:
```
List the files in /workspace/data
```

If the MCP server started correctly, it lists the contents of `./data/`.

### docker-compose.yml volume (already present)

```yaml
volumes:
  - ./data:/workspace/data
```

### config.yaml MCP block (already in config.yaml.example)

```yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/workspace/data"]
```

> The path `/workspace/data` is what Hermes sees inside the container. On your host it maps to `./data/` relative to `docker-compose.yml`.

### Add sample files to test

```bash
echo "region,revenue\nNorth,120000\nSouth,95000\nWest,140000" > data/sales.csv
```

Then ask Hermes: `Read data/sales.csv and summarize it`
