# Agents Instructions

- **Agents_Folder**: .agents

These instructions apply to work on this repository only; `install.py` does not install this file
or `CLAUDE.md` in projects.

## Working mode

- By default, only discuss. Opinions, wishes, and answers to your questions are not orders to
  edit. Edit files or launch `craftsman` only on an explicit order.
- Make every framework change, to agents, skills, templates, references, or phase entries,
  through `craftsman`, even a small fix. It follows the
  [framework principles](.agents/references/framework-principles.md) and the
  [maintaining-framework](.agents/skills/maintaining-framework/SKILL.md) skill.
- Work in steps. Between steps, review the diff and report errors or inconsistencies before
  continuing.
- Evaluate compatibility and upgrade notes against the last released version, the newest dated
  section of `.agents/CHANGELOG.md`.
- Write repository content in English; the conversation may use another language.

## Commits

- Before a commit, run `python3 .agents/scripts/generate_agents.py --check`; it must report that
  the generated files are up to date.
- Commit only when asked, with the commit-changes skill (Conventional Commits).
