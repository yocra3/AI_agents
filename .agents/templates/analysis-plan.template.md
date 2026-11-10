# Analysis plan template

Use this template for `{Analysis_Plans_Folder}/<analysis-id>.md`, where `<analysis-id>` is
`analysis-<slug>`. `data_analyst` owns the content; `analysis_coordinator` may change only the
tracking markers and `Status`. Write acceptance criteria with the
[EARS format guide](../skills/generating-specs/EARS.md).

```markdown
# Analysis plan: <short title>

- **ID**: `analysis-<slug>`
- **Version**: `v1`
- **Status**: Draft
- **Container image**: `<immutable image URI with digest or pinned version tag>`

Allowed status flow: Draft -> Approved -> Coded -> Verified. A revision after approval reopens this file at Draft.

## Scientific question

<The question the user wants to answer. Do not state an expected answer.>

## Input data

| Input | Config key | Path | Format | Expected structure |
| --- | --- | --- | --- | --- |
| `<name>` | `INPUT_<NAME>` | `<exact path>` | `<format and compression>` | `<fields or columns with types, identifiers, relationships to other inputs>` |

## Methodology

### M1: <step title>

- **Tool**: `<package::function, or tool and subcommand>`
- **Inputs**: `<inputs or upstream outputs>`
- **Key parameters**: `<name = value, including any value that differs from the tool default>`
- **Filters**: `<rule and threshold, or none>`
- **Model and covariates**: `<design or formula, or not-applicable>`
- **Multiple-testing correction**: `<method and scope, or not-applicable>`
- **Seed**: `<integer, or not-applicable>`

## Removed

<!-- One entry per removed increment; leave this section empty in a new plan. -->

### Removed: `<old file>`, `<old file>`

- [ ] `tester: remove-tests`
- [ ] `coder: remove-code`

## Setup

- [x] `coder: renumber`
- [ ] `tester: test-setup`
- [ ] `coder: real-config`

## Increments

### Increment 1: <title>

- **Kind**: `<computation | report>`
- **Language**: `<R | R Markdown | Python | Bash>`
- **Verification**: `<subset | post-run>`
- **Files**: `{Analysis_Scripts_Folder}/<analysis-id>/<NN>-<slug>.<ext>`
- **Methodology**: `<M1, M2>`
- **Depends on**: `<increment numbers or none>`
- **Acceptance criteria**: `<AC1, AC2>`

- [ ] `tester: subset-test`
- [ ] `coder: subset-implementation`

## Finalization

- [ ] `cleaner: analysis-refactor`
- [ ] `reviewer: plan-fidelity-review`
- [ ] `dev_ops: code-documentation`

## Expected outputs

| Output | Increment | Folder | File name | Format | Columns and types | Rows |
| --- | --- | --- | --- | --- | --- | --- |
| `<name>` | `<n>` | `<RESULTS_DIR, FIGURES_DIR, or REPORTS_DIR>` | `<file>` | `<format>` | `<name: type, ...> or not-applicable` | `<relative to an input, e.g. one per sample in the samplesheet> or not-applicable` |

## Acceptance criteria

| ID | Criterion | Increment |
| --- | --- | --- |
| AC1 | `<EARS criterion>` | `<n>` |

## Test subset

- **Location**: `{Analysis_Test_Data_Folder}/<analysis-id>/`
- **Rule**: `<deterministic rule deriving the subset from the inputs, with seed if sampled>`
- **Justification**: `<why every subset increment produces meaningful output on it>`

## Changes since the last approval

| Item | Change | Description | Tasks |
| --- | --- | --- | --- |
| `<increment, method step, output, or criterion>` | `<added | modified | removed>` | `<what changed>` | `<phases to run>` |
```

## Authoring rules

- The plan is the only source of analytical decisions. A delegate must be able to execute it
  without choosing methods, parameters, paths, or criteria.
- When a methodology produces a figure, state only what the figure must show, never the plot
  type, library, or styling.
- The container image must provide every tool used by the methodology plus, for each declared
  language, its test framework and linters, and Pandoc when the plan has reports.
- Each increment produces one computation script or one report. A report increment's files are
  its source, `{Analysis_Reports_Folder}/<analysis-id>/<NN>-<slug>.Rmd`, and its render script,
  `{Analysis_Scripts_Folder}/<analysis-id>/<NN>-<slug>.<ext>`, with the same `NN` and slug.
- `NN` in a file name is the increment number, two digits zero-padded (`01`, `02`, ...), and also
  the execution order: the user runs the scripts in `NN` order. An increment may depend only on
  earlier increments.
- Use `subset` unless a step cannot run on a subset, for example an external tool that needs full
  references or large resources. A `subset` increment must not depend on a `post-run` increment;
  declare such a dependent increment `post-run` as well.
- Setup phases, in order: `coder: renumber`, then `tester: test-setup`, then `coder: real-config`.
  The `coder: renumber` marker is complete except at a new version in which some increment number
  changes.
- Phases per increment:
  - `subset`: `tester: subset-test`, then `coder: subset-implementation`.
  - `post-run`: `tester: post-run-checks`, then `coder: post-run-implementation`.
- The Removed section holds one entry per removed increment, with the phases `tester: remove-tests`
  then `coder: remove-code`, and is empty when no increment has been removed. The section order
  Removed, Setup, Increments, Finalization is the execution order.
- Acceptance criteria are formal only: file existence, format, column names and types, row counts
  relative to an input, successful execution, provenance, seed reproducibility on the test
  subset, report rendering, and required report sections. Name outputs by their configuration
  folder, for example `RESULTS_DIR/de-results.tsv`. Never depend on analysis results, such as a
  number of significant genes, or on subset sizes, such as a fixed number of rows.
- Every acceptance criterion maps to exactly one increment, and every increment has at least one.
- Report increments list their required section headings in an acceptance criterion. A report
  increment MAY be assigned methodology steps for figures drawn inline in the report and for
  simple, cheap analyses of files in `RESULTS_DIR` and `FIGURES_DIR`. Assign costly computations
  and every definitive figure, saved in `FIGURES_DIR`, to computation increments. Reports never
  interpret, conclude, or discuss.
- Versioned folders are `vN`, the plan version: `{Analysis_Results_Folder}/<analysis-id>/vN/`,
  `{Analysis_Figures_Folder}/<analysis-id>/vN/`, and `{Analysis_Reports_Folder}/<analysis-id>/vN/`.

## Versions and revisions

- The user manages `Version`. Agents never change it on their own; a new version is the user's
  decision, typically for a change of input data or methodology. `data_analyst` may point out that
  a change looks like it warrants one.
- Edit a never-approved `Draft` in place without change markers.
- Revise an approved plan in place; do not rewrite it. Set `Status` to `Draft`.
- Mark every changed item in place with `[added]`, `[modified]`, or `[removed]`, and list it in the
  changes table. Delete markers and table rows whose tasks are complete. Removed items whose
  removal tasks are complete may be deleted.
- On every revision, reset to pending the markers of the modified increments and of every
  Finalization phase. Also reset `tester: test-setup` and `coder: real-config` when the input
  data, the subset rule, or the version changes, and `coder: renumber` when a new version changes
  any increment number. Unmodified increments keep their markers, including renumbered ones; at a
  new version their tests run again on the regenerated subset.
- Within a version, never renumber increments; append new increments at the end. An increment that
  must run before an existing one, or a new dependency of an increment on a later one, is a
  methodology change and requires a new version.
- When the user sets a new version, renumber the increments consecutively from `01` without gaps,
  so that the numbers again give the execution order. Update the headings, every reference to the
  numbers, such as `Depends on` and the `Increment` columns, and each increment's `Files`.
  Renumbering alone does not make an increment modified; `coder: renumber` renames its files.
- Whether within a version or at a new version, move a removed increment from Increments to the
  Removed section as one entry that lists all its old files, for example
  `Removed: 04-report.Rmd, 04-report.sh`, with its removal phases as pending markers. The entry is
  its `[removed]` marker; list it in the changes table. It takes no number in a new version's
  sequence, so headings never repeat.
- For a new version, every increment runs from the start into empty `vN` folders; never reuse
  outputs of another version.
