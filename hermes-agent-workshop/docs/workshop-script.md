# Workshop Script — Presenter Guide

60-minute session. Each section has talking points, commands to run live, and timing cues.

---

## Pre-Session Checklist

Run these **before attendees arrive**:

- [ ] `docker compose up -d` — Hermes running, health check green
- [ ] `curl http://localhost:8642/health` returns `{"status":"ok"}`
- [ ] ngrok running: `ngrok http 8642` — URL pasted into AgentMail webhook
- [ ] Test email sent and Hermes replied (confirm email flow is live)
- [ ] Telegram bot responding (if demoing Telegram)
- [ ] Demo asset files ready in `assets/`: `demo-image.jpg`, `sample-invoice.pdf`, `voice-note.mp3`, `error-screenshot.png`
- [ ] Browser tabs open: web dashboard (http://localhost:9119), ngrok inspector (http://localhost:4040), AgentMail dashboard
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
- Hermes uses `0.1` — we want reliable, not creative

**Tool use / function calling:**
> "The model emits structured JSON asking the host to call a function. Host runs it, returns result, model continues. This is the foundation of every agent."

```
Model: { "tool": "send_email", "to": "bob@co.com", "body": "Hi Bob..." }
Host:  runs send_email() → {"status":"sent"}
Model: "Email sent."
```

**Why free models for this workshop?**

`nvidia/nemotron-3-super-120b-a12b:free` via OpenRouter: 120B params, supports tool use, free tier, no credit card.

| Model | Context | Tool Use | Cost |
|-------|---------|----------|------|
| nemotron-3-super-120b (free) | 128k | Yes | Free |
| Claude Haiku 4.5 | 200k | Yes | ~$1/M tokens |
| Claude Sonnet 4.6 | 200k | Excellent | ~$3/M tokens |
| Claude Opus 4.7 | 200k | Excellent | ~$15/M tokens |

**Live demo:** hit OpenRouter directly:

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia/nemotron-3-super-120b-a12b:free",
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
1. Email arrives → AgentMail fires webhook
2. LLM reads email: "What do I know? What do I need?"
3. LLM calls tool (web search, read attachment, look up history)
4. Tool result returned
5. LLM reasons again with new info
6. Repeat until task done → send reply

**MCP — Model Context Protocol:**
> "Anthropic's open standard for connecting tools to AI models. Think USB-C for AI tools. Any MCP server works with any MCP client. Claude Code ships with MCP support built in."

```json
{
  "mcpServers": {
    "agentmail": {
      "command": "npx",
      "args": ["-y", "agentmail-mcp"]
    }
  }
}
```

> "That config line gives Hermes email superpowers."

**AgentMail vs. rolling your own:**

Without AgentMail: SES + Lambda + S3 + MIME parser + attachment handling.  
With AgentMail: one API key.

**Agentic patterns Hermes uses:**

- **ReAct** — model alternates reasoning and acting. Most reliable for task completion.
- **Tool chaining** — `read_email → extract_data → search_web → send_reply`
- **Conditional branching** — invoice → payment flow; support → ticket system; lead → CRM sequence

**Hermes architecture:**

```
Email arrives
    │
    ▼
AgentMail webhook → Hermes (Docker :8642)
    │
    ▼
LLM (OpenRouter) ──── Tools (MCP)
    │                    ├── AgentMail MCP  (read/send email)
    │                    ├── Filesystem MCP (save/load files)
    │                    └── Vision MCP     (images, PDFs)
    ▼
Reply sent via AgentMail API
```

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

### Step 2 — Start Hermes

```bash
docker compose up -d
docker compose ps
curl http://localhost:8642/health
```

Open **http://localhost:9119** — show dashboard.

### Step 3 — AgentMail webhook

```bash
ngrok http 8642
# Copy https://... URL
```

1. AgentMail dashboard → Inboxes → your inbox → Settings
2. Webhook URL: `https://<ngrok-url>/webhook/email`
3. Save

### Step 4 — First email test

Send from your personal email to the AgentMail inbox:

```
To: hermes@yourdomain.agentmail.to
Subject: Hello
Body: What can you do?
```

Watch logs live:

```bash
docker compose logs -f hermes
```

Show reply arriving. Point to ngrok inspector at http://localhost:4040.

### Step 5 — Telegram (optional, if time allows)

1. @BotFather → `/newbot` → copy token
2. Add `TELEGRAM_BOT_TOKEN=...` to `.env`
3. `docker compose up -d --force-recreate hermes`
4. Message bot in Telegram → reply appears

---

## 00:40 – 00:55 | Live Demos

> Reference: `scenarios/AGENTMAIL_DEMO_SCENARIOS.md`

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
| "Can I use my own domain?" | Yes — configure custom SMTP in AgentMail settings |
| "What does this cost in production?" | AgentMail free tier: 1k emails/month. OpenRouter free models have rate limits — upgrade to Claude Haiku for ~$1/M tokens |
| "How do I add more tools?" | Add MCP server entry to Claude config, restart. See `tools/TOOLS_REQUIRED.md` |
| "Is this secure for real email?" | Read the security notes in `tools/TOOLS_REQUIRED.md` before going to prod. Add allowlists, human-in-the-loop for high-stakes actions |
| "Can Hermes remember past emails?" | Not by default — add Filesystem MCP to write conversation history, read it back in the system prompt |

**Next steps for attendees:**
1. Fork repo → add your own scenario to `scenarios/`
2. Swap the free model for Claude Sonnet 4.6 for better accuracy
3. Add Tavily for live web search — just one API key
4. Join AgentMail Discord for support

**Close:**
> "The entire agent is in `app/main.py` — under 150 lines. Everything we demoed today is in that file plus a handful of API keys. That's the point: agentic systems are not magic. They're a loop, some tools, and a good system prompt."

---

## Post-Session

- [ ] Share repo link with attendees
- [ ] Remind: never share real `.env` keys — `.env.example` is safe to share
- [ ] Direct to `docs/setup-guide.md` for self-serve replay
