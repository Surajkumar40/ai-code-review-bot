"""Home page — hero, features, stats. Stunning first impression."""
from __future__ import annotations
import json
from pathlib import Path
import streamlit as st
from ui.components import section_label, stat_card, spacer

HISTORY_FILE = Path(__file__).parent.parent.parent / "data" / "history.json"

def _history():
    try: return json.loads(HISTORY_FILE.read_text())
    except: return []

def render():
    # ── HERO ──────────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="rb-hero">'
        '<h1 class="rb-hero-title">AI-Powered Code Review<br>for Serious Engineers</h1>'
        '<p class="rb-hero-sub">Catch bugs, security vulnerabilities, and code smells before '
        'they reach production. Powered by LLaMA 3 on Groq — results in seconds, not minutes.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    c1, c2, _ = st.columns([1.2, 1, 4])
    with c1:
        if st.button("Start Reviewing →", use_container_width=True):
            return "review"
    with c2:
        if st.button("View History", use_container_width=True, type="secondary"):
            return "history"

    # ── DIVIDER ────────────────────────────────────────────────────────────────
    spacer("2rem")
    st.markdown("<hr>", unsafe_allow_html=True)
    spacer("0.25rem")

    # ── FEATURES ──────────────────────────────────────────────────────────────
    section_label("What ReviewBot Does")

    features = [
        ("⚡", "Instant Analysis",   "Paste a GitHub URL or upload a file — get a full severity-graded review in under 30 seconds."),
        ("🌐", "Multi-Language",     "Python, JavaScript, TypeScript, Java, and C++ with language-specific rule sets."),
        ("🛡️", "Security First",     "Detects OWASP Top 10 patterns, SQL injection, hardcoded secrets, and unsafe deserialization."),
        ("📋", "Exportable Reports", "Every review produces a Markdown report with before/after code fixes ready to share."),
        ("📈", "Score Tracking",     "A 0–100 health score per review tracked over time — watch your codebase improve."),
        ("🔁", "Rock-Solid Calls",   "Exponential backoff via Tenacity — no flaky reviews when the API hiccups."),
    ]

    for row in range(0, len(features), 3):
        cols = st.columns(3, gap="small")
        for i, col in enumerate(cols):
            idx = row + i
            if idx < len(features):
                icon, title, desc = features[idx]
                with col:
                    st.markdown(
                        f'<div class="rb-card rb-card-glow" style="min-height:140px;">'
                        f'<div class="rb-feat-icon">{icon}</div>'
                        f'<span class="rb-feat-title">{title}</span>'
                        f'<p class="rb-feat-desc">{desc}</p>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
        spacer("8px")

    # ── STATS ──────────────────────────────────────────────────────────────────
    spacer("1.25rem")
    st.markdown("<hr>", unsafe_allow_html=True)
    spacer("0.25rem")
    section_label("Live Stats")

    history = _history()
    total_issues = sum(r.get("total_issues", 0) for r in history)

    c1, c2, c3, c4 = st.columns(4, gap="small")
    for col, val, lbl, clr in [
        (c1, "5",                 "Languages",     "var(--accent)"),
        (c2, str(len(history)),   "Reviews Run",   "var(--green)"),
        (c3, str(total_issues),   "Issues Found",  "#E3B341"),
        (c4, "Free",              "Groq Tier",     "var(--text1)"),
    ]:
        with col: stat_card(val, lbl, clr)

    spacer("2.5rem")
    return None
