---
name: testing-unit
description: Write, run, and interpret tests for one component or behavior using TDD. Use the applicable framework profile; do not use for live-service contracts or full-system validation.
---

# Unit Testing

Resolve `{Root_Folder}` and any test folders or commands from global project instructions.
Load the applicable bundled profiles before choosing syntax or commands.

## Bundled profiles

- Test each language with the test framework that the Tech Stack of `{Agents_file}` declares for
  it, and load its profile: [R and R Markdown](references/R.md), [Python](references/python.md),
  and [Bash](references/bash.md). When the Tech Stack declares no test framework for a language,
  use the one of its profile; run a declared framework that has no profile here with its
  documented commands.
- Nextflow implementation plans and their reference implementations: also
  [Nextflow component testing](references/nextflow.md); for nf-core module or subworkflow
  nf-tests, also [module testing](references/nf-core/testing_modules.md) or
  [subworkflow testing](references/nf-core/testing_subworkflows.md).
- Implementation plans of analysis methods documents: additionally the
  [analysis testing rules](analysis.md), which take precedence over the language profiles and
  this skill's general guidance where they differ.

## TDD evidence

Run the relevant existing tests and record the baseline; if none exist, report that instead of
claiming a green baseline. Create or extend the smallest focused test and run it. RED is valid
only when the failure demonstrates missing behavior: a missing required production symbol may be
valid RED; invalid syntax, fixtures, environment, or setup are not.

Keep tests deterministic, independent, and focused on observable behavior. For ordinary unit
tests, isolate network, database, filesystem, time, and process boundaries with suitable test
doubles unless the framework profile requires real execution to verify the component.
Choose reference outputs, property assertions, or both according to
the contract; expected behavior must be independent of the implementation under test.
Report the command, result, covered behavior, and any unresolved failure.
