---
name: agent-delegation
description: Brief a delegate with the instructions of its phase from the phase reference, check the evidence it returns, and route its failures. Use from implementation-coordinator for every delegation of an implementation plan phase, contract validation, planning, or replanning. Do not use to run a phase yourself.
---

# Purpose

Give each delegate the exact instructions of its phase and the context it needs, so that it
decides nothing that the contract, the implementation plan, and the phase reference do not
state, and turn its result into the coordinator's next action: record the phase, retry it, or
stop.

# Phase reference

Resolve `{Agents_Folder}` from `{Agents_file}`. The phase reference is
`{Agents_Folder}/references/phases/`:

- `common.md`: the phases of both plan types and the delegations that are not plan markers:
  `reviewer: contract-validation`, `engineer: planning`, `engineer: replanning`, and
  `<agent>: validation-fix`;
- `specs.md`: the phases that only specification plans use;
- `nextflow.md`: the Nextflow-only phases of specification plans, and the Nextflow rules of some
  other phases;
- `analysis.md`: analysis plans, with the analysis rules of some common phases.

Find each entry by its ID, `<agent>: <phase>`, which a plan marker names without its argument.
Stop and report when no entry matches a marker.

# Brief

Send the delegate, in this order:

1. The contract path and, when it exists, the implementation plan path.
2. What the phase acts on: the step, increment, Removed entry, or plan section, and the marker as
   the plan writes it, with any argument, such as the image ID of `tester: image-check`.
3. The phase instructions, pasted verbatim from the phase reference, never summarized or
   reworded:
   - for a phase of `tester`, `coder`, or `cleaner`, including an `<agent>: validation-fix`, the
     "Rules for every phase" section of `specs.md` or `analysis.md`, by the plan type, then the
     entry, then the phase's rules for its plan type when they exist: its analysis rules in
     `analysis.md` for an analysis plan, or its Nextflow rules in `nextflow.md` for a step that
     has `tester: reference-validation`;
   - for a phase of `engineer`, `reviewer`, or `dev-ops`, including contract validation, planning,
     and replanning, the entry only.
4. The earlier evidence that the entry uses, such as tester's exact command and RED result for
   the coder phase that follows it, tester's image check command for `coder: image-build`, the
   `full-validation` report for `reviewer: implementation-review`, the failures routed for
   `<agent>: validation-fix`, or the evidence that requires `engineer: replanning`.
5. On a retry, the previous attempt's failure, with its commands and messages, and the retry
   number.

Add no instruction that changes what the entry requires. For `reviewer: contract-validation`,
send only the contract path, the request to validate it, and the entry.

# Result

Require back the evidence that the entry lists, with exact commands and results, and each stop
of the entry or any other condition that prevents the phase as written, reported and not
resolved.

- A result without the entry's evidence, or with changes outside the phase's scope, is a failure
  of the phase.
- A reported stop is never retried; return it to the coordinator's stop handling. The exception is
  a stop that only needs a change of the implementation plan, including a change or a functional
  failure of the frozen test support code of an analysis: delegate `engineer: replanning` with
  that evidence, then run the phases that the replanning leaves pending.

# Failure routing

- Retry each phase at most twice. When the retries are exhausted, return the stop to the
  coordinator.
- Route code, lint, and GREEN failures to coder, invalid tests to tester, and failed refactoring
  to cleaner, as a retry of that agent's phase for the same step, increment, or section, with the
  failure.
- Route each `full-validation` failure by file, as `<agent>: validation-fix`: tests, image checks,
  and their static data to tester; a file changed by the analysis plan's `cleaner:
  analysis-refactor` to cleaner; any other file to coder, including a lint finding in the frozen
  test support code of an analysis. A functional failure in that frozen code goes instead to
  `engineer: replanning`, which resets `tester: test-setup` and `coder: test-setup`, and also
  `tester: real-input-check` when the change affects the input checks; run the
  phases that it leaves pending. Then run `coder: full-validation` again.
- Never route a failure in an imported nf-core component to an agent: return it to the
  coordinator as a stop, for the user to decide how to resolve it.
