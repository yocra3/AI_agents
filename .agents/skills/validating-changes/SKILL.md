---
name: validating-changes
description: Validate a completed task branch without changing files, by running the complete test suite and linting every file changed on the branch. Use for a `full-validation` phase. Do not fix findings.
---

# Validating Changes

Validate the whole task branch read-only and report every failure to the caller.

## Scope

The scope is every file changed on the task branch: the files that differ between the working
tree and the merge base with `{Default_Branch}`, plus untracked files, excluding deleted files.
For example:

```bash
git diff --name-only --diff-filter=d "$(git merge-base {Default_Branch} HEAD)"
git ls-files --others --exclude-standard
```

Use only read-only Git commands.

## Steps

1. Run the complete test suite with the project's test command from `{Agents_file}` when it
   defines one; otherwise run the tests as the applicable language or framework testing profile
   defines. Run the suite in the execution environment declared by the implementation plan,
   when it declares one.
2. Lint each in-scope file with the linting skill. Skip files that have no lint profile.

## Rules

- Do not edit any file, apply lint fixes, or fix findings; only the test suite's own outputs may
  be written.
- If a required placeholder or the test command cannot be resolved, stop and report it instead
  of guessing.

## Report

Report the exact commands, the suite result, the lint result of each in-scope file, the skipped
files, and the file of every failure.

## Profiles

- Implementation plans of analysis methods documents in `{Analysis_Methods_Folder}`: also load
  the [analysis validation rules](analysis.md), which take precedence where they are more
  specific.
