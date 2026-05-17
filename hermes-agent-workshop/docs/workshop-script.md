# Workshop Script — Presenter Guide

60-minute session. Each section has talking points, commands to run live, and timing cues.

---

## Pre-Session Checklist

Run these **before attendees arrive**:

- [ ] `docker compose up -d` — Hermes running, health check green
- [ ] `curl http://localhost:8642/health` returns `{"status":"ok"}`
- [ ] AgentMail inbox created and address confirmed (via [console.agentmail.to](https://console.agentmail.to))
- [ ] Test email sent to AgentMail address and Hermes replied (confirm email flow is live)
- [ ] Telegram bot responding (if demoing Telegram)
- [ ] Demo asset files ready in `assets/`: `demo-image.jpg`, `sample-invoice.pdf`, `voice-note.mp3`, `error-screenshot.png`
- [ ] Browser tabs open: web dashboard (http://localhost:9119), AgentMail console
- [ ] Pre-send all demo emails — have replies ready as fallback if live demo lags

---

## 00:00 – 00:05 | Welcome & Goals

**Say:**
> "Today we build Hermes — an AI agent that lives in your inbox. By the end of this hour it reads emails, understands attachments, searches the web, and replies on its own. We're going to set it up live, from zero."

**Show:** repo structure, then open http://localhost:9119 (dashboard already running).

**Goals for attendees:**
1. Understand what LLMs and agents actually are — in plain terms
2. Set up a working email agent in Docker
3. See it handle real SMB scenarios live

---

## 00:05 – 00:15 | Basics of LLMs

> Reference: `docs/basics-llms.md`

### Key points to hit

**What is an LLM?**
> "A neural network trained to predict the next token. That's it. Everything else — reasoning, coding, summarizing — emerges from scale and data."

**Tokens and context windows:**
- ~1 token = 0.75 words
- Context window = everything the model can "see" at once — system prompt, history, documents, tool results
- When context fills up, older content drops — no persistent memory by default

**Temperature:**
- `0.0` = deterministic (use for agents doing tasks)
- `1.0` = creative (use for writing)
- Hermes uses low temperature — we want reliable, not creative

**Tool use / function calling:**
> "The model emits structured JSON asking the host to call a function. Host runs it, returns result, model continues. This is the foundation of every agent."

```
Model: { "tool": "send_email", "to": "bob@co.com", "body": "Hi Bob..." }
Host:  runs send_email() → {"status":"sent"}
Model: "Email sent."
```

**Why free models for this workshop?**

OpenRouter free tier — no credit card, supports tool use.

| Model | Context | Tool Use | Cost |
|-------|---------|----------|------|
| `nvidia/nemotron-ultra-253b-v1:free` | 128k | Yes | Free |
| `anthropic/claude-haiku-4-5` | 200k | Yes | ~$1/M tokens |
| `anthropic/claude-sonnet-4-5` | 200k | Excellent | ~$3/M tokens |

**Live demo:** hit OpenRouter directly:

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia/nemotron-ultra-253b-v1:free",
    "messages": [{"role":"user","content":"What is an LLM in one sentence?"}]
  }'
```

Show the raw JSON response. Point out `choices[0].message.content`.

---

## 00:15 – 00:25 | Agents & Agentic Systems

> Reference: `docs/basics-agents.md`

### Key points to hit

**What is an agent?**
> "An LLM connected to tools, running in a loop until it completes a goal. The LLM reasons. Tools act. The loop persists."

```
Perceive → Reason → Act → repeat
```

**The agentic loop — what Hermes does for every email:**
1. Email arrives → AgentMail MCP notifies Hermes
2. LLM reads email: "What do I know? What do I need?"
3. LLM calls tool (web search, read attachment, save file)
4. Tool result returned
5. LLM reasons again with new info
6. Repeat until task done → calls `reply_to_message` via AgentMail

**How Hermes is configured:**
> "No code editing. Hermes is a pre-built Docker image. You configure it with `.env` for secrets, `~/.hermes/config.yaml` for model and behaviour — then `docker compose up`. That's it."

**Hermes architecture:**

```
Email arrives
    │
    ▼
AgentMail (agent-owned inbox) ──→ Hermes Gateway (Docker :8642)
    │
    ▼
LLM (OpenRouter)
    │
    ├── Auxiliary vision model  → analyze image/PDF attachments
    ├── Tavily / web search     → live information
    ├── Built-in cron           → scheduled proactive tasks
    └── AgentMail MCP tools     → send reply
```

**Agentic patterns Hermes uses:**

- **ReAct** — model alternates reasoning and acting. Most reliable for task completion.
- **Tool chaining** — `read_email → extract_data → search_web → send_reply`
- **Conditional branching** — invoice → payment flow; support → ticket system; lead → CRM sequence
- **Scheduled subagents** — cron jobs run in isolated agent sessions, deliver to Telegram or email

---

## 00:25 – 00:40 | Live Setup

> Reference: `docs/setup-guide.md`

Audience follows along on their own machines. Walk through each step, wait for the room.

### Step 1 — Clone and configure

```bash
git clone <repo-url>
cd hermes-agent-workshop
cp .env.example .env
```

Open `.env`, fill in keys. Workshop-specific keys on the shared slide (or pre-filled for attendees).

Minimum to start:
```env
OPENROUTER_API_KEY=sk-or-...
AGENTMAIL_API_KEY=am_...
```

### Step 2 — Configure model and integrations

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

`config.yaml.example` is pre-configured with OpenRouter + vision model + AgentMail MCP.

### Step 3 — Start Hermes

```bash
docker compose up -d
docker compose ps
curl http://localhost:8642/health
```

Open **http://localhost:9119** — show dashboard.

### Step 4 — First email test

First tell Hermes to create an inbox (via Telegram or direct message):
```
Create an inbox called "hermes" for me
```

Then send from your personal email to the AgentMail address:

```
To: hermes@yourdomain.agentmail.to
Subject: Hello
Body: What can you do?
```

Watch logs live:

```bash
docker compose logs -f hermes
```

Show reply arriving in your inbox.

### Step 5 — Telegram (optional, if time allows)

1. [@BotFather](https://t.me/BotFather) → `/newbot` → copy token
2. [@userinfobot](https://t.me/userinfobot) → get your numeric user ID
3. Add to `.env`:
   ```env
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_ALLOWED_USERS=123456789
   ```
4. `docker compose up -d --force-recreate hermes`
5. Message bot in Telegram → reply appears

---

## 00:40 – 00:55 | Live Demos

> Reference: `docs/use-cases.md`

Run 4–5 scenarios, ~3 min each. Narrate what Hermes is doing while it processes.

**Recommended order:**

| # | Scenario | What to show |
|---|----------|-------------|
| 1 | Plain Q&A | Hermes replies to "What can you do?" — baseline working |
| 2 | Image Analysis | Attach photo → Hermes describes it, drafts marketing copy |
| 3 | Invoice Processing | Attach PDF → Hermes extracts vendor/amount/date, confirms receipt |
| 4 | Support Ticket | Login issue email → Hermes classifies, creates ticket, auto-replies with ID |
| 5 | Lead Response | Inbound sales inquiry → Hermes replies with personalized pitch |

**Wildcard (last 3 min):** ask an attendee to pick a topic. Send a spontaneous email live.

**If a demo lags:** switch to pre-sent replies already in the inbox. Say "I pre-ran this so we don't wait — here's what came back."

---

## 00:55 – 01:00 | Q&A and Next Steps

**Common questions:**

| Question | Answer |
|----------|--------|
| "Can I use my own domain?" | Yes — AgentMail paid plans support custom domains |
| "What does this cost in production?" | AgentMail free: 3 inboxes, 3k emails/month. OpenRouter free models have rate limits — upgrade to Claude Haiku for ~$1/M tokens |
| "How do I add more tools?" | Add env vars to `.env`, update `config.yaml`, restart. See `docs/tools.md` |
| "Is this secure for real email?" | AgentMail is a dedicated agent inbox — not your personal account. Add `TELEGRAM_ALLOWED_USERS` to lock down who can send commands |
| "Can Hermes remember past emails?" | Yes — Hermes has a built-in memory system. Persistent context lives in `~/.hermes/memories/` (mounted into the container) |
| "How do scheduled tasks work?" | Built-in cron scheduler — tell Hermes to schedule something via chat or `/cron add`. No external cron needed |

**Next steps for attendees:**
1. Fork repo → add your own scenario to `docs/use-cases.md`
2. Swap the free model for `anthropic/claude-haiku-4-5` for better accuracy
3. Add [Tavily](https://app.tavily.com) for live web search — one env var
4. Try the built-in cron: `/cron add "every morning" "summarize my emails from yesterday"`

**Close:**
> "Everything we demoed today is driven by a handful of API keys and a config file. That's the point: agentic systems are not magic. They're a loop, some tools, and a model that knows what it's supposed to do."

---

## Post-Session

- [ ] Share repo link with attendees
- [ ] Remind: never share real `.env` keys — `.env.example` is safe to share
- [ ] Direct to `docs/setup-guide.md` for self-serve replay
