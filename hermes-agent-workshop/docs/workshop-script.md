# Workshop Script — 60 Minutes

## 00:00 – 00:05 | Welcome & Goals (5 min)

**Say:**
> "Today we build Hermes — an AI agent that lives in your inbox. By the end of this hour it will read emails, understand attachments, and take real actions."

**Show:** repo structure, final demo video (30 sec).

**Goals:**
1. Understand what LLMs and agents actually are
2. Set up a working email agent in Docker
3. Run live demos across real SMB scenarios

---

## 00:05 – 00:15 | Basics of LLMs (10 min)

Reference: `docs/basics-llms.md`

Key points to cover:
- Tokens, context windows, temperature
- Why LLMs alone aren't agents
- Models available via OpenRouter (free tier)
- Why `nvidia/nemotron-3-super-120b-a12b:free` for this workshop

**Live demo:** curl OpenRouter, show raw completion.

---

## 00:15 – 00:25 | Basics of Agents & Agentic Systems (10 min)

Reference: `docs/basics-agents.md`

Key points to cover:
- Perception → Reasoning → Action loop
- Tools as the bridge between LLM and the world
- MCP (Model Context Protocol) — what it is, why it matters
- AgentMail as the email perception/action layer

**Diagram:** show `architecture/EMAIL_ARCHITECTURE.md` diagram.

---

## 00:25 – 00:40 | Setting up Hermes in Docker (15 min)

Reference: `docs/hermes-setup-guide.md`

```bash
# Audience follows along
git clone <repo>
cd hermes-agent-workshop
./setup/install.sh
# Edit .env (pre-filled keys for workshop)
docker-compose up
```

Verify: `http://localhost:3000/health` returns `{"status":"ok"}`.

Wire MCP tools in Claude Code:
```json
{
  "mcpServers": {
    "agentmail": { "command": "npx", "args": ["-y", "agentmail-mcp"] },
    "filesystem": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "./data"] }
  }
}
```

---

## 00:40 – 00:55 | Live Demos (15 min)

Reference: `scenarios/AGENTMAIL_DEMO_SCENARIOS.md`

Run in this order (3 min each, pick 5):
1. Image Analysis & Reply
2. Invoice Processing
3. Support Ticket Routing
4. Lead Response Automation
5. Voice Message Handling

For each: send test email → watch Hermes process → show response.

---

## 00:55 – 01:00 | Q&A and Next Steps (5 min)

**Common questions:**
- "Can I use my own domain?" → Yes, configure SMTP in AgentMail
- "Cost in production?" → See AgentMail vs Custom table in `architecture/EMAIL_ARCHITECTURE.md`
- "How do I add more tools?" → Add MCP server to config, restart

**Next steps for attendees:**
- Fork repo, add your own scenario
- Read `architecture/SECURITY_AUDIT.md` before going to prod
- Join AgentMail Discord for support
