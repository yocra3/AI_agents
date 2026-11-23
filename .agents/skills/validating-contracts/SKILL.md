---
name: validating-contracts
description: Validate an analysis methods document or a specification read-only and report its blocking and non-blocking findings in plain language, ending with a verdict. Use for reviewer's contract validation, after the user authorizes a contract and before its approval commit, or when the user asks reviewer to validate one. Do not use while a contract is being drafted. Never edits the contract or reads data files.
---

# Purpose

Check that a contract states everything needed to implement it without a decision that it does
not record, and tell the user in plain language what blocks it. Validate the text only: never
judge whether the scientific methods or the product decisions are the right ones, and never
choose a value for the user.

# Contract

Resolve global placeholders from `{Agents_file}`. Validate exactly the one contract named in the
request, identified by its folder:

- a file in `{Analysis_Methods_Folder}`: a methods document. Read
  `{Agents_Folder}/templates/analysis-methods.template.md` and
  `{Agents_Folder}/references/analysis-inputs.md`, which define its format and rules.
- a file in `{Specs_Folder}`: a specification. Read
  `{Agents_Folder}/skills/generating-specs/spec.template.md` and
  `{Agents_Folder}/skills/generating-specs/EARS.md`, which define its format and its criteria.

Stop and report when the path is missing, does not exist, or is in neither folder.

# Classification

- **Blocking**: only the cases this skill marks as blocking. The contract cannot be approved
  until it is revised and authorized again.
- **Non-blocking**: every other departure from the template or its rules. Report it; the
  workflow continues.
- When a departure makes a blocking check impossible to pass, such as a missing Input data or
  Acceptance Criteria section, report it as that blocking check.

# Methods documents

## Step cards

Reconstruct the card of each methods step, in execution order, so the user sees how the methods
were read:

| Field | Content |
| --- | --- |
| Tool | `package::function`, or tool and subcommand |
| Inputs | Input keys and outputs of earlier steps; an input that is not mentioned is the output of the previous step |
| Non-default parameters | Each parameter with its exact value; a global parameter by name, with its value from the Global parameters table |
| Filters | Each threshold with its comparison |
| Model | The formula or design |
| Correction | The multiple-testing method and its scope |

Decide which fields a step requires with the template's required elements, from what its
functions do and not from what the paragraph says. In each field, write the value,
`not applicable` when the step's functions do not call for it, or `missing` when it is required
and not stated. When you cannot establish what a function does, write `unverified` with your
assumption.

- Blocking: each `missing` required element.
- Non-blocking: each `unverified` field, which the user confirms.

## Minimum checks

Each failed check is blocking:

1. Every result in Results to report comes from a methods step or is a simple calculation, as
   the template defines it.
2. Every comparison of interest in Design is performed by a methods step, as stated and in its
   direction.
3. Every step uses defined inputs: each input is an `INPUT_<NAME>` or `REF_<NAME>` key defined
   in Input data, or the output of an earlier step. A first step that names no input has none.
4. Every design variable, meaning the variable that defines the groups, each covariate, and each
   variable of a model formula, is marked as a design variable in Input data, and every level
   that Design or Methods names is one of its levels. Check this against the document only.
5. No value is pending: no `TBD`, `?`, unfilled template placeholder, parameter named without
   its value, or global parameter that a step names and the Global parameters table lacks.
6. No result is anticipated: no expected values, expected directions of effects, or conclusions.
7. Input data meets every completeness criterion of `analysis-inputs.md`. Report each unmet
   criterion with its number and the input key.

## Version control

Find the last approval commit and the changes since it, with read-only Git commands. The diff
compares that commit with the working tree, so it includes uncommitted changes:

```bash
git log -1 --format='%H %s' --fixed-strings --grep='docs(<analysis-id>): approve methods v' -- <path>
git diff <commit> -- <path>
```

With no approval commit, the version control table must hold exactly the template's initial
row. Any other table is blocking.

With an approval commit, check the diff against the table:

- Blocking: a content change to Methods, to a global parameter that a step uses, to Input data,
  or to Results to report that no row records.
- Blocking: while `Version` is still the approved one, a change that requires a new `Version`
  under the template's revision rules, including a new step whose output an existing step uses by
  the omission rule. Explain that the change alters how results are computed, while the user may
  already have run the approved version's scripts, so it needs a new `Version`, which only the
  user sets.
- Blocking: a row of the table at the approval commit that was deleted or changed. Approved rows
  are immutable; rows added since that commit may still be edited.
- Non-blocking: an imprecise row added since the approval, such as a wrong section, change type,
  version, or description; a content change to another section with no row; and, within a
  version, a new step that is not last in execution order or a step ID that was reused or
  renumbered.
- Wording corrections that do not change content need no row and are not findings.

## Template conformance

Report as non-blocking any other departure from the template: missing or misordered sections or
header fields, steps not written as `**M1: <name>.**`, content the template excludes, such as
acceptance criteria, increments, container images, seeds, output files, test values, or
execution markers, and results that define reports, files, or plotting, or ask for
interpretations.

# Specifications

Blocking:

- An acceptance criterion that does not follow the EARS guide, or that is not testable because
  no test could check it, for example one that relies on a vague term such as "quickly".
- A user story that no acceptance criterion covers.
- Acceptance criteria that contradict each other or the Solution Overview.
- A pending value: `TBD`, `?`, or an unfilled template placeholder such as `{...}`.

Non-blocking:

- Implementation details.
- More than 3 user stories or more than 9 acceptance criteria.
- Ambiguous wording that still allows writing the tests.
- Any other departure from the template's header and sections.

# Report

Write for a reader with little experience in bioinformatics or software. For each finding, name
the affected section, step, input key, or criterion; say what is missing or inconsistent and why
it matters for the implementation; and say what the contract must state, not which value to
choose. Use this structure, writing `None.` under an empty list:

```markdown
# Contract validation: <contract path>

- **Contract**: <methods document or specification>, `<ID>`, <Version for a methods document>
- **Compared with**: <approval commit hash and subject, or no previous approval; methods only>

## Step cards

| Step | Tool | Inputs | Non-default parameters | Filters | Model | Correction |
| --- | --- | --- | --- | --- | --- | --- |

## Blocking findings

1. **<Section, step, input key, or criterion>**: <plain-language explanation>

## Non-blocking findings

1. **<Section, step, input key, or criterion>**: <plain-language explanation>

Verdict: <blocking findings present | no blocking findings>
```

Omit Step cards for a specification. The verdict is always the last line and uses exactly one of
the two values. Revisions are not part of validation: `data_analyst` revises methods documents
and `product_owner` revises specifications.

# Prohibited

- Editing, creating, or formatting any file, including the contract, or changing its `Status`
  or `Version`.
- Opening, listing, or running commands on the data paths of Input data or on any other data
  file.
- Git commands that change the repository.
- Judging whether the methods or the product decisions are appropriate, or proposing values.
