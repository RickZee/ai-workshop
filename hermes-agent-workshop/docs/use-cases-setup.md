# Use Cases — Setup Requirements

Hermes is a pre-built Docker image. All configuration is done via `.env` and `docker-compose.yml`. No code editing needed.

**Base stack** (required for everything) → see [setup-guide.md](setup-guide.md):
- Docker + Hermes running
- AgentMail + ngrok (email use cases)
- Telegram bot (Telegram use cases)

After any `.env` change:
```bash
docker compose up -d --force-recreate hermes
```

---

## Tool Requirements by Use Case

| # | Use Case | Extra needed |
|---|----------|-------------|
| 1 | Image Analysis | Vision model via `OPENROUTER_MODEL` |
| 2 | PDF Processing | none |
| 3 | Voice Message | `OPENAI_API_KEY` for Whisper |
| 4 | Screenshot Debugging | Vision model via `OPENROUTER_MODEL` |
| 5 | Receipt & Expense | Vision model via `OPENROUTER_MODEL` |
| 6 | Video Summary | `TAVILY_API_KEY` |
| 7–8 | Customer / Invoice | none |
| 9 | Support Ticket Routing | `SLACK_BOT_TOKEN` (optional) |
| 10–13 | SMB scenarios | none |
| 11 | Appointment Booking | `GOOGLE_CALENDAR_*` vars |
| 14–18 | Developer Tools | none (Telegram) |
| 19–23 | Personal Assistant | none (Telegram) |
| 24 | Travel Assistant | `TAVILY_API_KEY` + trip config in `~/.hermes/trips/` |

---

## Vision (Image Analysis)

Needed for: #1, #4, #5.

Set in `.env`:
```env
OPENROUTER_MODEL=google/gemini-flash-1.5
```

| Model | Cost | Notes |
|-------|------|-------|
| `google/gemini-flash-1.5` | Free tier | Recommended |
| `meta-llama/llama-3.2-11b-vision-instruct:free` | Free | Decent |
| `openai/gpt-4o-mini` | ~$0.15/M tokens | Reliable |

---

## Voice Transcription (Whisper)

Needed for: #3.

Add to `.env`:
```env
OPENAI_API_KEY=sk-...
```

Add to `docker-compose.yml` under `environment`:
```yaml
- OPENAI_API_KEY=${OPENAI_API_KEY}
```

Hermes passes the `.mp3` attachment to OpenAI Whisper API and summarizes the transcript.

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

Hermes runs the travel assistant internally — no external cron needed. Once you drop a trip config into `~/.hermes/trips/`, Hermes monitors it on its own schedule and pushes Telegram updates proactively.

**How it works:**
- Hermes has a built-in scheduler that checks `~/.hermes/trips/` periodically
- When a trip is upcoming, it calls Tavily for live flight/weather data and messages your Telegram chat
- No external trigger required — just configure the trip file and Hermes does the rest

**Trip config file** — create on your host machine at `~/.hermes/trips/my-trip.json` (maps to `/opt/data/trips/` inside the container):

Mac/Linux:
```bash
mkdir -p ~/.hermes/trips
```

Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.hermes\trips"
```

Then create `~/.hermes/trips/my-trip.json` (Windows: `%USERPROFILE%\.hermes\trips\my-trip.json`):
```json
{
  "destination": "Lisbon",
  "flight": {
    "number": "TAP351",
    "departs": "2025-05-20T10:40:00",
    "arrives": "2025-05-20T22:15:00",
    "origin": "YYZ",
    "destination_airport": "LIS"
  },
  "hotel": {
    "name": "Marriott Downtown Lisbon",
    "checkin": "2025-05-20",
    "checkout": "2025-05-24"
  },
  "telegram_chat_id": "123456789",
  "timezone": "Europe/Lisbon",
  "preferences": ["weather", "restaurants", "transport", "packing"]
}
```
