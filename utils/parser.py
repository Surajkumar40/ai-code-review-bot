"""Language detection utilities."""
from __future__ import annotations
import os

EXT_MAP = {
    ".py": "python", ".js": "javascript", ".ts": "typescript",
    ".java": "java", ".cpp": "cpp", ".cc": "cpp", ".h": "cpp",
}

def detect_language(filename: str) -> str:
    return EXT_MAP.get(os.path.splitext(filename)[1].lower(), "unknown")
