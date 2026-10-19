"""
Orchestration layer — coordinates GitHub fetching, prompt building, AI calls,
and score calculation into a single review pipeline.
"""
from __future__ import annotations

import os
import time
from typing import Callable, Optional

from loguru import logger

from api.groq_client import review_code, ReviewBotError
from api.github_client import fetch_file_content, GitHubError
from core.prompt_builder import build_system_prompt, build_user_prompt, sanitize_code
from core.scorer import summarize
from utils.cache import get_cached_review, cache_review


class ReviewError(ReviewBotError):
    """Raised when a review pipeline step fails."""


def review_github_repo(
    repo_url: str,
    branch: str,
    selected_paths: list[str],
    progress_callback: Optional[Callable[[str, float], None]] = None,
) -> dict:
    """
    Run a full review of selected files from a GitHub repository.

    Args:
        repo_url: GitHub URL, e.g. https://github.com/owner/repo
        branch: Branch name.
        selected_paths: List of file paths within the repo to review.
        progress_callback: Optional fn(message, fraction) for UI progress.

    Returns:
        Full review result dict.

    Raises:
        ReviewError: On pipeline failure.
    """
    if not selected_paths:
        raise ReviewError("No files selected for review")

    def _progress(msg: str, frac: float) -> None:
        if progress_callback:
            progress_callback(msg, frac)
        logger.info(f"[{frac:.0%}] {msg}")

    system_prompt = build_system_prompt()
    file_results: list[dict] = []
    total = len(selected_paths)

    for idx, path in enumerate(selected_paths, 1):
        _progress(f"Fetching {path}...", (idx - 1) / total * 0.4)
        try:
            content = fetch_file_content(repo_url, path, branch)
        except GitHubError as exc:
            logger.warning(f"Skipping {path}: {exc}")
            continue

        ext = os.path.splitext(path)[1].lower()
        from api.github_client import EXTENSION_TO_LANGUAGE
        language = EXTENSION_TO_LANGUAGE.get(ext, "unknown")

        _progress(f"Reviewing {path}...", 0.4 + (idx / total) * 0.55)

        cached = get_cached_review(path, content)
        if cached:
            logger.debug(f"Cache hit for {path}")
            file_results.append(cached)
            continue

        code = sanitize_code(content)
        user_prompt = build_user_prompt(code, path, language)

        try:
            result = review_code(
                code=code,
                filename=path,
                language=language,
                system_prompt=system_prompt,
                user_prompt_template="{code}",  # already formatted
            )
            # Override with already-formatted prompt
            from api import groq_client as gc
            raw = gc._call_groq(
                messages=[{"role": "user", "content": user_prompt}],
                system_prompt=system_prompt,
            )
            parsed = gc._extract_json(raw)
            result = {
                "filename": path,
                "language": language,
                "issues": parsed.get("issues", []) if isinstance(parsed, dict) else [],
                "health_score": parsed.get("health_score") if isinstance(parsed, dict) else None,
                "summary": parsed.get("summary", "") if isinstance(parsed, dict) else "",
                "total_issues": 0,
            }
            result["total_issues"] = len(result["issues"])
            cache_review(path, content, result)
            file_results.append(result)
        except Exception as exc:
            logger.error(f"Review failed for {path}: {exc}")
            file_results.append({
                "filename": path,
                "language": language,
                "issues": [],
                "health_score": None,
                "summary": f"Review failed: {exc}",
                "total_issues": 0,
                "error": str(exc),
            })

    _progress("Calculating scores...", 0.97)
    score_summary = summarize(file_results)

    return {
        "repo_url": repo_url,
        "branch": branch,
        "files_reviewed": len(file_results),
        "file_results": file_results,
        "score_summary": score_summary,
        "timestamp": time.time(),
    }


def review_uploaded_file(
    content: str,
    filename: str,
    language: str,
) -> dict:
    """
    Review a single uploaded file.

    Args:
        content: File content string.
        filename: Original filename.
        language: Detected programming language.

    Returns:
        Full review result dict (single-file variant).
    """
    system_prompt = build_system_prompt()
    code = sanitize_code(content)
    user_prompt = build_user_prompt(code, filename, language)

    from api import groq_client as gc
    raw = gc._call_groq(
        messages=[{"role": "user", "content": user_prompt}],
        system_prompt=system_prompt,
    )
    parsed = gc._extract_json(raw)

    issues = parsed.get("issues", []) if isinstance(parsed, dict) else []
    result = {
        "filename": filename,
        "language": language,
        "issues": issues,
        "health_score": parsed.get("health_score") if isinstance(parsed, dict) else None,
        "summary": parsed.get("summary", "") if isinstance(parsed, dict) else "",
        "total_issues": len(issues),
    }

    file_results = [result]
    score_summary = summarize(file_results)

    return {
        "repo_url": None,
        "branch": None,
        "files_reviewed": 1,
        "file_results": file_results,
        "score_summary": score_summary,
        "timestamp": time.time(),
    }
