"""Simple in-memory + hash-based file review cache."""
from __future__ import annotations
import hashlib

_cache: dict[str, dict] = {}


def _key(path: str, content: str) -> str:
    h = hashlib.md5((path + content).encode()).hexdigest()
    return f"{path}:{h}"


def get_cached_review(path: str, content: str) -> dict | None:
    return _cache.get(_key(path, content))


def cache_review(path: str, content: str, result: dict) -> None:
    _cache[_key(path, content)] = result
