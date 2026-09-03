"""Shared helpers for the hands-on labs.

Everything here is deliberately small and readable — open it, don't treat it as a
framework. Both backends speak the OpenAI Chat Completions API, so one client
class covers the hosted free tier (OpenRouter) and a local model (Ollama).
"""
from __future__ import annotations

import json
import os
from typing import Any, Iterable

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

# Override to point the labs at any OpenAI-compatible endpoint (a proxy, a gateway,
# another provider) without editing this file.
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
MODEL = os.getenv("MODEL", "nvidia/nemotron-ultra-253b-v1:free")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def client(local: bool = False) -> OpenAI:
    """Return an OpenAI-compatible client for the hosted free tier or local Ollama."""
    if local:
        return OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")  # Ollama ignores the key
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set — copy .env.example to .env and fill it in")
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=key)


def model_name(local: bool = False) -> str:
    return OLLAMA_MODEL if local else MODEL


def chat(
    messages: list[dict[str, Any]] | str,
    *,
    system: str | None = None,
    local: bool = False,
    temperature: float = 0.2,
    tools: list[dict] | None = None,
    **kwargs: Any,
):
    """One-shot chat call. Pass a string for a quick question, or a message list.

    Returns the raw `message` object so tool calls survive; use `.content` for text.
    """
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    if system:
        messages = [{"role": "system", "content": system}] + messages
    resp = client(local).chat.completions.create(
        model=model_name(local),
        messages=messages,
        temperature=temperature,
        **({"tools": tools} if tools else {}),
        **kwargs,
    )
    return resp.choices[0].message


def ask(prompt: str, *, system: str | None = None, local: bool = False, **kwargs: Any) -> str:
    """Text in, text out — the 90% case."""
    return chat(prompt, system=system, local=local, **kwargs).content or ""


def stream(messages: list[dict[str, Any]] | str, *, system: str | None = None,
           local: bool = False, temperature: float = 0.2) -> Iterable[str]:
    """Yield content deltas as they arrive."""
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    if system:
        messages = [{"role": "system", "content": system}] + messages
    resp = client(local).chat.completions.create(
        model=model_name(local), messages=messages,
        temperature=temperature, stream=True,
    )
    for chunk in resp:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def extract_json(text: str) -> Any:
    """Pull the first JSON object/array out of a model response.

    Free models often wrap JSON in prose or a ```json fence. Production code should
    use a provider's structured-output mode; this is the honest fallback.
    """
    if text is None:
        raise ValueError("no text to parse")
    cleaned = text.strip()
    if "```" in cleaned:
        parts = cleaned.split("```")
        for part in parts:
            candidate = part[4:] if part.lower().startswith("json") else part
            try:
                return json.loads(candidate.strip())
            except json.JSONDecodeError:
                continue
    starts = [i for i, ch in enumerate(cleaned) if ch in "{["]
    for start in starts:
        opener = cleaned[start]
        closer = "}" if opener == "{" else "]"
        depth = 0
        for end in range(start, len(cleaned)):
            if cleaned[end] == opener:
                depth += 1
            elif cleaned[end] == closer:
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(cleaned[start:end + 1])
                    except json.JSONDecodeError:
                        break
    raise ValueError(f"no JSON found in response: {cleaned[:200]!r}")


def preflight() -> None:
    """Print what this environment can reach. Run it first, in every lab."""
    print(f"hosted model : {MODEL}")
    print(f"local  model : {OLLAMA_MODEL} at {OLLAMA_BASE_URL}")
    key = os.getenv("OPENROUTER_API_KEY")
    print(f"OPENROUTER_API_KEY: {'set (' + key[:8] + '…)' if key else 'MISSING'}")
    try:
        reply = ask("Reply with exactly: ok", temperature=0)
        print(f"hosted call  : ok -> {reply.strip()[:40]!r}")
    except Exception as exc:  # noqa: BLE001 - we want the message, whatever it is
        print(f"hosted call  : FAILED -> {type(exc).__name__}: {exc}")
    try:
        reply = ask("Reply with exactly: ok", local=True, temperature=0)
        print(f"local call   : ok -> {reply.strip()[:40]!r}")
    except Exception as exc:  # noqa: BLE001
        print(f"local call   : unavailable -> {type(exc).__name__} (fine if you skipped Ollama)")
