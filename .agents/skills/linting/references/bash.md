# Bash linting with ShellCheck

Use the repository's lint command when defined; otherwise run these checks from the repository
root. Respect `.shellcheckrc` when present.

- Lint: `shellcheck <file>`.
- Format check: not applicable unless the repository defines a shell formatter.
- Syntax check: `bash -n <file>`.
- Fix: ShellCheck does not rewrite files; resolve findings by hand.

Official reference: [ShellCheck](https://www.shellcheck.net/wiki/).
