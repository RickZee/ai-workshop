# Hermes Setup Guide

Step-by-step to get Hermes running locally in Docker.

## Prerequisites

| Requirement | Version | Check |
|-------------|---------|-------|
| Docker | 24+ | `docker --version` |
| Docker Compose | 2+ | `docker compose version` |
| Node.js | 18+ (for MCP tools) | `node --version` |
| Claude Code CLI | latest | `claude --version` |

## Step 1: Clone & Configure

```bash
git clone <repo-url>
cd hermes-agent-workshop
./setup/install.sh
```

Edit `.env`:
```bash
OPENROUTER_API_KEY=sk-or-...
AGENTMAIL_API_KEY=am_...
AGENTMAIL_INBOX=hermes@yourdomain.agentmail.to
```

## Step 2: Start Services

```bash
docker-compose up -d
```

Verify:
```bash
curl http://localhost:3000/health
# {"status":"ok","model":"nvidia/nemotron-3-super-120b-a12b:free"}
```

Logs:
```bash
docker-compose logs -f hermes
```

## Step 3: Configure AgentMail Webhook

In AgentMail dashboard:
1. Go to Inboxes → your inbox → Settings
2. Set webhook URL: `http://<your-public-ip>:3000/webhook/email`
3. For local dev, use ngrok: `ngrok http 3000`
4. Copy the ngrok HTTPS URL into AgentMail

Test webhook:
```bash
# Send a test email to your AgentMail inbox
# Watch logs: docker-compose logs -f hermes
```

## Step 4: Wire MCP Tools in Claude Code

Add to `~/.claude/claude_desktop_config.json` (or Claude Code settings):

```json
{
  "mcpServers": {
    "agentmail": {
      "command": "npx",
      "args": ["-y", "agentmail-mcp"],
      "env": {
        "AGENTMAIL_API_KEY": "<your key>"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "./data"
      ]
    }
  }
}
```

Restart Claude Code. Verify tools appear: `/mcp` in Claude Code shows `agentmail` and `filesystem`.

## Step 5: Send Your First Email

Send an email to your AgentMail inbox:

```
To: hermes@yourdomain.agentmail.to
Subject: Test
Body: Hello Hermes! What can you do?
```

Expected: Hermes replies within 10 seconds describing its capabilities.

## Troubleshooting

**Hermes not responding to emails**
- Check webhook URL is reachable from internet
- `docker-compose logs hermes` for errors
- Verify `AGENTMAIL_API_KEY` is correct

**Model errors / rate limits**
- Switch to a different free model on OpenRouter
- Check OpenRouter dashboard for quota

**MCP tools not appearing in Claude Code**
- Restart Claude Code after config change
- Check Node.js 18+ is installed
- Run `npx -y agentmail-mcp` manually to test

**Docker fails to start**
- `docker-compose down -v && docker-compose up --build`

## Model Swap

To use Claude directly instead of OpenRouter, update `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-...
# Comment out OPENROUTER_API_KEY
```

And update `hermes` service config to use Anthropic SDK.
