"""Review page — 3-step flow: Input → Select Files → Results."""
from __future__ import annotations
import os
import streamlit as st
import plotly.graph_objects as go
from ui.components import (
    step_indicator, section_label, issue_card,
    metric_card, empty_state, lang_pill, hint, spacer, badge,
)
from utils.report import generate_markdown_report
from utils.history import save_review

EXT_LANG = {
    ".py":"python",".js":"javascript",".ts":"typescript",
    ".java":"java",".cpp":"cpp",".cc":"cpp",".h":"cpp",".hpp":"cpp",
}
LANG_ICONS = {"python":"🐍","javascript":"📜","typescript":"🔷","java":"☕","cpp":"⚙️","unknown":"📄"}

def _detect(fname: str) -> str:
    return EXT_LANG.get(os.path.splitext(fname)[1].lower(), "unknown")

def _gauge(score: int, color: str) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score,
        domain={"x":[0,1],"y":[0,1]},
        title={"text":"Health Score","font":{"size":13,"color":"#8B949E","family":"Inter"}},
        number={"font":{"size":48,"color":color,"family":"Inter"},"suffix":""},
        gauge={
            "axis":{"range":[0,100],"tickwidth":1,"tickcolor":"#30363D",
                    "tickfont":{"color":"#6E7681","size":10}},
            "bar":{"color":color,"thickness":0.22},
            "bgcolor":"#161B22","borderwidth":0,
            "steps":[
                {"range":[0,40],"color":"rgba(248,81,73,0.07)"},
                {"range":[40,70],"color":"rgba(210,153,34,0.07)"},
                {"range":[70,100],"color":"rgba(63,185,80,0.07)"},
            ],
            "threshold":{"line":{"color":color,"width":3},"thickness":0.75,"value":score},
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family":"Inter"}, height=240,
        margin={"t":35,"b":10,"l":15,"r":15},
    )
    return fig

def _donut(crit: int, warn: int, sugg: int) -> go.Figure:
    raw = [("Critical",crit,"#F85149"),("Warning",warn,"#D29922"),("Suggestion",sugg,"#2F81F7")]
    data = [(l,v,c) for l,v,c in raw if v > 0] or [("Clean",1,"#3FB950")]
    labels, values, colors = zip(*data)
    fig = go.Figure(go.Pie(
        labels=list(labels), values=list(values), hole=0.64,
        marker={"colors":list(colors),"line":{"color":"#0D1117","width":2}},
        textfont={"color":"#E6EDF3","family":"Inter","size":12},
        hovertemplate="%{label}: %{value}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"family":"Inter","color":"#8B949E"},
        showlegend=True,
        legend={"font":{"color":"#8B949E","size":12},"bgcolor":"rgba(0,0,0,0)",
                "orientation":"v","x":1.0,"y":0.5},
        height=240, margin={"t":20,"b":20,"l":10,"r":10},
    )
    return fig

def render() -> None:
    # init
    defaults = [("review_step",1),("review_result",None),("repo_files",[]),("selected_files",[])]
    for k, v in defaults:
        if k not in st.session_state: st.session_state[k] = v

    step = st.session_state.review_step
    step_indicator(step)

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 1 — Input
    # ══════════════════════════════════════════════════════════════════════════
    if step == 1:
        tab_gh, tab_up = st.tabs(["🔗  GitHub URL", "📁  Upload File"])

        with tab_gh:
            spacer("0.75rem")
            repo_url = st.text_input(
                "Repository URL",
                placeholder="https://github.com/facebook/react",
                key="repo_url_input",
            )
            spacer("4px")
            col_branch, col_btn = st.columns([2.5, 1], gap="small")
            with col_branch:
                branch = st.text_input("Branch", value="main", key="branch_input")
            with col_btn:
                spacer("1.65rem")
                fetch = st.button("Fetch Files →", use_container_width=True)

            hint("💡 Public repos work without a token · Private repos need GITHUB_TOKEN in .env")

            if fetch:
                if not repo_url.strip():
                    st.error("Please enter a GitHub repository URL.")
                else:
                    with st.spinner("Connecting to GitHub..."):
                        try:
                            from api.github_client import get_repo_files
                            files = get_repo_files(repo_url.strip(), branch.strip() or "main")
                            if not files:
                                st.warning("No supported source files found (.py .js .ts .java .cpp).")
                            else:
                                st.session_state.repo_files = files
                                st.session_state.source = "github"
                                st.session_state.review_step = 2
                                st.toast(f"✅ Found {len(files)} files!", icon="✅")
                                st.rerun()
                        except Exception as exc:
                            st.error(f"❌ {str(exc)}")

        with tab_up:
            spacer("0.75rem")
            uploaded = st.file_uploader(
                "Drop your file here, or click to browse",
                type=["py","js","ts","java","cpp","cc","h","hpp"],
                key="file_uploader",
                label_visibility="collapsed",
            )
            hint("Supported: .py  .js  .ts  .java  .cpp  .cc  .h")

            if uploaded:
                lang = _detect(uploaded.name)
                spacer("8px")
                col_lang, col_run = st.columns([2, 1])
                with col_lang:
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:10px;padding:8px 0;">'
                        f'<span style="font-size:13px;color:var(--text2);">Detected:</span>',
                        unsafe_allow_html=True,
                    )
                    lang_pill(lang)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_run:
                    if st.button("Run Review →", use_container_width=True, key="upload_btn"):
                        content = uploaded.read().decode("utf-8", errors="replace")
                        with st.spinner("Reviewing with LLaMA 3..."):
                            try:
                                from core.reviewer import review_uploaded_file
                                result = review_uploaded_file(content, uploaded.name, lang)
                                st.session_state.review_result = result
                                st.session_state.source = "upload"
                                st.session_state.review_step = 3
                                save_review(result, uploaded.name)
                                st.toast("🎉 Review complete!", icon="🎉")
                                st.rerun()
                            except Exception as exc:
                                st.error(f"❌ Review failed: {str(exc)}")

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 2 — File Selector
    # ══════════════════════════════════════════════════════════════════════════
    elif step == 2:
        files = st.session_state.repo_files
        if not files:
            st.session_state.review_step = 1
            st.rerun()

        st.markdown(
            f'<p style="font-size:13.5px;color:var(--text2);margin-bottom:1rem;">'
            f'Found <strong style="color:var(--text1);">{len(files)} supported files</strong>. '
            f'Select which ones to review.</p>',
            unsafe_allow_html=True,
        )

        # Toolbar
        c_all, c_none, c_spacer = st.columns([1, 1, 5], gap="small")
        with c_all:
            if st.button("✓ Select All", use_container_width=True):
                st.session_state.selected_files = [f.path for f in files]
                st.rerun()
        with c_none:
            if st.button("✕ Clear", use_container_width=True, type="secondary"):
                st.session_state.selected_files = []
                st.rerun()

        spacer("0.75rem")
        section_label(f"{len(st.session_state.selected_files)} of {len(files)} selected")

        selected = list(st.session_state.selected_files)

        # Group files by directory for cleaner display
        for f in files:
            icon = LANG_ICONS.get(f.language, "📄")
            label = f"{icon}  {f.path}"
            checked = st.checkbox(
                label,
                value=f.path in selected,
                key=f"cb_{f.path}",
                help=f"{f.language.upper()} · {f.size_kb} KB",
            )
            if checked and f.path not in selected:
                selected.append(f.path)
            elif not checked and f.path in selected:
                selected.remove(f.path)

        st.session_state.selected_files = selected
        spacer("1rem")
        st.markdown("<hr>", unsafe_allow_html=True)

        col_back, col_run = st.columns([1, 2], gap="small")
        with col_back:
            if st.button("← Back", type="secondary", use_container_width=True):
                st.session_state.review_step = 1
                st.rerun()
        with col_run:
            n = len(selected)
            if n == 0:
                hint("☝️ Select at least one file to continue")
            else:
                if st.button(f"Run Review on {n} file{'s' if n>1 else ''} →", use_container_width=True):
                    repo_url = st.session_state.get("repo_url_input","")
                    branch   = st.session_state.get("branch_input","main")
                    pb = st.progress(0)
                    status = st.empty()

                    def _prog(msg: str, frac: float) -> None:
                        pb.progress(min(frac, 1.0))
                        status.markdown(
                            f'<p style="font-size:13px;color:var(--text3);">⏳ {msg}</p>',
                            unsafe_allow_html=True,
                        )
                    try:
                        from core.reviewer import review_github_repo
                        result = review_github_repo(repo_url, branch, selected, _prog)
                        pb.progress(1.0)
                        st.session_state.review_result = result
                        st.session_state.review_step = 3
                        save_review(result, repo_url)
                        st.toast("🎉 Review complete!", icon="🎉")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"❌ {str(exc)}")

    # ══════════════════════════════════════════════════════════════════════════
    # STEP 3 — Results
    # ══════════════════════════════════════════════════════════════════════════
    elif step == 3:
        result = st.session_state.review_result
        if not result:
            st.session_state.review_step = 1
            st.rerun()

        ss = result["score_summary"]
        st.markdown('<div class="rb-fadeup">', unsafe_allow_html=True)

        # ── Charts ──────────────────────────────────────────────────────────
        cg, cd = st.columns(2, gap="medium")
        with cg:
            st.plotly_chart(
                _gauge(ss.health_score, ss.color),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.markdown(
                f'<p style="text-align:center;font-size:0.95rem;font-weight:600;'
                f'color:{ss.color};margin-top:-12px;">{ss.label}</p>',
                unsafe_allow_html=True,
            )
        with cd:
            st.plotly_chart(
                _donut(ss.critical_count, ss.warning_count, ss.suggestion_count),
                use_container_width=True,
                config={"displayModeBar": False},
            )

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Metrics ─────────────────────────────────────────────────────────
        m = st.columns(5, gap="small")
        for col, val, lbl, clr in [
            (m[0], ss.total_issues,       "Total Issues",  "var(--text1)"),
            (m[1], ss.critical_count,     "Critical",      "#FF7B72"),
            (m[2], ss.warning_count,      "Warnings",      "#E3B341"),
            (m[3], ss.suggestion_count,   "Suggestions",   "#79B8FF"),
            (m[4], result["files_reviewed"],"Files",       "var(--green)"),
        ]:
            with col: metric_card(val, lbl, clr)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Issues ──────────────────────────────────────────────────────────
        section_label("Issues by File")

        file_results = result.get("file_results", [])
        all_clean = all(len(fr.get("issues",[])) == 0 for fr in file_results)

        if not file_results or all_clean:
            empty_state("🎉", "No Issues Found", "Your code is clean — nothing was flagged during this review.")
        else:
            for fr in file_results:
                issues = fr.get("issues", [])
                crit_n = sum(1 for i in issues if i.get("severity")=="CRITICAL")
                warn_n = sum(1 for i in issues if i.get("severity")=="WARNING")
                sugg_n = sum(1 for i in issues if i.get("severity")=="SUGGESTION")

                badges_html = ""
                if crit_n: badges_html += f'<span class="rb-badge rb-crit" style="margin-left:8px;">🔴 {crit_n}</span>'
                if warn_n: badges_html += f'<span class="rb-badge rb-warn" style="margin-left:4px;">🟡 {warn_n}</span>'
                if sugg_n: badges_html += f'<span class="rb-badge rb-sugg" style="margin-left:4px;">🔵 {sugg_n}</span>'

                label = f"📄 {fr.get('filename','?')} — {len(issues)} issue{'s' if len(issues)!=1 else ''}"
                with st.expander(label, expanded=(crit_n > 0)):
                    if badges_html:
                        st.markdown(
                            f'<div style="margin-bottom:0.875rem;">{badges_html}</div>',
                            unsafe_allow_html=True,
                        )
                    if fr.get("summary"):
                        st.markdown(
                            f'<p style="font-size:13px;color:var(--text2);'
                            f'margin-bottom:0.875rem;line-height:1.6;">{fr["summary"]}</p>',
                            unsafe_allow_html=True,
                        )
                    if not issues:
                        st.success("✅ No issues found in this file.")
                    else:
                        for iss in issues:
                            issue_card(iss)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Actions ─────────────────────────────────────────────────────────
        col_dl, col_reset = st.columns([2, 1], gap="small")
        with col_dl:
            st.download_button(
                "📥  Download Full Report (.md)",
                data=generate_markdown_report(result),
                file_name="reviewbot_report.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with col_reset:
            if st.button("🔄  Review Another", use_container_width=True, type="secondary"):
                for k in ["review_step","review_result","repo_files","selected_files","source"]:
                    st.session_state.pop(k, None)
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
