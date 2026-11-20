# Analysis methods template

Use this template for `{Analysis_Methods_file}`, where `<analysis-id>` is `analysis-<slug>`.
The document reads like the methods section of a paper: the user discusses it with
`data_analyst` and within the group, and `engineer` derives the implementation plan from it.
`data_analyst` owns the content; the implementation workflow changes only `Status`.

```markdown
# Analysis methods: <short title>

- **ID**: `analysis-<slug>`
- **Version**: `v1`
- **Status**: Draft

## Scientific question

<The question the analysis answers, without anticipating the answer.>

## Design

- **Unit of analysis**: <what one observation is, for example one sample>
- **Groups or conditions**: <groups or conditions, and the variable that defines them>
- **Comparisons of interest**: <each comparison with its direction, for example treated vs control>
- **Covariates**: <variables the model adjusts for, or none>

## Methods

**M1: <Step name>.** <Short paragraph with the tool as `package::function` and the required
elements of the step.>

**M2: <Step name>.** <Short paragraph.>

- Parameters:
  - `<parameter> = <value>`

## Results to report

| Result | Type | What it shows | From |
| --- | --- | --- | --- |
| <name> | <table, or figure type such as volcano plot> | <content; for a figure, the variable on each axis, the grouping, and any marked threshold> | <methods step, or simple calculation on a step's results> |

## Input data

<Inputs and their relations, following `{Agents_Folder}/references/analysis-inputs.md`.>

## Global parameters

| Parameter | Value | Used by |
| --- | --- | --- |
| <meaning, with its comparison, for example adjusted p-value strictly below> | <value> | <M2, M3> |

## References

1. <Authors, year, title, journal, DOI; or the documentation URL> (<steps it supports>)

## Version control

| Version | Section or step | Change | Description | Reason |
| --- | --- | --- | --- | --- |
| v1 | Document | added | Initial document | First approval |
```

## Content rules

- The document holds the scientific decisions and nothing else. `engineer` must be able to
  implement every step without choosing anything that the text does not state and that is not a
  default value.
- Never include acceptance criteria, increments, container images, seeds, output files, test
  values, configuration keys other than the input keys, or execution markers; they belong to the
  implementation plan.
- Be precise: name each tool as `package::function`, or as tool and subcommand for a command-line
  tool; give the exact value of every parameter that differs from its default; and state every
  threshold with its comparison (`<`, `<=`, `>`, `>=`).
- Software versions are optional. Cite the method without a version unless the user fixes one,
  and then write it with the tool, for example `DESeq2::DESeq` (DESeq2 1.42.0). Otherwise
  `engineer` resolves the version when planning. Revising the document never updates a version;
  the user updates one only by fixing it here, with its row in the version control table.
- Never anticipate results or state expected values.
- Write the document concisely; explanations, alternatives, and their consequences stay in the
  conversation with `data_analyst`.

## Methods steps

- Each step is a short paragraph that starts with its ID and name in bold, `**M1: <name>.**`,
  numbered `M1`, `M2`, ... in the order the steps run. A step with many parameters may add a
  brief `Parameters` list below its paragraph.
- Omission rules:
  - A parameter that is not mentioned uses its default value.
  - An input that is not mentioned is the output of the previous step. Name any other input by
    its key, such as `INPUT_COUNTS`, or as the output of a step, such as `the result of M2`.
  - What does not apply is not written.
- Required elements, decided by what the step's functions do rather than by what the paragraph
  says. For example, a step that uses `DESeq2::results` produces p-values even if its paragraph
  does not mention them.

  | When the step | It states |
  | --- | --- |
  | Always | The tool, as `package::function`. |
  | Filters | Each threshold and its comparison. |
  | Fits a model | The formula or design. |
  | Produces p-values | The multiple-testing correction method and its scope, even when it is the default. |
  | Uses non-default values | Each of them, with its exact value. |

- A step that uses a global parameter names it instead of repeating its value.

## Results to report

- Describe what to report or explore and, for a figure, its type and what it shows. Never define
  reports, their sections, or file names, and never specify plotting functions, their arguments,
  or styling; `engineer` decides how results are reported.
- Each result comes from a methods step or is a simple calculation: descriptive and deterministic
  on existing results, such as counts, proportions, means, or the first N. Anything inferential or
  model based, such as a statistical test, p-values, a model fit, or clustering, needs a methods
  step.
- Never ask for interpretations or conclusions; the user interprets the results.

## Input data

Follow `{Agents_Folder}/references/analysis-inputs.md` for the fields, formats, vocabulary,
design variables, and completeness criteria. The section may be completed at any time before the
document is authorized.

## Status

Allowed status flow: `Draft -> Approved -> Planned -> Coded -> Verified -> Released`. The document
stays at `Draft` while it is written or revised. The approval commit,
`docs(<analysis-id>): approve methods vN`, records that the user authorized this exact document. A
revision after an approval sets `Status` back to `Draft`.

## Versions and revisions

- The user sets `Version`. Agents never change it on their own; they may only suggest a new one.
- The version control table is cumulative: never delete its rows, and never change a row once it
  has been approved. Rows added since the last approval may be edited until the next approval.
  `Change` is `added`, `modified`, or `removed`; `Section or step` names the section, the step
  ID, or the input key.
- Before the first authorization, `data_analyst` writes the initial row
  `| v1 | Document | added | Initial document | First approval |`. Until the first approval
  commit, the draft is edited freely and the table holds only that row.
- After the first approval, revise the document in place and add one row per content change, with
  the document's current `Version`. Wording corrections that do not change content take no row.
- A change to how results are computed requires a new `Version`: removing a methods step;
  modifying an existing step's tool, parameters, filters, model, or correction; changing a global
  parameter that a step uses; changing Design or Input data; or adding a step whose output an
  existing step uses.
- Only these changes fit within a version: new steps at the end of the execution order whose
  output no existing step uses, changes to Results to report, references, and wording
  corrections. The implementation numbers its scripts in execution order, and the user may
  already have run them for the current version. A new step takes the next unused `M` number,
  and step IDs are never reused or renumbered within a version.
- At a new version, every step runs again from the start into new, empty output folders; no output
  of another version is reused.

## Checks before authorization

Before the user authorizes the document, check that:

- every methods step states the required elements that its functions call for;
- the Input data section meets the completeness criteria of
  `{Agents_Folder}/references/analysis-inputs.md`;
- the version control table has the initial row and, after an approval, one row per content
  change, with every approved row unchanged;
- while `Version` is still the last approved one, every change since that approval fits within a
  version.
