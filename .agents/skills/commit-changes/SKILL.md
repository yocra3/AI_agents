---
name: commit-changes
description: Create reviewed local commits when requested, or at a commit point of an active implementation_coordinator. Never publish or rewrite history.
---

# Committing Changes Skill

Use this skill only when the user explicitly asks for a local commit or an active coordinator
reaches a commit point. An active implementation_coordinator commits only at its approval,
planning, and status commits and at the green commit points of the implementation plan it
executes.

Commit completed preparatory cycles before any later human review. Do not commit a failing or
incomplete cycle. When authorized:

1. **Check for uncommitted changes**:
  - Use `git status` to see if there are any uncommitted changes.
2. **Group changes**:
  - If there are multiple files changed, group them logically if possible.
  - Decide on meaningful commit messages for each group.
3. **Stage changes**:
  - Stage only reviewed files for each group.
  - Avoid `git add .` unless the user explicitly asks to include every change.
4. **Commit changes**:
  - Commit the staged changes using [conventional commit messages](./conventional-commits.md) guidelines.
5. **Keep commits local**:
  - Do not push, merge into the default branch, or rewrite history unless explicitly requested.

Report the reviewed files, commit hash and message, remaining worktree state, and any
blocker. Do not include unrelated changes in the commit.
