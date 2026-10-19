"""
ReviewBot — AI Code Review for Serious Engineers
Entry point: python -m streamlit run app.py
"""
from __future__ import annotations
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

logger.add(
    "reviewbot.log",
    rotation="10 MB",
    retention="7 days",
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} — {message}",
)

st.set_page_config(
    page_title="ReviewBot — AI Code Review",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.styles import inject_css
from ui.components import render_sidebar
from ui.pages import home, review, history

inject_css()

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

selected = render_sidebar(st.session_state.current_page)
if selected != st.session_state.current_page:
    st.session_state.current_page = selected
    st.rerun()

page = st.session_state.current_page

try:
    if page == "home":
        result = home.render()
        if result in ("review", "history"):
            st.session_state.current_page = result
            st.rerun()
    elif page == "review":
        review.render()
    elif page == "history":
        history.render()
    else:
        st.session_state.current_page = "home"
        st.rerun()

except Exception as exc:
    logger.exception(f"Unhandled error on page '{page}': {exc}")
    st.error(f"Something went wrong — **{type(exc).__name__}:** {str(exc)[:300]}")
    if st.button("← Go Home"):
        st.session_state.current_page = "home"
        st.rerun()
