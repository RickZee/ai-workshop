# Tools & Integrations

Hermes is a pre-built Docker image. Configure via `.env`, `docker-compose.yml`, and `~/.hermes/config.yaml` — no code editing needed.

---

## Core (Required)

### OpenRouter — LLM

All model calls go through [OpenRouter](https://openrouter.ai). One API key, 100+ models.

`.env`:
```env
OPENROUTER_API_KEY=sk-or-...
```

`~/.hermes/config.yaml`:
```yaml
model:
  provider: openrouter
  default: inclusionai/ling-3.0-flash-fin:free
```

Browse models at [openrouter.ai/models](https://openrouter.ai/models). Filter "Free" for
no-cost options, and check the model's page lists **tool use** — Hermes needs it. Free ids
are retired without notice; this one was verified against the OpenRouter model list on 2026-09-03.

---

## Optional Integrations

### AgentMail — Email

Gives Hermes its own dedicated email address (e.g. `hermes@yourdomain.agentmail.to`). No SMTP/IMAP, no personal inbox. Connects as an MCP skill — provides 11 tools: `create_inbox`, `send_message`, `reply_to_message`, `list_threads`, `get_attachment`, and more.

`.env`:
```env
AGENTMAIL_API_KEY=am_...
```

`~/.hermes/config.yaml`:
```yaml
mcp_servers:
  agentmail:
    command: "npx"
    args: ["-y", "agentmail-mcp"]
    env:
      AGENTMAIL_API_KEY: "${AGENTMAIL_API_KEY}"
```

`docker-compose.yml` already passes `AGENTMAIL_API_KEY` into the container. Restart to apply:
```bash
docker compose up -d --force-recreate hermes
```

Free tier: 3 inboxes, 3,000 emails/month. Sign up at [console.agentmail.to](https://console.agentmail.to).

---

### Telegram

Hermes polls Telegram via the Bot API and replies in-chat.

`.env`:
```env
TELEGRAM_BOT_TOKEN=123456789:AAF...
TELEGRAM_ALLOWED_USERS=123456789
```

For cron job delivery to a specific group/channel:
```env
TELEGRAM_HOME_CHANNEL=-1001234567890
```

---

### Vision — Image Analysis

Auxiliary model for image/PDF attachments. Set in `~/.hermes/config.yaml`:

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

No extra API key — all route through `OPENROUTER_API_KEY`.

---

### Tavily — Web Search

`.env`:
```env
TAVILY_API_KEY=tvly-...
```

Other supported backends: Firecrawl (`FIRECRAWL_API_KEY`), SearXNG (self-hosted, `SEARXNG_URL`), Exa (`EXA_API_KEY`).

---

## Applying Changes

After editing `.env`:
```bash
docker compose up -d --force-recreate hermes
```

After editing `~/.hermes/config.yaml`:
```bash
docker compose restart hermes
```

Verify:
```bash
curl http://localhost:8642/health
docker compose logs -f hermes
```
