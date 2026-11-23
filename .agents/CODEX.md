# Codex Workflow Catalog

## Implementation Flow

Both workflows execute a contract, a specification or an analysis methods document, through
`implementation_coordinator`, a main session. After the user's explicit authorization to execute
the named contract, it delegates contract validation to `reviewer` on the current branch; only a
contract without blocking findings gets a task branch and the approval commit. Then `engineer`
creates the single implementation plan in `{Plans_Folder}`, which the coordinator commits with
the `Planned` status and any ER model. The coordinator runs the phases that the plan declares,
Finalization included, commits each green unit of work that the plan defines, and manages the
contract's status. When it stops, it records the stop in the plan's Blockers.

Before authorizing, the user should validate the contract by running `reviewer` as a main session.
Validation does not approve the contract; the authorization and the approval commit do.

Each work item owns one stable contract, and each contract owns one stable implementation plan.
Revisions update those files in place instead of creating parallel artifacts.

## Delivery Flow

The user-facing sequence is `product_owner` -> a recommended manual validation with `reviewer` ->
the user's explicit authorization to execute the named specification ->
`implementation_coordinator` -> the user's implementation review -> `dev_ops` when release or
code-documentation work is requested.

`engineer` plans the specification with planning-specs and creates the applicable ER model.

## Analysis Flow

The user-facing sequence is `data_analyst` -> a recommended manual validation with `reviewer` ->
the user's explicit authorization to execute the named methods document ->
`implementation_coordinator` -> the user's implementation review, full `run-analysis.sh` run, and
`post-run` checks -> `dev_ops` when release work is requested. `data_analyst` runs as a main
session.

Each analysis owns one methods document, `{Analysis_Methods_file}` in `{Analysis_Methods_Folder}`,
with an `analysis-` identifier, and one implementation plan, `{Plans_Folder}/<analysis-id>.plan.md`.
The user sets the document's `Version`; agents never change it. `engineer` plans the document with
planning-analysis, including its container images, and the implementation plan keeps the
document's `Version`. Agents run the analysis scripts only on synthetic data and reference subsets,
and on the real inputs only the input checks; the user runs the full analysis and interprets the
results.

## Status Ownership

Both contracts follow `Draft` -> `Approved` -> `Planned` -> `Coded` -> `Verified` -> `Released`.

- `product_owner` and `data_analyst`: create or revise the specification or the methods document
  as `Draft`; a revision after approval reopens it at `Draft`.
- Human approval: explicitly authorizes executing the named contract.
- `reviewer`: validates the contract read-only and never changes its status.
- `implementation_coordinator`: records `Approved` in the approval commit, only when contract
  validation reports no blocking findings.
- `engineer`: advances `Approved` to `Planned` after planning.
- `implementation_coordinator`: advances `Planned` to `Coded` when every phase before
  Finalization is complete, runs Finalization, and advances to `Verified` only when the user
  approves the implementation review. For a methods document, that approval also requires the
  user's full run and green `post-run` checks.
- `dev_ops`: advances included `Verified` specifications and methods documents to `Released`
  during a requested release.

## Custom Agents

| Agent | Responsibility |
| --- | --- |
| `analyst` | Research, clarify, and own the project PRD. |
| `architect` | Clarify architecture constraints and own the project ADD. |
| `product_owner` | Maintain one lifecycle specification for a work item. |
| `data_analyst` | Maintain one analysis methods document per analysis with the user. |
| `implementation_coordinator` | Validate, approve, and execute one authorized contract in committed cycles. |
| `engineer` | Prepare the implementation plan of a contract, its images, and applicable data models. |
| `tester` | Establish RED by changing tests and supporting test artifacts only. |
| `coder` | Implement the minimum change for GREEN and build tier-4 images. |
| `cleaner` | Perform behavior-preserving REFACTOR. |
| `reviewer` | Validate contracts before approval and review completed work, read-only. |
| `dev_ops` | Handle requested code documentation and releases. |
| `craftsman` | Maintain Codex agents, skills, prompts, and evaluations. |

## Skills

| Skill | Responsibility |
| --- | --- |
| `$project-bootstrap` | Explicitly create global project instructions, briefing, and changelog. |
| `$generating-prd` | Create or update a Product Requirements Document. |
| `$generating-add` | Create or update an Architecture Design Document for structural changes. |
| `$generating-specs` | Create or update one lifecycle specification for a work item. |
| `$searching-tooluniverse-catalog` | Find candidate analysis methods in the ToolUniverse catalog for `data_analyst`. |
| `$defining-analysis-inputs` | Write the Input data section of a methods document by interview or authorized exploration. |
| `$validating-contracts` | Validate a specification or methods document read-only for `reviewer`. |
| `$planning-specs` | Create or update the single implementation plan for an approved specification. |
| `$planning-analysis` | Create or update the single implementation plan for an approved methods document. |
| `$selecting-container-images` | Select analysis images by tier for `engineer`, through planning-analysis. |
| `$data-modeling` | Model changed persistent entities and relationships. |
| `$nfcore-component-reuse` | Find reusable local and nf-core components before Nextflow planning. |
| `$importing-nf-core` | Import an approved nf-core module or subworkflow with nf-core tools. |
| `$building-container-images` | Write, build, and register a tier-4 image for `coder`. |
| `$coding-spec` | Apply repository and language coding conventions. |
| `$linting` | Run repository lint checks and fix requested findings. |
| `$testing-unit` | Write and run isolated tests. |
| `$reviewing-implementation` | Review completed work read-only against its contract and implementation plan for `reviewer`. |
| `$documenting-code` | Document source APIs and generate documentation artifacts. |
| `$agent-delegation` | Brief each delegate of `implementation_coordinator` with its phase instructions and route its failures. |
| `$start-task` | Prepare a local task branch. |
| `$commit-changes` | Create reviewed local commits. |
| `$push-changes` | Explicitly publish existing commits. |
| `$merging-default` | Explicitly merge a task branch locally. |
| `$releasing-version` | Explicitly prepare version and changelog changes. |

## Templates

| Template | Responsibility |
| --- | --- |
| [`agents.template.md`](templates/agents.template.md) | Base structure used by `craftsman` for Codex custom agents. |
| [`analysis-methods.template.md`](templates/analysis-methods.template.md) | Analysis methods document structure used by `data_analyst`. |
| [`container-images.template.md`](templates/container-images.template.md) | Project container image registry: `engineer` adds tier 2 and 3 entries while planning and `coder` adds tier-4 entries after building. |

## References

| Reference | Responsibility |
| --- | --- |
| [`analysis-inputs.md`](references/analysis-inputs.md) | Fields, formats, vocabulary, and completeness criteria of a methods document's Input data, used by `data_analyst`, defining-analysis-inputs, validating-contracts, planning-analysis, and the analysis coding and testing profiles. |
| [`phases/`](references/phases/) | One entry per phase of the implementation plans and per delegation that is not a plan marker, with its skill, steps, evidence, and stops. Read by planning-specs, planning-analysis, and agent-delegation, which pastes each entry verbatim into the delegate's brief. |
| [`craftsman-sources.md`](references/craftsman-sources.md) | External workflow sources that `craftsman` verifies before proposing adoption. |
