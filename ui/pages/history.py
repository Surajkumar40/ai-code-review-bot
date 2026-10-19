"""History page — past reviews table, score trend chart, clear action."""
from __future__ import annotations
from datetime import datetime
import plotly.graph_objects as go
import streamlit as st
from ui.components import empty_state, section_label, spacer
from utils.history import load_history, clear_history


def render() -> None:
    st.markdown(
        '<h2 style="font-size:1.35rem;font-weight:700;color:var(--text1);'
        'letter-spacing:-0.02em;margin-bottom:0.25rem;">Review History</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:var(--text2);font-size:13.5px;margin-bottom:1.5rem;">'
        'Track how your codebase health improves over time.</p>',
        unsafe_allow_html=True,
    )

    history = load_history()

    if not history:
        empty_state(
            "📭",
            "No reviews yet",
            "Run your first code review and it will appear here with score tracking.",
        )
        return

    # ── Summary table ──────────────────────────────────────────────────────
    rows = []
    for e in reversed(history):
        ts = e.get("timestamp", 0)
        date_str = datetime.fromtimestamp(ts).strftime("%b %d, %Y  %H:%M") if ts else "—"
        score = e.get("health_score", 0)
        rows.append({
            "Repo / File": e.get("name", "Unknown"),
            "Date":        date_str,
            "Score":       score,
            "Issues":      e.get("total_issues", 0),
            "Critical":    e.get("critical_count", 0),
            "Warnings":    e.get("warning_count", 0),
        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score",
                min_value=0,
                max_value=100,
                format="%d / 100",
            ),
            "Critical": st.column_config.NumberColumn("🔴 Critical"),
            "Warnings":  st.column_config.NumberColumn("🟡 Warnings"),
        },
    )

    spacer("1.5rem")

    # ── Score trend chart ──────────────────────────────────────────────────
    if len(history) >= 2:
        section_label("Score Trend")

        dates  = [datetime.fromtimestamp(e.get("timestamp", 0)).strftime("%b %d") for e in history]
        scores = [e.get("health_score", 0) for e in history]

        # Color-coded markers
        marker_colors = []
        for s in scores:
            if s >= 70:   marker_colors.append("#3FB950")
            elif s >= 40: marker_colors.append("#D29922")
            else:         marker_colors.append("#F85149")

        fig = go.Figure()

        # Area fill
        fig.add_trace(go.Scatter(
            x=dates, y=scores,
            mode="none",
            fill="tozeroy",
            fillcolor="rgba(47,129,247,0.06)",
            showlegend=False,
            hoverinfo="skip",
        ))

        # Line + markers
        fig.add_trace(go.Scatter(
            x=dates, y=scores,
            mode="lines+markers",
            name="Health Score",
            line={"color": "#2F81F7", "width": 2.5, "shape": "spline", "smoothing": 0.8},
            marker={
                "color": marker_colors,
                "size": 8,
                "line": {"color": "#0D1117", "width": 2},
            },
            hovertemplate="<b>%{x}</b><br>Score: %{y}/100<extra></extra>",
        ))

        # Reference lines
        fig.add_hline(y=70, line_dash="dot", line_color="rgba(63,185,80,0.25)", line_width=1)
        fig.add_hline(y=40, line_dash="dot", line_color="rgba(210,153,34,0.25)", line_width=1)

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"family": "Inter", "color": "#8B949E"},
            xaxis={
                "showgrid": False,
                "color": "#6E7681",
                "tickfont": {"size": 12},
                "linecolor": "#30363D",
            },
            yaxis={
                "showgrid": True,
                "gridcolor": "#21262D",
                "gridwidth": 1,
                "range": [0, 108],
                "color": "#6E7681",
                "tickfont": {"size": 12},
                "ticksuffix": " ",
            },
            height=290,
            margin={"t": 20, "b": 35, "l": 45, "r": 20},
            showlegend=False,
            hoverlabel={
                "bgcolor": "#161B22",
                "bordercolor": "#30363D",
                "font": {"family": "Inter", "size": 13, "color": "#E6EDF3"},
            },
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Legend hint
        st.markdown(
            '<p style="font-size:11.5px;color:var(--text3);margin-top:-8px;">'
            '<span style="color:#3FB950;">●</span> ≥70 Excellent &nbsp;'
            '<span style="color:#D29922;">●</span> ≥40 Fair &nbsp;'
            '<span style="color:#F85149;">●</span> &lt;40 Critical &nbsp;&nbsp;'
            '— Dashed lines at 70 and 40</p>',
            unsafe_allow_html=True,
        )

    spacer("0.5rem")
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Clear history ──────────────────────────────────────────────────────
    section_label("Danger Zone")

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button("🗑️  Clear All History", type="secondary", use_container_width=True):
            st.session_state["confirm_clear"] = True

    if st.session_state.get("confirm_clear"):
        spacer("0.5rem")
        st.markdown(
            '<div style="background:rgba(248,81,73,0.07);border:1px solid rgba(248,81,73,0.25);'
            'border-radius:10px;padding:1rem 1.25rem;margin-bottom:0.75rem;">'
            '<p style="color:#FF7B72;font-weight:600;margin-bottom:4px;font-size:14px;">⚠️ Are you sure?</p>'
            '<p style="color:var(--text2);font-size:13px;margin:0;">'
            'This will permanently delete all review history and score data. This cannot be undone.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        cy, cn, _ = st.columns([1, 1, 4], gap="small")
        with cy:
            if st.button("Yes, delete all", use_container_width=True):
                clear_history()
                st.session_state.pop("confirm_clear", None)
                st.toast("🗑️ History cleared successfully")
                st.rerun()
        with cn:
            if st.button("Cancel", type="secondary", use_container_width=True):
                st.session_state.pop("confirm_clear", None)
                st.rerun()

    spacer("2rem")
