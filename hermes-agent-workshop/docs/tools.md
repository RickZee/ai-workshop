# Tools & Integrations

Hermes is a pre-built Docker image. Configure integrations via `.env` and `docker-compose.yml` — no code editing needed.

## Core (Required)

### OpenRouter — LLM

All model calls go through [OpenRouter](https://openrouter.ai). One API key, access to 100+ models.

```env
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_MODEL=nvidia/nemotron-3-super-120b-a12b:free
```

To switch models, change `OPENROUTER_MODEL`. Browse at [openrouter.ai/models](https://openrouter.ai/models).

---

### AgentMail — Email

[AgentMail](https://agentmail.to) provides the inbox and webhook. Hermes receives emails via webhook, replies via REST API.

```env
AGENTMAIL_API_KEY=am_...
AGENTMAIL_INBOX=hermes@yourdomain.agentmail.to
```

---

## Optional

### Tavily — Web Search

Triggered automatically on keywords: `stock`, `news`, `search`, `research`, `latest`, `today`, `market`, `price`, `trend`.

```env
TAVILY_API_KEY=tvly-...
```

---

### Telegram — Chat Channel

Hermes polls Telegram every 2 seconds and replies in-chat.

```env
TELEGRAM_BOT_TOKEN=123456789:AAF...
TELEGRAM_CHAT_ID=123456789
```

---

### Vision — Image Analysis

Switch to a vision-capable model. No extra configuration beyond the model name.

```env
OPENROUTER_MODEL=google/gemini-flash-1.5
```

Good options:

| Model | Cost | Notes |
|-------|------|-------|
| `google/gemini-flash-1.5` | Free tier | Recommended |
| `meta-llama/llama-3.2-11b-vision-instruct:free` | Free | Decent |
| `openai/gpt-4o-mini` | ~$0.15/M tokens | Reliable |

---

## Applying Changes

After editing `.env`:

```bash
docker compose up -d --force-recreate hermes
```

Verify:
```bash
curl http://localhost:8642/health
```
