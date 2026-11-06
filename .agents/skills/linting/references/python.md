# Python linting with Ruff

Use the repository's lint command when defined; otherwise run these checks from the repository
root. Respect Ruff configuration in `pyproject.toml` or `ruff.toml` when present.

- Lint: `ruff check <file>`.
- Format check: `ruff format --check <file>`.
- Syntax check: `python3 -m py_compile <file>`.
- Fix: `ruff check --fix <file>` and `ruff format <file>`; resolve remaining findings by hand.

Official reference: [Ruff](https://docs.astral.sh/ruff/).
