# Capstone — pick one, ship it badly, then measure it

**90 minutes, in pairs.** The point is not a polished system. It is to hit the failure modes
yourself while someone is in the room who can explain them.

Whichever you pick, you are done when you can show:

1. it works on three inputs you did not design for,
2. **a number** — accuracy, recall@k, schema-valid rate, or override rate,
3. one failure you found and either fixed or documented,
4. the thing you would refuse to automate, and why.

That last item is the real deliverable.

---

## Option A — Inbox triage that a human would actually trust

Combine Lab 2 and Lab 3. Classify incoming support email, draft a reply for the easy
categories, and route everything else to a person with a reason attached.

- Extend `data/support_emails.json` with ten of your own (redacted) messages and label them.
- The draft reply is generated only when `needs_human` is false and `confidence >= 0.8`.
- Report the override rate: how often would a human have to correct it? That number decides
  whether it ships.

## Option B — A knowledge worker over your team's real docs

Take Lab 4 and repoint `DOCS` at a folder of your own runbooks, onboarding docs, or ADRs.

- Write eight eval questions with known source documents *before* you tune anything.
- Get a baseline recall@3, then improve chunking or add the hybrid retriever, and re-measure.
- Add an `audience` metadata filter and demonstrate that a filtered chunk never reaches the
  model — that is how access control works in RAG.

## Option C — An MCP server for something you own

Take Lab 6 and wrap the smallest read-only system your team has: a status endpoint, a ticket
search, a log query, a deploy history.

- Two tools, good descriptions, an allowlist on what they can reach.
- Drive it with the Lab 5 agent, then point a second client at it (Claude Desktop, or the
  Hermes agent from Workshop 1) to prove the "write once, use anywhere" claim.
- Write down what would have to be true for this to hold a write tool.

## Option D — Break someone else's

Swap notebooks with another pair and try to make their system fail: prompt injection in a
document, an ambiguous input, a tool argument they did not validate, a question their corpus
cannot answer. Report findings kindly. This is the most useful option and nobody picks it.

---

## Debrief questions (15 minutes, whole room)

- What surprised you about where it failed?
- Which of your fixes was a prompt change, and which was an engineering change? Which held up?
- What is the smallest version of this that would be genuinely useful on Monday?
- What would you need to see before you let it act without a human?
