# Contributing to StealthInterview

Thank you for wanting to contribute! StealthInterview is a community-driven project, and we welcome contributions of all kinds — code, documentation, testing, design, and more.

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Pull Request Process](#pull-request-process)
6. [Reporting Bugs](#reporting-bugs)
7. [Feature Requests](#feature-requests)
8. [License](#license)

## 📜 Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold these standards.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Git
- Ollama (for LLM features)

### Setup

```bash
# Fork and clone your fork
git clone https://github.com/YOUR_USERNAME/stealthinterview.git
cd stealthinterview

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_stt.py -v
```

## 🔄 Development Workflow

1. Create a branch from `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests and linting:
   ```bash
   pytest
   flake8 src/
   black --check src/
   isort --check src/
   mypy src/
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: describe your change"
   ```

5. Push and open a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Coding Standards

### Python

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting (line length 100)
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Type hints required for all public functions
- Docstrings using Google style

### Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`, `revert`

Example: `feat: add Whisper STT engine with VAD support`

### File Headers

Each source file should include:

```python
"""
StealthInterview - <module description>
Copyright (C) 2026 StealthInterview Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""
```

## 🔀 Pull Request Process

1. Ensure your branch is up-to-date with `main`
2. All tests must pass
3. Code must follow project standards
4. Update documentation if needed
5. Add tests for new features
6. Request review from maintainers

PRs will be reviewed by maintainers. Please be responsive to review feedback.

## 🐛 Reporting Bugs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md). Include:

- Steps to reproduce
- Expected vs actual behavior
- OS and Python version
- Screenshots or logs if applicable

## ✨ Feature Requests

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md). Describe:

- The problem you're trying to solve
- Your proposed solution
- Alternatives considered
- Additional context

## 📄 License

By contributing, you agree that your contributions will be licensed under the GPLv3.

## 🙏 Thank You

Your contributions make StealthInterview better for everyone. Thank you!