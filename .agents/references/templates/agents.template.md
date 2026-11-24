# Agent template

Skeleton of the neutral source of an agent, `{Agents_Folder}/agents/<agent-name>.md`, from which
`{Agents_Folder}/scripts/generate_agents.py` generates the agent of each environment. The rules
of each frontmatter field are in the maintaining-framework skill, and the structure and phase
rules in `{Agents_Folder}/references/framework-principles.md`. Keep only the sections that
materially change the agent's behavior.

```markdown
---
name: {agent-name}
description: {Specific responsibility and activation boundary.}
profile: {high|medium|low}
effort: {low|medium|high|xhigh}
skills:
  - {skill}
codex:
  sandbox_mode: {read-only|workspace-write}
claude:
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

## Writing rules

- State the outcome first; prescribe steps only when their order is a real invariant.
- Give the agent one owner responsibility.
- Say when the agent asks, proceeds, stops, and reports evidence.
- Put project paths and commands behind global placeholders.
