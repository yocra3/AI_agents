# Agent template

Use this template for the neutral source of an agent, `{Agents_Folder}/agents/<agent-name>.md`,
from which `{Agents_Folder}/scripts/generate_agents.py` generates the agent of each environment.
Resolve global placeholders and keep only the sections and settings that materially change the
agent's behavior.

```markdown
---
name: {agent-name}
description: {Specific responsibility and activation boundary.}
codex:
  model: {Codex model}
  model_reasoning_effort: {none|low|medium|high|xhigh|max}
  sandbox_mode: {read-only|workspace-write}
  disabled_skills:
    - project-bootstrap
claude:
  model: {Claude Code model}
  effort: {low|medium|high|xhigh|max}
  tools: Read, Grep, Glob, Skill, {other tools the agent needs}
---
# Role
Act as {role and ownership}. {Invoked as a delegate, as the main session, or both.} Resolve global
placeholders from `{Agents_file}`, and read {the context the agent needs}.

# Goal
Produce {observable outcome}. Success means {concise success criteria}.

# Skills
- {skill}: {when to use it}.
{For an agent that runs implementation plan phases: Follow the phase instructions in the
delegation exactly; they name the skill to use among {skills}.}

# {Agent-specific section}
{Only what is specific to this agent and valid for any of its tasks, such as a clarification gate
that says when to ask the user with AskUserQuestion and wait.}

# Boundaries
Do not {out-of-scope work, implicit side effects, or unauthorized Git or network operations}.

# Output
Return {artifact paths, decisions, evidence, validation, and blockers}. {For an agent that runs
implementation plan phases: the evidence that the phase instructions request.}
```

## Adaptation rules

- Every agent has Role, Goal, Skills, Boundaries, and Output, in that order, with its own
  sections between Skills and Boundaries.
- Declare the available tools only in the frontmatter. Say when to use a tool in the section where
  it is used, and what context to read in Role, or in Skills when the skill already says it.
- List in Skills every skill the agent can use, also those it uses through another skill. Do not
  name implementation plan phases; they live in `{Agents_Folder}/references/phases/`.
- Use an outcome-first prompt; prescribe steps only when ordering is a real invariant.
- Give each agent one clear owner responsibility.
- Put project-specific paths and commands behind global placeholders or repository instructions.
- Use `workspace-write` only when the agent owns an artifact it must edit.
- Add `disabled_skills` entries only for capabilities the agent must not use.
- Define when the agent asks, proceeds, stops, and reports evidence.
