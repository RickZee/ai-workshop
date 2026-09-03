# Basics of LLMs

## What Is a Language Model?

A Large Language Model (LLM) is a neural network trained to predict the next token given a sequence of tokens. At inference time, it samples tokens one at a time to produce a completion.

That's it. Everything else — reasoning, coding, conversation — emerges from scale and training data.

## Key Concepts

### Tokens
Text is split into subword chunks called tokens. Roughly 1 token ≈ 0.75 words in English.

- `"Hello, world!"` → 4 tokens
- GPT-4o context window: 128k tokens (~100k words)
- Cost is priced per token (input + output)

### Context Window
Everything the model "sees" at once. Includes: system prompt, conversation history, tool results, documents you paste in.

Once context is full, older content is dropped — the model has no memory beyond what's in the window.

### Temperature
Controls randomness in token sampling.
- `0.0` → deterministic, always picks highest-probability token
- `1.0` → creative, samples from full distribution
- For agents doing tasks: use `0.1–0.3`. For creative writing: `0.7–1.0`.

### System Prompt
Instructions given to the model before the conversation. Sets persona, constraints, output format. The model treats it as authoritative context.

### Tool Use / Function Calling
Models can emit structured JSON asking the host to call a function. The host runs the function, returns results, and the model continues. This is the foundation of agents.

```
Model: { "tool": "send_email", "to": "bob@co.com", "body": "Hi Bob..." }
Host:  runs send_email() → returns { "status": "sent", "id": "msg_123" }
Model: "Email sent successfully."
```

## Why Free Models for This Workshop?

`inclusionai/ling-3.0-flash-fin:free` via [OpenRouter](https://openrouter.ai):
- Free tier, no credit card
- Supports tool use — required, or Hermes cannot call anything
- Good enough for all workshop demos

**Free model ids are retired without notice.** Before running the workshop, check
[openrouter.ai/models?q=free](https://openrouter.ai/models?q=free) and confirm the id below
still exists and still lists tool use — the previous default in this repo was retired.
Last verified against the OpenRouter model list on 2026-09-03.

In production you'd use a paid frontier model for better accuracy and reliability.

## Model Comparison

| Model | Context | Tool Use | Cost |
|-------|---------|----------|------|
| [ling-3.0-flash-fin](https://openrouter.ai/inclusionai/ling-3.0-flash-fin:free) (free) | 262k | Yes | Free |
| [inkling-small](https://openrouter.ai/thinkingmachines/inkling-small:free) (free) | 1M | Yes | Free |
| [Claude Opus 5](https://openrouter.ai/anthropic/claude-opus-5) | 1M | Excellent | ~$5/M in, ~$25/M out |

Prices and ids move — verified against the OpenRouter model list on 2026-09-03.

## What LLMs Cannot Do (Alone)

- Send emails
- Read files
- Browse the web
- Remember past conversations
- Take actions in the world

For all of that, you need an agent.
