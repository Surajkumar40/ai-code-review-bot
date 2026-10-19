"""
Health score calculator — aggregates per-file results into a single 0-100 score.
"""
from __future__ import annotations
from dataclasses import dataclass


SEVERITY_PENALTY = {
    "CRITICAL":   20,
    "WARNING":    7,
    "SUGGESTION": 2,
}


@dataclass
class ScoreSummary:
    """Aggregated review score and issue breakdown."""
    health_score: int
    total_issues: int
    critical_count: int
    warning_count: int
    suggestion_count: int
    label: str
    color: str


def calculate_health_score(issues: list[dict]) -> int:
    """
    Calculate a 0-100 health score from a list of issues.

    Starts at 100 and deducts based on severity:
    - CRITICAL: -20 each (capped to avoid sub-zero)
    - WARNING:  -7 each
    - SUGGESTION: -2 each

    Args:
        issues: List of issue dicts with 'severity' keys.

    Returns:
        Integer score 0-100.
    """
    score = 100.0
    for issue in issues:
        penalty = SEVERITY_PENALTY.get(issue.get("severity", "SUGGESTION"), 2)
        score -= penalty
    return max(0, min(100, round(score)))


def score_label(score: int) -> tuple[str, str]:
    """Return (label, hex_color) for a given score."""
    if score >= 80:
        return "Excellent", "#3FB950"
    elif score >= 60:
        return "Good",      "#58A6FF"
    elif score >= 40:
        return "Fair",      "#F0B429"
    elif score >= 20:
        return "Poor",      "#FF7B72"
    else:
        return "Critical",  "#DA3633"


def summarize(file_results: list[dict]) -> ScoreSummary:
    """
    Aggregate multiple per-file review results into a single ScoreSummary.

    Args:
        file_results: List of dicts returned by groq_client.review_code().

    Returns:
        ScoreSummary with rolled-up stats.
    """
    all_issues: list[dict] = []
    for r in file_results:
        all_issues.extend(r.get("issues", []))

    critical   = sum(1 for i in all_issues if i.get("severity") == "CRITICAL")
    warnings   = sum(1 for i in all_issues if i.get("severity") == "WARNING")
    suggestions = sum(1 for i in all_issues if i.get("severity") == "SUGGESTION")

    score = calculate_health_score(all_issues)
    label, color = score_label(score)

    return ScoreSummary(
        health_score=score,
        total_issues=len(all_issues),
        critical_count=critical,
        warning_count=warnings,
        suggestion_count=suggestions,
        label=label,
        color=color,
    )
