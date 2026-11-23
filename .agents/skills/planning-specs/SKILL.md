---
name: planning-specs
description: Create or update the single implementation plan for an approved specification, with its steps, phases, acceptance-criterion coverage, and Removed and Finalization sections. Use when engineer plans or replans a specification after its approval commit. Do not use for analysis methods documents, unapproved specifications, unscoped ideas, or direct code edits.
---

# Purpose

Turn an approved specification into the implementation plan that `implementation_coordinator`
executes: ordered steps, each with the phases and agents that run it.

# Contract

Resolve `{Agents_Folder}`, `{Specs_Folder}`, and `{Plans_Folder}` from global instructions.
Read:

- the specification, `{Specs_Folder}/<spec-slug-id>.spec.md`;
- the [implementation plan template](plan.template.md), which defines its format and content
  rules;
- the phase reference, `{Agents_Folder}/references/phases/common.md` and `specs.md`, which
  defines the phases that the markers name;
- for Nextflow work, also [Nextflow planning](references/nextflow.md),
  [test-data discovery](test_data.md), and `{Agents_Folder}/references/phases/nextflow.md`.

Plan only an approved specification. Find its last approval commit with read-only Git commands,
and stop when there is none or when the specification differs from it in anything other than
`Status`:

```bash
git log -1 --format='%H %s' --fixed-strings --grep='docs(<spec-slug-id>): approve specification' -- <path>
git diff <commit> -- <path>
```

The implementation plan is `{Plans_Folder}/<spec-slug-id>.plan.md`. Resolve an existing plan by
its specification identifier or path; update a single existing one in place and preserve its
path, create it when none exists, and stop when several candidates exist.

# Workflow

## 1. Choose the mode

- **New plan**: no implementation plan exists.
- **Replanning**: the implementation plan exists; apply the rules below.

Write the last approval commit in the implementation plan's header; in replanning, only after
taking the diff below.

## 2. Design the implementation

Understand the specification's requirements, consider the repository's conventions and existing
interfaces, and choose the simplest viable approach.

## 3. Decompose it in steps

Break the implementation down into 3 to 9 ordered steps, each a logical unit of work, with its
tasks and Execution markers as the template defines them.

## 4. Map the acceptance criteria

Map each acceptance criterion to the step whose tests verify it, with its verification.

## 5. Write the execution sections

Write Removed, the Execution markers of each step, and Finalization, as the template defines
them, with the Finalization phases pending. In replanning, apply the rules below.

## 6. Check

Before returning, confirm that:

- every rule of the template holds, and every user story, solution item, and acceptance
  criterion is covered;
- every field that an applicable framework profile requires is present and resolved for the
  complete implementation plan;
- the approval commit is the last one.

Leave the specification's `Status` unchanged; the caller owns lifecycle transitions.

# Replanning

Replan from the diff between the approval commit in the implementation plan's header and the
current specification, `git diff <that commit> -- <path>`. Replanning for implementation
evidence, with no specification change, follows the same rules.

- Map each changed user story, solution item, and acceptance criterion to the steps that
  implement or verify it, and propagate the change, directly or transitively through
  `Depends on`, to every step whose tasks, phases, components, test data, or verification must
  change. Update the Acceptance criteria coverage rows of every changed, added, and removed
  criterion.
- Reset to pending the Execution markers of every modified step and every Finalization marker.
  Unchanged steps keep their markers.
- New steps go after the last step, with the next number, and may depend only on earlier steps.
  Completed steps are never renumbered.
- For each removed step or acceptance criterion whose code or tests exist, add a Removed entry
  with its files and pending removal markers. Remove a removed step from Steps.
- Delete Removed entries whose markers are complete.

# Stop conditions

Stop and report to the caller, citing the specification section, user story, or criterion, or
the implementation plan step, without editing the specification or choosing for it, when:

- the specification has no approval commit or differs from it in anything other than `Status`;
- several implementation plans match the specification, or an existing one has no
  `Approval commit` in its header;
- a required placeholder, input artifact, or framework-profile field cannot be resolved.

# Output

Return the specification identifier, the implementation plan path, whether it was created or
updated, the mode and approval commit, the markers reset and Removed entries added, and any stop
with its cited section.
