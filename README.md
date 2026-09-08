# AI Workshops

Three tracks, each self-contained:

| Track | Folder | Format | Audience |
|-------|--------|--------|----------|
| **1. AI Foundations for Engineers** | `presentation/ai-foundations-for-engineers.*` | Seven concept modules (six core + a gotchas clinic), ~60-75 min each | IT/software people new to AI |
| **2. AI Hands-On Lab** | `handson-lab/` + `presentation/ai-handson-lab.*` | Seven notebooks in four blocks, free stack | Same audience, after track 1 |
| **3. Hermes Agent Workshop** | `hermes-agent-workshop/` | 60-min build of a deployed email agent | Anyone wanting the deployed version |

Each presentation ships as a markdown presenter guide (bullets + speaker notes, with Mermaid diagrams) and a matching `.pptx`. The markdown is the source: edit it, and the deck is regenerated from it.

Workshop 2's project ideas are adapted from [Ed Donner](https://edwarddonner.com)'s Udemy courses — see [`handson-lab/README.md`](handson-lab/README.md) for credits, setup and troubleshooting.

```
├── presentation/              # decks for tracks 1 and 2 (.md presenter guide + .pptx)
├── handson-lab/               # track 2 — notebooks/ (TODO cells), solutions/, data/, capstone.md
│   ├── README.md              #   setup, the lab table, troubleshooting
│   └── requirements.txt       #   verified version floors — check here first if a lab breaks
└── hermes-agent-workshop/     # track 3 — docs/, assets/, docker-compose.yml
```

**Before running track 2:** free model ids get retired without notice. Lab 0 lists which
OpenRouter models are currently free *and* claim tool support, then fires a real tool call —
run both cells and put a passing id in `.env` rather than trusting the committed default.

---

## Track 3 — Hermes Agent Workshop

60-minute hands-on workshop: build an autonomous AI agent that lives in your inbox — reads emails, reasons about them, and replies using live web search and multimodal tools.

### What You'll Build

**Hermes** — a Docker-based AI email agent powered by OpenRouter (free tier). It handles plain text, attachments, images, PDFs, and voice messages. Optionally connects to Telegram.

### Schedule

| Time | Topic |
|------|-------|
| 00:00 – 00:05 | Welcome & Goals |
| 00:05 – 00:15 | Basics of LLMs |
| 00:15 – 00:25 | Agents & Agentic Systems |
| 00:25 – 00:40 | Setup: Docker + Email + Telegram |
| 00:40 – 00:55 | Live Demos |
| 00:55 – 01:00 | Q&A |

### Quick Start

```bash
cd hermes-agent-workshop
cp .env.example .env
# Fill in all vars
docker compose up -d
```

Dashboard: **http://localhost:9119** · API: **http://localhost:8642**

### Docs

- [Setup Guide](hermes-agent-workshop/docs/setup-guide.md) — Docker, email, Telegram, web search
- [Workshop Script](hermes-agent-workshop/docs/workshop-script.md) — presenter guide with timing and live commands
- [Basics: LLMs](hermes-agent-workshop/docs/basics-llms.md)
- [Basics: Agents](hermes-agent-workshop/docs/basics-agents.md)
- [Use cases](hermes-agent-workshop/docs/use-cases.md) — email, multimedia, SMB, developer tools, personal assistant
- [Use cases setup](hermes-agent-workshop/docs/use-cases-setup.md) — Vision, Whisper, Slack, Google Calendar, cron scheduler
- [Tools & integrations](hermes-agent-workshop/docs/tools.md) — OpenRouter, AgentMail, Telegram, vision, web search


### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) 24+ and [Docker Compose](https://docs.docker.com/compose/install/) 2+
- [OpenRouter](https://openrouter.ai) API key (free tier)
- [AgentMail](https://agentmail.to) account (free tier)
- [ngrok](https://ngrok.com) account (free tier, for local webhook exposure)

### Slides

[Hermes workshop — Google Slides](https://docs.google.com/presentation/d/11jxwLDl3uARdpcatefZ31XNugTaNIptlTC6hP9UzXxU/edit?usp=sharing) (this track only; tracks 1 and 2 have their own decks in `presentation/`)