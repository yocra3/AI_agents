# Reusable AI agent definitions

This repository is a template for creating AI agents that can be reused across
projects. Agent definitions are Markdown files with YAML front matter describing
the agent and instructions that define its behavior.

## Use an agent in another project

1. Copy `agents/agent-template.md` into the target project's
   `.github/agents/` directory.
2. Rename it to describe the agent, for example `code-reviewer.agent.md`.
3. Replace the placeholder name, description, and instructions with the agent's
   purpose and project-specific guidance.
4. Commit the file to the target project.

Keep agent instructions focused on a clear role, the tasks it should perform,
and any project-specific conventions it must follow. Review the copied
definition in the context of the target project before using it.

## Template contents

- `agents/agent-template.md` — a starting point for a reusable agent definition.
