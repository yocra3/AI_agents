# AI_agents

Agent definitions for programming with AI, usable from Codex and Claude Code.

## Contents

- `.agents/`: shared skills (`skills/`), the workflow catalog (`CODEX.md`), the `AGENTS.md` template
  and reference sources.
- `.codex/`: Codex configuration and the 11 custom agents (`agents/*.toml`), which are the source
  of truth.
- `.claude/`: Claude Code settings, the agents generated from `.codex/agents`, and
  `scripts/generate_agents.py`. `.claude/skills` is a symbolic link to `.agents/skills`.

This first version is kept in one piece. It includes Nextflow, Groovy and nf-core profiles and
skills (`coding-spec`, `linting`, `planning-specs`, `generating-specs`, `testing-unit`,
`nfcore-component-reuse`, `importing-nf-core`); remove the ones a target project does not need.

## Install in a project

```bash
./install.sh /path/to/target-repository
```

The script copies the three folders (keeping the symbolic link) and regenerates
`.claude/agents`. It stops if any of them already exists in the target.

Then, in the target repository:

1. Generate `AGENTS.md`, the briefing and the changelog with the `project-bootstrap` skill
   (template in `.agents/templates/agents.template.md`).
2. Add a `CLAUDE.md` that imports it with `@AGENTS.md`, plus the Claude Code notes: agent names use
   hyphens (`product_owner` is `product-owner`), skills are shared through `.claude/skills`, and the
   model equivalence between Codex and Claude Code.
3. Create `agents_data/specs/` and `agents_data/plans/`, where the lifecycle artifacts are stored.

## Update

Change agents in `.codex/agents`, then regenerate the Claude Code copies:

```bash
python3 .claude/scripts/generate_agents.py
```

## Model equivalence

| Codex | Claude Code |
| --- | --- |
| `gpt-6-sol` | `claude-opus-5-5` |
| `gpt-5.6-terra` | `claude-sonnet-5-5` |
| `gpt-6-luna` | `claude-haiku-5-5` |
