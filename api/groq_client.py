"""
Groq API client with exponential-backoff retry logic and structured JSON output.
All calls route through this module — never instantiate the client elsewhere.
"""
from __future__ import annotations

import json
import os
import re
import time
from typing import Any

from dotenv import load_dotenv
from loguru import logger
from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

load_dotenv()

# ── Lazy import so the app doesn't crash if groq isn't installed yet ──────────
try:
    from groq import Groq, APIError
    _GROQ_AVAILABLE = True
except ImportError:
    _GROQ_AVAILABLE = False
    logger.warning("groq package not installed — AI features disabled")


class ReviewBotError(Exception):
    """Base exception for all ReviewBot errors."""


class APIError(ReviewBotError):
    """Raised when the Groq API returns an error."""


class ParseError(ReviewBotError):
    """Raised when the AI response cannot be parsed."""


_RETRYABLE = (Exception,)  # retries on any exception; tighten in production

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
MAX_RETRIES = 4
CHUNK_TOKEN_LIMIT = int(os.getenv("CHUNK_TOKEN_LIMIT", "3000"))


def _get_client() -> Any:
    """Return a configured Groq client."""
    if not _GROQ_AVAILABLE:
        raise APIError("groq package not installed. Run: pip install groq")
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise APIError("GROQ_API_KEY is not set. Add it to your .env file.")
    return Groq(api_key=api_key)


@retry(
    retry=retry_if_exception_type(_RETRYABLE),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    stop=stop_after_attempt(MAX_RETRIES),
    reraise=True,
)
def _call_groq(messages: list[dict], system_prompt: str, temperature: float = 0.1) -> str:
    """
    Single Groq completion call with retry.

    Args:
        messages: List of {role, content} dicts.
        system_prompt: System-level instruction.
        temperature: Sampling temperature (low = more deterministic).

    Returns:
        Raw text content from the model.

    Raises:
        APIError: On unrecoverable API failure.
    """
    client = _get_client()
    start = time.time()
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "system", "content": system_prompt}] + messages,
            temperature=temperature,
            max_tokens=4096,
        )
        elapsed = time.time() - start
        logger.debug(f"Groq call completed in {elapsed:.2f}s")
        return response.choices[0].message.content or ""
    except Exception as exc:
        logger.warning(f"Groq call failed ({type(exc).__name__}): {exc}")
        raise


def _extract_json(raw: str) -> dict | list:
    """
    Extract JSON from a model response that may contain markdown fences.

    Args:
        raw: Raw model output.

    Returns:
        Parsed Python object.

    Raises:
        ParseError: If no valid JSON is found.
    """
    # Try stripping markdown fences first
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Fall back: find the first {...} or [...] block
    for pattern in (r"\{.*\}", r"\[.*\]"):
        match = re.search(pattern, cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

    raise ParseError(f"Could not extract JSON from model response: {raw[:300]}")


def _estimate_tokens(text: str) -> int:
    """Rough token estimate: 1 token ≈ 4 chars."""
    return len(text) // 4


def chunk_code(code: str, limit: int = CHUNK_TOKEN_LIMIT) -> list[str]:
    """
    Split code into chunks that fit within the token limit.

    Args:
        code: Source code string.
        limit: Max tokens per chunk.

    Returns:
        List of code chunk strings.
    """
    lines = code.splitlines(keepends=True)
    chunks: list[str] = []
    current: list[str] = []
    current_tokens = 0

    for line in lines:
        line_tokens = _estimate_tokens(line)
        if current_tokens + line_tokens > limit and current:
            chunks.append("".join(current))
            current = [line]
            current_tokens = line_tokens
        else:
            current.append(line)
            current_tokens += line_tokens

    if current:
        chunks.append("".join(current))

    return chunks or [code]


def review_code(
    code: str,
    filename: str,
    language: str,
    system_prompt: str,
    user_prompt_template: str,
) -> dict:
    """
    Review a single code file, chunking if necessary, and return merged results.

    Args:
        code: Source code content.
        filename: File name for context.
        language: Programming language string.
        system_prompt: Full system prompt from prompt_builder.
        user_prompt_template: Template with {code}, {filename}, {language} placeholders.

    Returns:
        Merged review dict with keys: issues, health_score, summary.

    Raises:
        APIError, ParseError on failure.
    """
    chunks = chunk_code(code)
    logger.info(f"Reviewing {filename} ({language}) in {len(chunks)} chunk(s)")

    all_issues: list[dict] = []
    chunk_scores: list[float] = []

    for i, chunk in enumerate(chunks):
        chunk_label = f"{filename} [chunk {i+1}/{len(chunks)}]" if len(chunks) > 1 else filename
        user_msg = user_prompt_template.format(
            code=chunk,
            filename=chunk_label,
            language=language,
        )
        try:
            raw = _call_groq(
                messages=[{"role": "user", "content": user_msg}],
                system_prompt=system_prompt,
            )
            parsed = _extract_json(raw)

            if isinstance(parsed, dict):
                all_issues.extend(parsed.get("issues", []))
                if "health_score" in parsed:
                    chunk_scores.append(float(parsed["health_score"]))
            elif isinstance(parsed, list):
                all_issues.extend(parsed)

        except RetryError as exc:
            logger.error(f"All retries exhausted for {chunk_label}: {exc}")
            raise APIError(f"Groq API failed after {MAX_RETRIES} retries for {chunk_label}") from exc
        except ParseError:
            logger.warning(f"JSON parse failed for {chunk_label} — skipping chunk")

    avg_score = round(sum(chunk_scores) / len(chunk_scores), 1) if chunk_scores else None

    return {
        "filename": filename,
        "language": language,
        "issues": all_issues,
        "health_score": avg_score,
        "total_issues": len(all_issues),
    }
