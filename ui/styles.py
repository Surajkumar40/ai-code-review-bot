"""ReviewBot — Premium SaaS CSS. Every pixel intentional."""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:        #0D1117;
  --bg2:       #161B22;
  --bg3:       #21262D;
  --border:    #30363D;
  --border2:   #3D444D;
  --accent:    #2F81F7;
  --accent-h:  #388BFD;
  --accent-g:  rgba(47,129,247,0.18);
  --text1:     #E6EDF3;
  --text2:     #8B949E;
  --text3:     #6E7681;
  --red:       #F85149;
  --amber:     #D29922;
  --green:     #3FB950;
  --font:      'Inter', system-ui, sans-serif;
  --mono:      'JetBrains Mono', monospace;
  --r:         10px;
  --r-sm:      6px;
  --tr:        0.15s ease;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
.main, .stApp {
  background: var(--bg) !important;
  color: var(--text1) !important;
  font-family: var(--font) !important;
  font-size: 14px;
  line-height: 1.65;
}

#MainMenu, footer, header,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
  display: none !important;
  visibility: hidden !important;
  height: 0 !important;
}

.block-container {
  padding: 2rem 2rem 4rem !important;
  max-width: 1080px !important;
  margin: 0 auto !important;
}

/* ── SIDEBAR ─────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border) !important;
  width: 240px !important;
  min-width: 240px !important;
  max-width: 240px !important;
}
section[data-testid="stSidebar"] > div:first-child {
  display: flex !important;
  flex-direction: column !important;
  height: 100vh !important;
  padding: 0 !important;
  overflow: hidden !important;
}
section[data-testid="stSidebar"] .block-container {
  padding: 0 !important;
  flex: 1 !important;
  display: flex !important;
  flex-direction: column !important;
}
[data-testid="stSidebarContent"] {
  display: flex !important;
  flex-direction: column !important;
  height: 100% !important;
  padding: 1.25rem 0.875rem !important;
  gap: 2px !important;
}

/* ── TYPOGRAPHY ──────────────────────────────────────────── */
h1,h2,h3,h4,h5,h6 {
  font-family: var(--font) !important;
  color: var(--text1) !important;
  font-weight: 600 !important;
  letter-spacing: -0.02em !important;
  line-height: 1.25 !important;
}
p { color: var(--text2) !important; }
label {
  color: var(--text2) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  letter-spacing: 0.01em !important;
}
code, pre { font-family: var(--mono) !important; }

/* ── BUTTONS ─────────────────────────────────────────────── */
.stButton > button {
  font-family: var(--font) !important;
  font-weight: 500 !important;
  font-size: 13.5px !important;
  padding: 8px 20px !important;
  border-radius: var(--r-sm) !important;
  border: 1px solid var(--accent) !important;
  background: var(--accent) !important;
  color: #ffffff !important;
  transition: background var(--tr), box-shadow var(--tr), transform var(--tr) !important;
  cursor: pointer !important;
  letter-spacing: 0.01em !important;
  line-height: 1.4 !important;
}
.stButton > button:hover {
  background: var(--accent-h) !important;
  border-color: var(--accent-h) !important;
  box-shadow: 0 0 0 4px var(--accent-g) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button[kind="secondary"],
.stButton > button[data-testid*="secondary"] {
  background: transparent !important;
  border-color: var(--border2) !important;
  color: var(--text2) !important;
}
.stButton > button[kind="secondary"]:hover {
  border-color: var(--accent) !important;
  color: var(--accent) !important;
  box-shadow: none !important;
  background: var(--accent-g) !important;
  transform: none !important;
}

/* ── INPUTS ──────────────────────────────────────────────── */
[data-testid="stTextInput"] > div > div {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-sm) !important;
  transition: border-color var(--tr), box-shadow var(--tr) !important;
}
[data-testid="stTextInput"] input {
  background: transparent !important;
  color: var(--text1) !important;
  font-family: var(--font) !important;
  font-size: 14px !important;
  caret-color: var(--accent) !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--text3) !important; }
[data-testid="stTextInput"] > div > div:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px var(--accent-g) !important;
}

/* ── FILE UPLOADER ───────────────────────────────────────── */
[data-testid="stFileUploader"] > div {
  background: var(--bg3) !important;
  border: 2px dashed var(--border2) !important;
  border-radius: var(--r) !important;
  padding: 2rem 1.5rem !important;
  text-align: center !important;
  transition: border-color var(--tr), background var(--tr) !important;
  cursor: pointer !important;
}
[data-testid="stFileUploader"] > div:hover {
  border-color: var(--accent) !important;
  background: rgba(47,129,247,0.04) !important;
}
[data-testid="stFileUploader"] label {
  color: var(--text1) !important;
  font-size: 14px !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] p {
  color: var(--text3) !important;
  font-size: 13px !important;
}

/* ── TABS ────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-sm) !important;
  padding: 3px !important;
  gap: 2px !important;
}
[data-testid="stTabs"] [role="tab"] {
  background: transparent !important;
  border: none !important;
  border-radius: 5px !important;
  color: var(--text3) !important;
  font-weight: 500 !important;
  font-size: 13.5px !important;
  padding: 7px 18px !important;
  transition: all var(--tr) !important;
  font-family: var(--font) !important;
}
[data-testid="stTabs"] [role="tab"]:hover { color: var(--text2) !important; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  background: var(--bg3) !important;
  color: var(--text1) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"],
[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none !important; }

/* ── EXPANDERS ───────────────────────────────────────────── */
[data-testid="stExpander"] {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
  overflow: hidden !important;
  margin-bottom: 8px !important;
  transition: border-color var(--tr) !important;
}
[data-testid="stExpander"]:hover { border-color: var(--border2) !important; }
[data-testid="stExpander"] > details > summary {
  padding: 14px 18px !important;
  font-weight: 500 !important;
  font-size: 14px !important;
  color: var(--text1) !important;
  background: var(--bg2) !important;
  cursor: pointer !important;
  transition: background var(--tr) !important;
  list-style: none !important;
}
[data-testid="stExpander"] > details > summary:hover { background: var(--bg3) !important; }
[data-testid="stExpander"] > details[open] > summary { border-bottom: 1px solid var(--border) !important; }
[data-testid="stExpander"] > details > div { padding: 1rem 1.125rem !important; }

/* ── CHECKBOXES ──────────────────────────────────────────── */
[data-testid="stCheckbox"] label {
  color: var(--text2) !important;
  font-size: 13.5px !important;
  font-weight: 400 !important;
  gap: 8px !important;
}
[data-testid="stCheckbox"] label:hover { color: var(--text1) !important; }
[data-testid="stCheckbox"] > label > div:first-child {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 4px !important;
}
[data-testid="stCheckbox"] > label > div:first-child[data-checked="true"] {
  background: var(--accent) !important;
  border-color: var(--accent) !important;
}

/* ── DATAFRAME ───────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
  overflow: hidden !important;
}
[data-testid="stDataFrame"] iframe { background: var(--bg2) !important; }

/* ── PROGRESS BAR ────────────────────────────────────────── */
[data-testid="stProgress"] > div {
  background: var(--bg3) !important;
  border-radius: 20px !important;
  height: 6px !important;
  overflow: hidden !important;
}
[data-testid="stProgress"] > div > div {
  background: linear-gradient(90deg, var(--accent), var(--accent-h)) !important;
  border-radius: 20px !important;
  transition: width 0.4s ease !important;
}

/* ── ALERTS ──────────────────────────────────────────────── */
.stAlert {
  border-radius: var(--r) !important;
  border: 1px solid !important;
  font-size: 13.5px !important;
  font-family: var(--font) !important;
}
[data-testid="stAlert"][kind="error"],
div[data-baseweb="notification"][kind="negative"] {
  background: rgba(248,81,73,0.08) !important;
  border-color: rgba(248,81,73,0.3) !important;
  color: #FF7B72 !important;
}
[data-testid="stAlert"][kind="success"] {
  background: rgba(63,185,80,0.08) !important;
  border-color: rgba(63,185,80,0.3) !important;
  color: #56D364 !important;
}
[data-testid="stAlert"][kind="warning"] {
  background: rgba(210,153,34,0.08) !important;
  border-color: rgba(210,153,34,0.3) !important;
  color: #E3B341 !important;
}

/* ── DOWNLOAD BUTTON ─────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  color: var(--text1) !important;
  font-family: var(--font) !important;
}
[data-testid="stDownloadButton"] > button:hover {
  border-color: var(--green) !important;
  color: var(--green) !important;
  background: rgba(63,185,80,0.07) !important;
  box-shadow: none !important;
  transform: none !important;
}

/* ── SPINNER ─────────────────────────────────────────────── */
[data-testid="stSpinner"] > div {
  border-color: var(--border) transparent transparent transparent !important;
  border-top-color: var(--accent) !important;
}

/* ── SCROLLBAR ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--text3); }

/* ── DIVIDER ─────────────────────────────────────────────── */
hr {
  border: none !important;
  border-top: 1px solid var(--border) !important;
  margin: 1.5rem 0 !important;
}

/* ══════════════════════════════════════════════════════════
   REVIEWBOT COMPONENTS
══════════════════════════════════════════════════════════ */

/* Logo */
.rb-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0.5rem 0.25rem 1.25rem;
  text-decoration: none;
}
.rb-logo-icon { font-size: 1.3rem; }
.rb-logo-text {
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #E6EDF3 0%, #79B8FF 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Nav links */
.rb-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}
.rb-nav-item {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 8px 10px;
  border-radius: var(--r-sm);
  border: none;
  border-left: 2px solid transparent;
  background: transparent;
  color: var(--text3);
  font-family: var(--font);
  font-size: 13.5px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--tr);
  text-align: left;
  width: 100%;
  outline: none;
}
.rb-nav-item:hover {
  background: var(--bg3);
  color: var(--text1);
  border-left-color: var(--border2);
}
.rb-nav-item.active {
  background: rgba(47,129,247,0.1);
  color: var(--accent);
  border-left-color: var(--accent);
}
.rb-nav-icon { font-size: 15px; opacity: 0.85; }

/* Nav footer */
.rb-nav-footer {
  border-top: 1px solid var(--border);
  padding-top: 0.875rem;
  margin-top: auto;
}
.rb-nav-footer p {
  font-size: 11px !important;
  color: var(--text3) !important;
  margin: 0 0 5px !important;
  line-height: 1.4 !important;
}
.rb-nav-footer a {
  font-size: 11.5px;
  color: var(--accent);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: opacity var(--tr);
}
.rb-nav-footer a:hover { opacity: 0.75; }

/* Step indicator */
.rb-steps {
  display: flex;
  align-items: center;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 10px 20px;
  margin-bottom: 1.75rem;
  gap: 0;
}
.rb-step-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  border-radius: var(--r-sm);
  font-size: 13px;
  font-weight: 500;
  color: var(--text3);
  transition: all var(--tr);
  white-space: nowrap;
}
.rb-step-item.s-active { color: var(--accent); background: rgba(47,129,247,0.1); }
.rb-step-item.s-done   { color: var(--green); }
.rb-step-circle {
  width: 22px; height: 22px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; font-weight: 700;
  background: var(--bg3);
  border: 1.5px solid var(--border2);
  flex-shrink: 0;
  transition: all var(--tr);
}
.rb-step-item.s-active .rb-step-circle { background: var(--accent); border-color: var(--accent); color: #fff; }
.rb-step-item.s-done   .rb-step-circle { background: var(--green); border-color: var(--green);   color: #fff; }
.rb-step-line { flex: 1; height: 1px; background: var(--border); }

/* Section label */
.rb-section-label {
  font-size: 11px !important;
  font-weight: 600 !important;
  color: var(--text3) !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
  margin-bottom: 0.875rem !important;
  display: block !important;
}

/* Cards */
.rb-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 1.25rem;
  height: 100%;
  transition: border-color var(--tr), transform var(--tr), box-shadow var(--tr);
}
.rb-card:hover {
  border-color: var(--border2);
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.rb-card-glow:hover {
  border-color: rgba(47,129,247,0.5);
  box-shadow: 0 8px 24px rgba(47,129,247,0.12);
}

/* Feature cards */
.rb-feat-icon { font-size: 1.5rem; margin-bottom: 0.75rem; }
.rb-feat-title {
  font-size: 0.9rem; font-weight: 600;
  color: var(--text1); margin-bottom: 0.35rem;
  display: block;
}
.rb-feat-desc { font-size: 13px; color: var(--text2); line-height: 1.55; }

/* Stat cards */
.rb-stat {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 1.1rem 0.875rem;
  text-align: center;
  transition: border-color var(--tr);
}
.rb-stat:hover { border-color: var(--border2); }
.rb-stat-val {
  font-size: 2rem; font-weight: 700;
  line-height: 1; letter-spacing: -0.03em;
}
.rb-stat-lbl {
  font-size: 11px; color: var(--text3);
  margin-top: 6px; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.07em;
}

/* Metric cards (results row) */
.rb-metric {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 0.9rem 0.75rem;
  text-align: center;
  transition: border-color var(--tr);
}
.rb-metric:hover { border-color: var(--border2); }
.rb-metric-val {
  font-size: 1.65rem; font-weight: 700;
  line-height: 1; letter-spacing: -0.02em;
}
.rb-metric-lbl {
  font-size: 10.5px; color: var(--text3);
  margin-top: 5px; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.07em;
}

/* Severity badges */
.rb-badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 2px 10px; border-radius: 20px;
  font-size: 10.5px; font-weight: 700;
  letter-spacing: 0.05em; text-transform: uppercase;
  white-space: nowrap;
}
.rb-crit { background: rgba(248,81,73,0.12);  color: #FF7B72; border: 1px solid rgba(248,81,73,0.25); }
.rb-warn { background: rgba(210,153,34,0.12); color: #E3B341; border: 1px solid rgba(210,153,34,0.25); }
.rb-sugg { background: rgba(47,129,247,0.12); color: #79B8FF; border: 1px solid rgba(47,129,247,0.25); }

/* Issue cards */
.rb-issue {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-left: 3px solid transparent;
  border-radius: var(--r);
  padding: 1rem 1.125rem;
  margin-bottom: 8px;
  animation: fadeUp 0.25s ease forwards;
}
.rb-issue.ic-crit { border-left-color: var(--red); }
.rb-issue.ic-warn { border-left-color: var(--amber); }
.rb-issue.ic-sugg { border-left-color: var(--accent); }
.rb-issue-title {
  font-size: 14px; font-weight: 600;
  color: var(--text1); margin: 7px 0 5px;
}
.rb-issue-desc  { font-size: 13px; color: var(--text2); line-height: 1.6; }
.rb-issue-cause { font-size: 12px; color: var(--text3); margin-top: 7px; line-height: 1.5; }
.rb-code-lbl { font-size: 11px; font-weight: 700; margin-bottom: 5px; }
.rb-before-lbl { color: #FF7B72; }
.rb-after-lbl  { color: #56D364; }

/* Hero */
.rb-hero {
  padding: 3rem 0 2rem;
  animation: fadeUp 0.4s ease forwards;
}
.rb-hero-title {
  font-size: clamp(2rem, 4vw, 3rem) !important;
  font-weight: 700 !important;
  letter-spacing: -0.03em !important;
  line-height: 1.1 !important;
  background: linear-gradient(135deg, #E6EDF3 30%, #79B8FF 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0 !important;
}
.rb-hero-sub {
  font-size: clamp(0.95rem, 1.5vw, 1.05rem);
  color: var(--text2);
  max-width: 520px;
  line-height: 1.7;
  margin: 1rem 0 1.75rem;
}

/* Lang pill */
.rb-lang {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 3px 11px; border-radius: 20px;
  font-size: 11px; font-weight: 600;
  background: var(--bg3); border: 1px solid var(--border);
  color: var(--text2);
}
.rb-dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }

/* Empty state */
.rb-empty {
  text-align: center;
  padding: 3.5rem 1rem;
  animation: fadeUp 0.3s ease forwards;
}
.rb-empty-icon { font-size: 3rem; margin-bottom: 0.875rem; }
.rb-empty-title {
  font-size: 1.05rem; font-weight: 600;
  color: var(--text1); margin-bottom: 0.4rem;
}
.rb-empty-sub {
  font-size: 13.5px; color: var(--text3);
  max-width: 340px; margin: 0 auto; line-height: 1.6;
}

/* Hint */
.rb-hint { font-size: 11.5px; color: var(--text3); margin-top: 6px; }
.rb-kbd {
  display: inline-block; padding: 1px 6px;
  border-radius: 4px; font-size: 10px;
  font-family: var(--mono);
  background: var(--bg3); border: 1px solid var(--border);
  color: var(--text3);
}

/* Animations */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
.rb-fadein { animation: fadeIn 0.35s ease forwards; }
.rb-fadeup { animation: fadeUp 0.35s ease forwards; }

/* Responsive */
@media (max-width: 900px) {
  .block-container { padding: 1.25rem 1rem 3rem !important; }
  section[data-testid="stSidebar"] { width: 200px !important; min-width: 200px !important; }
}
@media (max-width: 768px) {
  .rb-steps { padding: 8px 12px !important; }
  .rb-step-item { font-size: 11.5px !important; padding: 4px 8px !important; }
  .block-container { padding: 1rem 0.75rem 2rem !important; }
}
</style>
"""

def inject_css() -> None:
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
