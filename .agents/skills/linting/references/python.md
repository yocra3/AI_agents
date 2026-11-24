# Python linting with Ruff

Use the repository's lint command when defined; otherwise run these checks from the repository
root. Respect Ruff configuration in `pyproject.toml` or `ruff.toml` when present.

- Lint: `ruff check <file>`.
- Format check: `ruff format --check <file>`.
- Syntax check: `python3 -m py_compile <file>`.
- Docstring check, only when the task adds or changes docstrings: the repository's docstring
  lint, otherwise `ruff check --select D <file>`, adding
  `--config "lint.pydocstyle.convention = 'google'"` when the Ruff configuration sets no
  convention.
- Fix: `ruff check --fix <file>` and `ruff format <file>`; resolve remaining findings by hand.

Official reference: [Ruff](https://docs.astral.sh/ruff/).
