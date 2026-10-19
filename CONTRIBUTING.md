# Contributing to ReviewBot

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/yourusername/reviewbot
cd reviewbot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Code Standards

- **Python 3.11+** required
- **Type hints** on all functions
- **Docstrings** on all public functions and classes
- Run `ruff check .` before submitting a PR

## Pull Request Process

1. Fork the repo and create a feature branch: `git checkout -b feature/my-feature`
2. Write clean, commented code with type hints
3. Ensure `ruff check .` passes with no errors
4. Open a PR with a clear description of what changed and why

## Reporting Bugs

Open a GitHub Issue with steps to reproduce, expected behavior, and actual behavior.
