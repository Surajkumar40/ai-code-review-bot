# 🤖 ReviewBot — AI Code Review for Serious Engineers

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square)
![Powered by Groq](https://img.shields.io/badge/Powered%20by-Groq%20LLaMA%203-orange?style=flat-square)

> Catch bugs, security vulnerabilities, and code smells before they hit production. Powered by LLaMA 3 on Groq — results in seconds, not minutes.

---

## ✨ Features

- ✅ **GitHub + File Upload** — Paste any public GitHub URL or upload a local file
- ✅ **Multi-Language** — Python, JavaScript, TypeScript, Java, C++
- ✅ **Severity Grading** — CRITICAL / WARNING / SUGGESTION with before/after fixes
- ✅ **Health Score** — 0–100 gauge per review with trend tracking
- ✅ **Exportable Reports** — Full Markdown report with one click
- ✅ **Review History** — Compare scores over time with a trend chart
- ✅ **Retry Logic** — Exponential backoff via Tenacity — no flaky reviews
- ✅ **Premium UI** — GitHub Dark theme, zero default Streamlit aesthetics

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/reviewbot
cd reviewbot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your secrets
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 4. Run
streamlit run app.py
```

**Get your free Groq API key:** https://console.groq.com

---

## 🗂️ Architecture

```mermaid
graph TD
    A[app.py] --> B[ui/pages/home.py]
    A --> C[ui/pages/review.py]
    A --> D[ui/pages/history.py]
    C --> E[core/reviewer.py]
    E --> F[api/groq_client.py]
    E --> G[api/github_client.py]
    F --> H[core/prompt_builder.py]
    E --> I[core/scorer.py]
    E --> J[utils/cache.py]
    C --> K[utils/report.py]
    D --> L[utils/history.py]
    L --> M[data/history.json]
```

---

## 📸 Screenshots

> _Demo screenshots coming soon_

---

## 🔮 Roadmap

- [ ] **PR Review Mode** — comment directly on GitHub pull requests
- [ ] **Team Workspace** — shared review history with org-level stats
- [ ] **IDE Extension** — VS Code extension for in-editor reviews
- [ ] **Custom Rulesets** — import ESLint/Pylint configs as review context
- [ ] **CI/CD Integration** — GitHub Action that fails builds on CRITICAL issues

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
