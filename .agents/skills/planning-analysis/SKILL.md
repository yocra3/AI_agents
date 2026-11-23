---
name: planning-analysis
description: Create or update the single implementation plan for an approved analysis methods document, with its images, test data rules, increments, acceptance criteria, and Setup and Finalization phases. Use when engineer plans or replans a methods document after its approval commit. Do not use for specifications, unapproved documents, or code changes.
---

# Purpose

Turn an approved methods document into the implementation plan that `implementation_coordinator`
executes. Make only engineering decisions: every scientific decision comes from the document, and
when one is missing, stop instead of choosing it.

# Contract

Resolve global placeholders from `{Agents_file}`. Read:

- the methods document, `{Analysis_Methods_file}` with `<analysis-id>` as `analysis-<slug>`;
- `{Agents_Folder}/templates/analysis-methods.template.md` and
  `{Agents_Folder}/references/analysis-inputs.md`, which define how the document is written and
  read, including the omission rules of methods steps;
- the [implementation plan template](plan.template.md), which defines its format and content
  rules;
- the phase reference, `{Agents_Folder}/references/phases/common.md` and `analysis.md`, which
  defines the phases that the markers name;
- `{Analysis_Images_file}`.

Plan only an approved document. Find its last approval commit with read-only Git commands, and
stop when there is none or when the document differs from it in anything other than `Status`:

```bash
git log -1 --format='%H %s' --fixed-strings --grep='docs(<analysis-id>): approve methods v' -- <path>
git diff <commit> -- <path>
```

The implementation plan is `{Plans_Folder}/<analysis-id>.plan.md`. Update a single existing one
in place, create it when none exists, and stop when several candidates exist.

# Workflow

## 1. Choose the mode

- **New plan**: no implementation plan exists.
- **Same-version replanning**: the implementation plan's `Version` equals the document's.
- **New-version replanning**: the document has a new `Version`.

Write the document's `Version` and its last approval commit in the implementation plan's header.

## 2. Read the methods

Read each methods step as its tool, inputs, non-default parameters, filters, model, and
multiple-testing correction, applying the omission rules. Check every step, design comparison,
result to report, and input for the stop conditions below before planning.

## 3. Select software and images

Use selecting-container-images for every increment and for the input checks, with any version
that the document fixes. From its records, fill Images and the Setup image pairs; fill Software
and effective parameters from the resolved versions and their documentation.

## 4. Define inputs and test data

From Input data and Global parameters, write Configuration. Derive the technical requirements
that the steps' functions impose on the inputs, and choose the language and image of the input
checks. Write the synthetic data rules with planted signal, the reference subset rules, and the
seeds.

## 5. Plan increments, reports, outputs, and criteria

Group the methods steps into computation increments in execution order and decide the reports
from Results to report. Choose each increment's verification mode, then write Expected outputs
and formal EARS acceptance criteria, mapping each criterion to one increment.

## 6. Write the execution sections

Write Removed, Setup, the Execution markers of each increment, and Finalization, as the template
defines them. In replanning, apply the rules below.

## 7. Check

Before returning, confirm that:

- every rule of the template holds, and every methods step, input, global parameter, and result
  to report is covered;
- every tier-1 to tier-3 image has its registry entry with its digest;
- `Version` equals the document's and the approval commit is the last one.

Leave the document's `Status` unchanged; the caller owns lifecycle transitions.

# Replanning

Replan from the diff between the approval commit in the implementation plan's header and the
current document, `git diff <that commit> -- <path>`, not from the version control table.
Replanning for implementation evidence, with no document change, follows the same rules.

- Map each changed step, input, global parameter, and result to the items that use it, and
  propagate the change, directly or transitively through `Depends on`, to every increment whose
  methods, inputs, images, outputs, or criteria must change. Unchanged increments keep their
  markers, also when renumbered.
- Keep the resolved versions and the chosen images, also an image that a missing Wave CLI sent
  to tier 4. Re-resolve an image only when the user asks or a methods change requires it; only a
  version that the user fixes in the document updates a version, which may need a new image ID.
- Reset to pending:
  - the Execution markers of every modified increment;
  - every Finalization marker;
  - `tester: test-setup`, `coder: test-setup`, `coder: real-config`, and
    `tester: real-input-check` when Input data, the global parameters, Configuration, the input
    checks, the test data rules, or `Version` change;
  - `tester: test-setup` and `coder: test-setup` when implementation evidence shows that the
    frozen test support code must change or fails functionally, and also
    `tester: real-input-check` when the change affects the input checks;
  - `coder: renumber` when a new version changes some increment number.
  New tier-4 images add new, pending image pairs.
- Within a version, only append: new increments go at the end, with the next `NN`, and no
  increment is removed or renumbered.
- At a new version, move each removed increment from Increments to Removed, as one entry with all
  its old files and pending removal markers. Then renumber the increments consecutively from `01`
  in execution order, and update the headings, `Depends on`, the `Increment` columns, Seeds,
  Reports, and each increment's `Files`. Renumbering alone does not modify an increment;
  `coder: renumber` renames its files.
- Delete Removed entries whose markers are complete.

# Stop conditions

Stop and report to the caller, citing the document section, step, or input key, without editing
the document or choosing for it, when:

- the document leaves open a decision that affects the results, such as a comparison without its
  direction, a filter without its threshold or comparison, a model without its formula, or a
  step that produces p-values without its correction method and scope;
- implementing a step needs a choice that the text does not state and that is not a default
  value, such as which annotation field maps identifiers or how replicates are aggregated;
- within the same `Version`, the diff contains a change that requires a new `Version` under the
  methods template's revision rules, such as a removed or modified step, or a change needs an
  increment inserted before an existing one, such as a new dependency of an increment on a later
  one; suggest a new version, which only the user sets;
- the document has no approval commit or differs from it, several implementation plans match,
  or a package version cannot be provided by any image tier.

For a scientific gap, say in plain language what the document must state, not which value to
choose.

# Output

Return the implementation plan path, whether it was created or updated, the mode, `Version` and
approval commit, the registry entries added, the tier-4 images and their Setup phases, whether
the Wave CLI was missing and which images it sent to tier 4, the markers reset, the Software and
effective parameters table, and any stop with its cited section.
