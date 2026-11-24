# Model profiles

The model of each agent profile in each environment, which
`{Agents_Folder}/scripts/generate_agents.py` reads to write the `model` of every generated agent.

Each agent source sets its `profile` and its own `effort`; a profile fixes only the model. To
change a model, edit this table and regenerate the agents.

| Profile | Codex | Claude Code |
| --- | --- | --- |
| `high` | `gpt-6-sol` | `claude-opus-5-5` |
| `medium` | `gpt-6-sol` | `claude-sonnet-5-5` |
| `low` | `gpt-6-luna` | `claude-haiku-5-5` |
