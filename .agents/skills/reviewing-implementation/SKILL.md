---
name: reviewing-implementation
description: Review completed work read-only against its approved contract and implementation plan, and report actionable blocking and non-blocking findings, ending with a verdict. Use for reviewer's implementation review, such as the `implementation-review` phase of an implementation plan, after complete validation. Do not use for contract validation, and never fix findings.
---

# Purpose

Tell the caller whether the completed work implements its approved contract and implementation
plan, and what must change before the user's review. Review the work, not the contract: never
judge whether the contract's scientific or product decisions are appropriate.

# Inputs

Resolve global placeholders from `{Agents_file}`. Read:

- the approved contract, a specification or an analysis methods document;
- its implementation plan, which scopes the review: the steps or increments, their files and
  acceptance criteria, and the software and environment they use;
- the files changed on the task branch, listed with read-only Git commands, and their tests;
- the `full-validation` report, which is the evidence of the test suite and lint results;
- the project and framework profiles that the caller supplies.

Review only after complete validation: when the `full-validation` report is missing or shows a
failure, report it as a blocking finding. Stop and report when the contract or the implementation
plan is missing or cannot be resolved.

# Checks

- **Fidelity**: the work satisfies the contract and every acceptance criterion, and implements
  every implementation plan item as planned.
- **Correctness**: the code does what the contract and the implementation plan state, including
  error handling and edge cases that they name.
- **Regressions**: the changes do not break behavior outside the implementation plan's scope.
- **Tests**: every acceptance criterion has a test that checks it and that would fail if the
  criterion were not met.
- **Scope**: the branch changes nothing that the contract and the implementation plan do not
  authorize.
- **Consistency**: planned and implemented behavior agree, such as names, interfaces, outputs, and
  dependencies.

# Classification

- **Blocking**: the work does not meet the contract or an acceptance criterion, misses or
  deviates from an implementation plan item, is incorrect, causes a regression, leaves a
  criterion without a test that can fail, or changes behavior that the contract does not
  authorize. The work must change before the user's review.
- **Non-blocking**: any other actionable finding, such as maintainability or readability
  problems, tests that could be stronger beyond the criteria, or small additions beyond the
  implementation plan that change no contracted behavior.

A profile below may classify specific cases; its classification takes precedence.

# Profiles

- Implementation plans of analysis methods documents in `{Analysis_Methods_Folder}`: also load
  the [analysis review rules](analysis.md).

# Report

Report only actionable findings. For each, give its location, the supporting evidence, and the
affected contract section or criterion, or implementation plan step, increment, or phase. Use
this structure, writing `None.` under an empty list:

```markdown
# Implementation review: <contract path>

- **Implementation plan**: <path>
- **Evidence**: <full-validation report summary>

## Blocking findings

1. **<file:line>** (<affected contract or implementation plan item>): <finding and evidence>

## Non-blocking findings

1. **<file:line>** (<affected contract or implementation plan item>): <finding and evidence>

Verdict: <blocking findings present | no blocking findings>
```

The verdict is always the last line and uses exactly one of the two values.

# Prohibited

- Editing, creating, or formatting any file, or fixing findings.
- Redesigning working code, or proposing changes to the contract's decisions.
- Changing a contract's `Status` or `Version`, or Git commands that change the repository.
