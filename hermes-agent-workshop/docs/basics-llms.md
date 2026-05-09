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

`nvidia/nemotron-3-super-120b-a12b:free` via OpenRouter:
- 120B parameter model — strong reasoning
- Free tier, no credit card
- Supports tool use
- Good enough for all workshop demos

In production you'd likely use Claude 3.5/3.7 Sonnet for better accuracy and reliability.

## Model Comparison

| Model | Context | Tool Use | Cost |
|-------|---------|----------|------|
| nemotron-3-super-120b (free) | 128k | Yes | Free |
| Claude Haiku 4.5 | 200k | Yes | ~$1/M tokens |
| Claude Sonnet 4.6 | 200k | Excellent | ~$3/M tokens |
| Claude Opus 4.7 | 200k | Excellent | ~$15/M tokens |

## What LLMs Cannot Do (Alone)

- Send emails
- Read files
- Browse the web
- Remember past conversations
- Take actions in the world

For all of that, you need an agent.
