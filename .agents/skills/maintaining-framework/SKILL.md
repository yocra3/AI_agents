---
name: maintaining-framework
description: Change the framework's agents, skills, templates, references, or phase entries, regenerate the agents of every environment and the catalog, and keep references and documentation in sync. Use from craftsman for every framework change. Do not use for product code or project documents.
---

# Purpose

Apply a requested framework change so that every environment gets the same behavior, no
reference is left dangling, and the documentation describes the result. Follow the principles in
`{Agents_Folder}/references/framework-principles.md`; resolve `{Agents_Folder}` from
`{Agents_file}`.

# Agents

- Edit only the neutral source `{Agents_Folder}/agents/<name>.md`. Never edit
  `.claude/agents/*.md` or `.codex/agents/*.toml`: they are generated, and a hand edit is lost.
- A source has this frontmatter, and its body is the agent's instructions, the same in every
  environment:

  ```yaml
  ---
  name: <hyphenated-name, equal to the file name>
  description: <responsibility and activation boundary, one line>
  codex:
    model: <Codex model>
    model_reasoning_effort: <low | medium | high | ...>
    sandbox_mode: <read-only | workspace-write>
    disabled_skills:        # optional: skills the agent must not use
      - <skill-name>
  claude:
    model: <Claude Code model>
    effort: <Claude Code effort>
    tools: Read, Grep, Glob, Skill, <other tools>
  ---
  ```

  Take `claude.model` from the model equivalence in the framework's `README.md` unless the user
  sets an override for the agent.
- Create or reformat an agent with `{Agents_Folder}/templates/agents.template.md`. To remove an
  agent, delete its source and its two generated files.
- Regenerate from the repository root:

  ```bash
  python3 {Agents_Folder}/scripts/generate_agents.py
  ```

  It writes `.claude/agents/<name>.md` and `.codex/agents/<name>.toml` from each source, with the
  name each environment expects, and `docs/catalog.md` where the repository keeps one. It lists,
  and never changes, agent files without a source, such as a project's own agents.
- Review the regenerated files with read-only `git diff -- .claude/agents .codex/agents docs`.
  Every difference must follow from the change to the sources; report any other. When the
  generator rejects a source, fix the source; do not edit the generator only to make it pass.
- As the final verification, run the generator with `--check`, which writes nothing and exits
  non-zero when a generated file is out of date, and parse every generated `.toml` with a TOML
  parser.

# Skills

- Use the skill-creator skill of the current environment for the structure, frontmatter
  `description`, and validation of a skill.
- A skill that must run only on explicit request also gets `agents/openai.yaml` with
  `allow_implicit_invocation: false`, and the agents that must not use it list it in their
  `codex.disabled_skills`.
- A skill's private files are read only by that skill; move material that another skill or
  agent needs to `{Agents_Folder}/references/`.

# Phase entries

Each phase or delegation that is not a plan marker has one entry in the file of
`{Agents_Folder}/references/phases/` for its plan type: `common.md`, `specs.md`, `nextflow.md`,
or `analysis.md`. The coordinator pastes entries verbatim into a delegate's brief, so write each
entry to the delegate, complete on its own, in this format:

```markdown
## `<agent>: <phase>`

- **Meaning**: <one line>. <For a delegation that is not a plan marker: "Not a plan marker:
  delegated <when>.">
- **Skill**: <the skill the delegate uses, or none>.
- **Steps**:
  1. <exact step, including when to lint with the linting skill>
- **Evidence**: <what the delegate returns>.
- **Stops**: <its own stop conditions, "none of its own", or "the skill's stops">.
```

- Rules that apply to every phase of a plan type go in its "Rules for every phase" section.
- A rule of a common phase that holds only for one plan type goes in that type's rules of other
  phases, under the phase ID, not in the entry.
- The plan templates of planning-specs and planning-analysis name the markers and their order;
  update them, `agent-delegation`, and the CHANGELOG when an ID changes.

# References and documentation

- After moving, renaming, or removing content, search the repository for its old names, paths,
  and section titles, and fix every dangling reference.
- Update, where they describe what changed: the Unreleased section of
  `{Agents_Folder}/CHANGELOG.md`, rewriting any entry that the change supersedes so that it
  states the net change from the last released version; `README.md`, whose Programming workflow
  and Analysis workflow subsections hold the only figure of each flow; and
  `docs/programming-workflow.md` and `docs/analysis-workflow.md`.
- Regenerate the agents, which also regenerates `docs/catalog.md` from the agent and skill
  descriptions and the first sentence of each template and reference; keep that sentence a
  description of the file.

# Output

Return the changed, created, and deleted files, the generator's output and `--check` result, the
dangling references fixed and left, and the documentation updated.
