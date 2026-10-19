"""Persistent review history stored in data/history.json."""
from __future__ import annotations
import json
import time
from pathlib import Path

HISTORY_FILE = Path(__file__).parent.parent / "data" / "history.json"


def load_history() -> list[dict]:
    try:
        return json.loads(HISTORY_FILE.read_text())
    except Exception:
        return []


def save_review(result: dict, name: str) -> None:
    history = load_history()
    score_summary = result.get("score_summary")
    history.append({
        "name":           name,
        "timestamp":      result.get("timestamp", time.time()),
        "health_score":   score_summary.health_score if score_summary else 0,
        "total_issues":   score_summary.total_issues if score_summary else 0,
        "critical_count": score_summary.critical_count if score_summary else 0,
        "warning_count":  score_summary.warning_count if score_summary else 0,
    })
    HISTORY_FILE.write_text(json.dumps(history, indent=2))


def clear_history() -> None:
    HISTORY_FILE.write_text("[]")
