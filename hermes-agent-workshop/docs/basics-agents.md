# Basics of Agents & Agentic Systems

## What Is an Agent?

An agent is an LLM connected to tools, running in a loop until it completes a goal.

```
Perceive → Reason → Act → (repeat)
```

The LLM provides reasoning. Tools provide perception and action. The loop provides persistence.

## The Agentic Loop

```
1. Receive input (email arrives, user message, scheduled trigger)
2. LLM reasons: "What do I know? What do I need? What should I do?"
3. LLM calls a tool (read file, send email, query DB)
4. Tool result returned to LLM
5. LLM reasons again with new information
6. Repeat until task complete or LLM emits final response
```

Hermes runs this loop for every email it receives.

## Tools

Tools are functions the model can call. They bridge the gap between language and action.

| Tool Category | Examples |
|---------------|---------|
| Read | fetch email, read file, search web |
| Write | send email, save file, create calendar event |
| Compute | run code, call API, process image |
| Memory | store fact, retrieve context, update DB |

In this workshop: AgentMail (email R/W) + Filesystem MCP (file R/W) + Vision (image analysis).

## MCP — Model Context Protocol

MCP is Anthropic's open standard for connecting tools to AI models. Think of it as USB-C for AI tools.

- Standardized interface: any MCP server works with any MCP client
- Tools described as JSON schemas — model knows how to call them
- Runs as a local process, spawned by the AI client
- Claude Code ships with MCP support built in

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

That's all you need to give Hermes email superpowers.

## AgentMail

AgentMail provides an inbox designed for AI agents:
- Webhook on every incoming email
- API to send, reply, forward
- Attachment access via URL
- Thread context maintained automatically

Without AgentMail you'd need: SES + Lambda + S3 + parsing library + MIME handling. With AgentMail: one API key.

## Agentic Patterns Used in Hermes

### ReAct (Reason + Act)
Model alternates between reasoning ("I need to check the attachment") and acting ("call get_attachment tool"). Most reliable pattern for task completion.

### Tool Chaining
Output of one tool feeds into the next.
```
read_email → extract_invoice_data → look_up_vendor → send_reply
```

### Conditional Branching
Model decides which path to take based on email content.
```
if invoice → process_payment_flow
if support → route_to_ticket_system
if lead → trigger_crm_sequence
```

### Human-in-the-Loop
Agent pauses and asks for approval before high-stakes actions (sending money, deleting data).

## What Makes a Good Agent?

1. **Clear system prompt** — explicit persona, scope, escalation rules
2. **Right tools** — not too many (confusion), not too few (blocked)
3. **Error handling** — graceful fallback when tools fail
4. **Logging** — every action recorded for audit and debugging
5. **Guardrails** — model shouldn't take irreversible actions without confirmation

## Hermes Architecture

```
Email arrives
    │
    ▼
AgentMail webhook → Hermes (Docker)
    │
    ▼
LLM (OpenRouter) + Tools (MCP)
    │
    ├── Read attachment → Vision MCP → extract data
    ├── Look up context → Filesystem MCP → read history
    └── Send reply → AgentMail MCP → compose + send
```

Full diagram in `architecture/EMAIL_ARCHITECTURE.md`.
