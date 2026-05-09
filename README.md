# Hermes Agent Workshop

60-minute hands-on workshop: build an autonomous AI agent that lives in your inbox — reads emails, reasons about them, and replies using live web search and multimodal tools.

## What You'll Build

**Hermes** — a Docker-based AI email agent powered by OpenRouter (free tier). It handles plain text, attachments, images, PDFs, and voice messages. Optionally connects to Telegram.

## Schedule

| Time | Topic |
|------|-------|
| 00:00 – 00:05 | Welcome & Goals |
| 00:05 – 00:15 | Basics of LLMs |
| 00:15 – 00:25 | Agents & Agentic Systems |
| 00:25 – 00:40 | Setup: Docker + Email + Telegram |
| 00:40 – 00:55 | Live Demos |
| 00:55 – 01:00 | Q&A |

## Quick Start

```bash
cd hermes-agent-workshop
cp .env.example .env
# Fill in all vars
docker compose up -d
```

Dashboard: **http://localhost:9119** · API: **http://localhost:8642**

## Docs

- [Setup Guide](hermes-agent-workshop/docs/setup-guide.md) — Docker, email, Telegram, web search
- [Workshop Script](hermes-agent-workshop/docs/workshop-script.md) — presenter guide with timing and live commands
- [Basics: LLMs](hermes-agent-workshop/docs/basics-llms.md)
- [Basics: Agents](hermes-agent-workshop/docs/basics-agents.md)
- [Use cases](hermes-agent-workshop/docs/use-cases.md) — email, multimedia, SMB, developer tools, personal assistant

## Repo Structure

```
hermes-agent-workshop/
├── docs/
│   ├── setup-guide.md
│   ├── workshop-script.md
│   ├── basics-llms.md
│   ├── basics-agents.md
│   ├── use-cases.md
│   └── tools.md
├── assets/               # Demo files (images, PDF, audio, slides)
└── docker-compose.yml
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) 24+ and [Docker Compose](https://docs.docker.com/compose/install/) 2+
- [OpenRouter](https://openrouter.ai) API key (free tier)
- [AgentMail](https://agentmail.to) account (free tier)
- [ngrok](https://ngrok.com) account (free tier, for local webhook exposure)
