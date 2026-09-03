# Workshop 2 — Hands-On Lab

Seven notebooks that build the things Workshop 1 explains. Same audience — IT and software
people — but this time everyone types.

**Credit where it is due.** The project ideas here are adapted from
[Ed Donner](https://edwarddonner.com)'s Udemy courses, mainly
[*LLM Engineering*](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/)
(brochure generator, tool-calling chat UI, RAG knowledge worker) and
[*The Complete Agentic AI Engineering Course*](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course/)
(hand-written agent loop, MCP). His repos are worth reading alongside these:
[llm_engineering](https://github.com/ed-donner/llm_engineering) and
[agents](https://github.com/ed-donner/agents). The code here is our own, rewritten to run on
a **free stack** — no credit card, no OpenAI billing — and condensed from fourteen weeks into
a day. If people want the full treatment afterwards, send them to his courses.

---

## The labs

| # | Lab | Time | You build | Source |
|---|-----|------|-----------|--------|
| 0 | First contact | 30 min | Working environment, first calls, tokens, temperature, streaming | Ed, LLM Eng. wk 1 |
| 1 | Brochure generator | 45 min | Scrape a site, model picks the links, chained calls write a brochure | Ed, LLM Eng. wk 1 |
| 2 | Structured output and evals | 50 min | A schema, validation with retry, and a 12-case eval harness with real numbers | Concepts M2 + M5 |
| 3 | Chat UI with tools | 50 min | Gradio chat that calls your functions — the tool-calling handshake | Ed, LLM Eng. wk 2 |
| 4 | RAG knowledge worker | 60 min | Chunk + index this repo's docs, answer with citations, measure recall@k | Ed, LLM Eng. wk 5 |
| 5 | Agent loop from scratch | 55 min | The loop by hand, then step caps, loop detection and an approval gate | Ed, Agentic wk 1 |
| 6 | MCP server and client | 50 min | An MCP server over the repo, driven by your own agent | Ed, Agentic wk 6 |

Each lab is a notebook in `notebooks/` with `# TODO` cells, and a matching finished version
in `solutions/`. Attendees work in `notebooks/`; presenters keep `solutions/` open.

Suggested split across four sessions: **0+1**, then **2+3**, then **4**, then **5+6** and the
[capstone](capstone.md).

---

## Setup (do this before the session, it takes ten minutes)

### 1. A Python environment

With [uv](https://docs.astral.sh/uv/) (fastest):

```bash
cd handson-lab
uv venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

Or plain pip:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. A free model key

Sign up at [openrouter.ai](https://openrouter.ai) (no card), create a key, then:

```bash
cp .env.example .env       # and paste your key into it
```

Free models come and go. If the default in `.env.example` has been retired, pick another
from [openrouter.ai/models?q=free](https://openrouter.ai/models?q=free) — you want one whose
page lists **tool use**, or Labs 3, 5 and 6 will struggle.

### 3. Optional — a model on your own laptop

```bash
# https://ollama.com, then:
ollama pull llama3.2
```

Every lab has a `local=True` path. The local 3B model is noticeably worse, which is itself
one of the lessons.

### 4. Start

```bash
jupyter lab
```

Open `notebooks/lab0-first-contact.ipynb` and run the `preflight()` cell. It prints exactly
what your machine can and cannot reach. **Do this before the workshop, not during it.**

---

## Troubleshooting

| Symptom | What is happening | Fix |
|---|---|---|
| `OPENROUTER_API_KEY is not set` | No `.env`, or you started Jupyter before creating it | Create `.env`, restart the kernel |
| `429` / rate limited | Free tier throttles per minute and per day | Wait a minute; batch fewer cases; switch free model |
| Model ignores the tools (Labs 3, 5, 6) | Free models vary a lot in tool-use quality | `temperature=0`, sharpen the tool description, or switch to another free model that lists tool support |
| JSON fails to parse (Labs 1, 2) | The model wrapped it in prose or a fence | That is the lesson — `extract_json()` handles it, and Lab 2 adds validate-and-retry |
| Lab 4 first run hangs | Downloading the ~90 MB embedding model | One-time; let it finish |
| `ModuleNotFoundError` in a notebook | Jupyter is on a different kernel than your venv | Start `jupyter lab` from the activated venv |
| Notebook cannot find `shared.py` | You opened it from the wrong directory | Run notebooks from inside `notebooks/` |

---

## What is deliberately missing

No fine-tuning (needs a GPU and hours — Ed's Weeks 6-7 cover it properly), no framework tour
(CrewAI, LangGraph and the Agents SDK are his Weeks 3-5; Lab 5 exists so you understand what
they wrap), and no deployment. Workshop 1's `hermes-agent-workshop/` is the deployment story:
the same ideas already running in Docker with a real inbox.
