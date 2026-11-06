# Bash coding guidelines

Apply to Bash scripts in any project. Repository conventions take precedence. Use Bash to
orchestrate external tools; move structured parsing or computation to R or Python.

## Structure

```bash
#!/usr/bin/env bash
set -euo pipefail
```

## Conventions

- Quote every expansion, use `"$(...)"` instead of backticks, and declare function variables with
  `local`.
- Validate required variables with `: "${NAME:?}"` before use.
- Pass key parameters explicitly to each tool, and never mask a failure with `|| true`.
