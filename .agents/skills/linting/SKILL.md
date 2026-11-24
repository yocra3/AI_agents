---
name: linting
description: Run lint checks and, when requested, fix lint findings using repository conventions.
---

# Linting

Use the repository's lint commands, pinned tools, and configuration for the requested scope.
Lint each language in scope with the linter that the Tech Stack of `{Agents_file}` declares for
it, and load its profile: [R and R Markdown](references/R.md), [Python](references/python.md), and
[Bash](references/bash.md). For Nextflow projects, load [Nextflow](references/nextflow.md). When
the Tech Stack declares no linter for a language, use the one of its profile; run a declared
linter that has no profile here with its documented check command.

- Run every check the loaded profiles define, without automatic fixes unless the task includes
  corrections.
- When correcting, keep edits focused, review the diff, and re-run the affected checks.
- Do not disable rules merely to obtain a passing result.
- Report commands, results, remaining findings, and unavailable checks.
