# Required MCP Tools

## Core (Required)

### AgentMail MCP
Email perception and action layer.

```bash
npx -y agentmail-mcp
```

**Provides tools:**
- `list_inboxes` — list available inboxes
- `list_emails` — fetch emails from inbox
- `get_email` — get full email with attachments
- `send_email` — send or reply to email
- `get_attachment` — download attachment by ID

**Setup:** `AGENTMAIL_API_KEY` in `.env`

---

### Filesystem MCP
Read/write local files. Used for saving extracted data, logs, CSV exports.

```bash
npx -y @modelcontextprotocol/server-filesystem ./data
```

**Provides tools:**
- `read_file`
- `write_file`
- `list_directory`
- `create_directory`

**Note:** Scoped to `./data` directory only. Do not mount repo root.

---

## Vision / Image Analysis

Two options:

### Option A: Claude Vision (via Anthropic SDK)
If using Claude as the LLM, image analysis is built-in. Pass image URL or base64 directly in the message.

No additional MCP needed.

### Option B: Separate Vision MCP
If using OpenRouter with a non-vision model:

```bash
npx -y @anthropic-ai/mcp-server-vision
```

Requires `ANTHROPIC_API_KEY` even if your main LLM is on OpenRouter.

---

## Optional

### Google Calendar MCP

```bash
npx -y @modelcontextprotocol/server-google-calendar
```

**Required env:**
```
GOOGLE_CALENDAR_CLIENT_ID=
GOOGLE_CALENDAR_CLIENT_SECRET=
GOOGLE_CALENDAR_REDIRECT_URI=
```

**Setup:** OAuth2 consent screen in Google Cloud Console.

---

### Slack MCP

```bash
npx -y @modelcontextprotocol/server-slack
```

**Required env:**
```
SLACK_BOT_TOKEN=xoxb-...
SLACK_TEAM_ID=T...
```

Used in: Support Ticket Routing scenario (posts to #support channel).

---

### Microsoft Teams MCP (alternative to Slack)

```bash
npx -y mcp-server-teams
```

---

## Full MCP Config Block

Paste into `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agentmail": {
      "command": "npx",
      "args": ["-y", "agentmail-mcp"],
      "env": {
        "AGENTMAIL_API_KEY": "your_key_here"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./data"]
    },
    "google-calendar": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-calendar"],
      "env": {
        "GOOGLE_CALENDAR_CLIENT_ID": "",
        "GOOGLE_CALENDAR_CLIENT_SECRET": ""
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "",
        "SLACK_TEAM_ID": ""
      }
    }
  }
}
```

Remove optional servers you don't need.

## Checking Tool Availability

In Claude Code, run:
```
/mcp
```

Each connected server appears with its tool count. Red = failed to start (check logs).
