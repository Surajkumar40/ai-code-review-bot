"""Reusable UI components — every component is intentional."""
from __future__ import annotations
import streamlit as st

LANG_COLORS = {
    "python":"#3776AB","javascript":"#F7DF1E","typescript":"#3178C6",
    "java":"#ED8B00","cpp":"#00599C","unknown":"#6E7681",
}
SEV = {
    "CRITICAL": ("ic-crit","rb-crit","🔴","Must fix — crash or security risk"),
    "WARNING":  ("ic-warn","rb-warn","🟡","Should fix — performance or bad practice"),
    "SUGGESTION":("ic-sugg","rb-sugg","🔵","Nice to fix — style or readability"),
}

def render_sidebar(current: str) -> str:
    """Render full sidebar with logo, nav links, footer. Returns selected page."""
    pages = [("🏠","Home","home"),("🔍","Review","review"),("📊","History","history")]
    selected = current

    with st.sidebar:
        # Logo
        st.markdown(
            '<div class="rb-logo">'
            '<span class="rb-logo-icon">🤖</span>'
            '<span class="rb-logo-text">ReviewBot</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="border-top:1px solid var(--border);margin-bottom:10px;"></div>',
            unsafe_allow_html=True,
        )

        # Nav links via st.button (styled via CSS to look like links)
        for icon, label, key in pages:
            is_active = current == key
            # inject per-button override
            st.markdown(
                f'<style>#btn_{key} button{{"border-left-color:{"var(--accent)" if is_active else "transparent"} !important;'
                f'background:{"rgba(47,129,247,0.1)" if is_active else "transparent"} !important;'
                f'color:{"var(--accent)" if is_active else "var(--text3)"} !important;'
                f'border:none !important; border-left: 2px solid {"var(--accent)" if is_active else "transparent"} !important;'
                f'border-radius:var(--r-sm) !important;padding:8px 10px !important;'
                f'font-weight:500 !important;font-size:13.5px !important;text-align:left !important;'
                f'justify-content:flex-start !important;width:100% !important;gap:9px !important;}}</style>',
                unsafe_allow_html=True,
            )
            with st.container():
                st.markdown(f'<span id="btn_{key}">', unsafe_allow_html=True)
                if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                    selected = key
                st.markdown('</span>', unsafe_allow_html=True)

        # Spacer pushes footer down
        st.markdown('<div style="flex:1;min-height:2rem;"></div>', unsafe_allow_html=True)

        # Footer — always at bottom, never overlaps nav
        st.markdown(
            '<div class="rb-nav-footer">'
            '<p>Powered by Groq + LLaMA 3</p>'
            '<a href="https://github.com" target="_blank">⭐ Star on GitHub</a>'
            '</div>',
            unsafe_allow_html=True,
        )

    return selected


def step_indicator(current: int) -> None:
    """Render 3-step progress bar."""
    steps = [(1,"Input"),(2,"Select Files"),(3,"Results")]
    parts = ['<div class="rb-steps">']
    for i,(n,label) in enumerate(steps):
        cls = "s-active" if n==current else ("s-done" if n<current else "")
        dot = "✓" if n < current else str(n)
        parts.append(
            f'<div class="rb-step-item {cls}">'
            f'<div class="rb-step-circle">{dot}</div>'
            f'<span>{label}</span></div>'
        )
        if i < 2:
            parts.append('<div class="rb-step-line"></div>')
    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)


def section_label(text: str) -> None:
    st.markdown(f'<span class="rb-section-label">{text}</span>', unsafe_allow_html=True)


def badge(level: str) -> str:
    _, cls, icon, tip = SEV.get(level, SEV["SUGGESTION"])
    return f'<span class="rb-badge {cls}" title="{tip}">{icon} {level}</span>'


def issue_card(issue: dict) -> None:
    level = issue.get("severity","SUGGESTION")
    ic_cls, _, icon, _ = SEV.get(level, SEV["SUGGESTION"])
    lang = issue.get("language","python")

    st.markdown(
        f'<div class="rb-issue {ic_cls}">'
        f'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">'
        f'{badge(level)}'
        f'<span style="font-size:11.5px;color:var(--text3);">Line {issue.get("line","?")}</span>'
        f'<span style="font-size:11.5px;color:var(--text3);margin-left:auto;">'
        f'confidence: {int(float(issue.get("confidence",0.8))*100)}%</span>'
        f'</div>'
        f'<div class="rb-issue-title">{issue.get("title","Issue")}</div>'
        f'<div class="rb-issue-desc">{issue.get("description","")}</div>'
        + (f'<div class="rb-issue-cause">💡 <strong style="color:var(--text2);">Root cause:</strong> {issue["root_cause"]}</div>'
           if issue.get("root_cause") else "")
        + '</div>',
        unsafe_allow_html=True,
    )
    if issue.get("before_code") or issue.get("after_code"):
        c1, c2 = st.columns(2)
        with c1:
            if issue.get("before_code"):
                st.markdown('<p class="rb-code-lbl rb-before-lbl">❌ Before</p>', unsafe_allow_html=True)
                st.code(issue["before_code"], language=lang)
        with c2:
            if issue.get("after_code"):
                st.markdown('<p class="rb-code-lbl rb-after-lbl">✅ After</p>', unsafe_allow_html=True)
                st.code(issue["after_code"], language=lang)
    st.markdown("<hr>", unsafe_allow_html=True)


def metric_card(val, label: str, color: str = "var(--text1)") -> None:
    st.markdown(
        f'<div class="rb-metric">'
        f'<div class="rb-metric-val" style="color:{color};">{val}</div>'
        f'<div class="rb-metric-lbl">{label}</div>'
        f'</div>', unsafe_allow_html=True,
    )


def stat_card(val, label: str, color: str = "var(--text1)") -> None:
    st.markdown(
        f'<div class="rb-stat">'
        f'<div class="rb-stat-val" style="color:{color};">{val}</div>'
        f'<div class="rb-stat-lbl">{label}</div>'
        f'</div>', unsafe_allow_html=True,
    )


def empty_state(icon: str, title: str, sub: str) -> None:
    st.markdown(
        f'<div class="rb-empty">'
        f'<div class="rb-empty-icon">{icon}</div>'
        f'<div class="rb-empty-title">{title}</div>'
        f'<div class="rb-empty-sub">{sub}</div>'
        f'</div>', unsafe_allow_html=True,
    )


def lang_pill(language: str) -> None:
    color = LANG_COLORS.get(language.lower(), "#6E7681")
    st.markdown(
        f'<span class="rb-lang">'
        f'<span class="rb-dot" style="background:{color};"></span>'
        f'{language.upper()}</span>', unsafe_allow_html=True,
    )


def hint(text: str) -> None:
    st.markdown(f'<p class="rb-hint">{text}</p>', unsafe_allow_html=True)


def spacer(h: str = "1rem") -> None:
    st.markdown(f'<div style="height:{h};"></div>', unsafe_allow_html=True)
