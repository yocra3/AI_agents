# Codex Workflow Catalog

## Delivery Flow

The user-facing sequence is `product_owner` -> human approval -> `builder` -> `dev_ops` when
release or code-documentation work is requested.

`builder` delegates preparation to `engineer` before TDD. The engineer creates the plan and the
applicable ER model. Specification status ownership follows the same flow:

Each work item owns one stable specification file and that specification owns one stable plan.
Revisions update those files in place instead of creating parallel artifacts.

- `product_owner`: creates or updates the specification as `Draft`.
- Human approval: explicitly authorizes the exact `Draft` revision for builder.
- `builder`: records the approved handoff as `Approved` on its task branch.
- `engineer`: advances `Approved` to `Planned` after planning.
- `builder`: advances `Planned` to `Coded`, then `Verified`, based on implementation and evidence.
- `dev_ops`: advances included `Verified` specifications to `Released` during a release.

## Analysis Flow

The user-facing sequence is `data_analyst` -> human approval of the exact plan path and version
-> `analysis_coordinator` -> the user's full run. `data_analyst` and `analysis_coordinator` run as
main sessions.

Each analysis owns one plan in `{Analysis_Plans_Folder}` with an `analysis-` identifier; revisions
update it in place. The user manages the plan version; agents never change it. Analysis plans are
neither specifications nor implementation plans.

- `data_analyst`: creates or revises the plan as `Draft`.
- Human approval: authorizes the exact plan path and version.
- `analysis_coordinator`: records `Approved` in the approval commit, delegates to `tester`,
  `coder`, `cleaner`, `reviewer`, and `dev_ops`, and advances the plan to `Coded` and `Verified`.
- User: runs the full analysis and the post-run checks, and interprets the results.

## Custom Agents

| Agent | Responsibility |
| --- | --- |
| `analyst` | Research, clarify, and own the project PRD. |
| `architect` | Clarify architecture constraints and own the project ADD. |
| `product_owner` | Maintain one lifecycle specification for a work item. |
| `engineer` | Prepare implementation plans and applicable data models for builder. |
| `builder` | Coordinate committed implementation cycles and perform declared direct imports. |
| `tester` | Establish RED by changing tests only. |
| `coder` | Implement the minimum change for GREEN. |
| `cleaner` | Perform behavior-preserving REFACTOR. |
| `reviewer` | Review completed work read-only against its approved specification and plan. |
| `dev_ops` | Handle requested code documentation and releases. |
| `craftsman` | Maintain Codex agents, skills, prompts, and evaluations. |
| `data_analyst` | Maintain one analysis plan per analysis. |
| `analysis_coordinator` | Coordinate committed execution of one approved analysis plan version. |

## Skills

| Skill | Responsibility |
| --- | --- |
| `$project-bootstrap` | Explicitly create global project instructions, briefing, and changelog. |
| `$generating-prd` | Create or update a Product Requirements Document. |
| `$generating-add` | Create or update an Architecture Design Document for structural changes. |
| `$generating-specs` | Create or update one lifecycle specification for a work item. |
| `$planning-specs` | Create or update the single plan for an approved specification. |
| `$data-modeling` | Model changed persistent entities and relationships. |
| `$nfcore-component-reuse` | Find reusable local and nf-core components before Nextflow planning. |
| `$importing-nf-core` | Import an approved nf-core module or subworkflow with nf-core tools. |
| `$coding-spec` | Apply repository and language coding conventions. |
| `$linting` | Run repository lint checks and fix requested findings. |
| `$testing-unit` | Write and run isolated tests. |
| `$documenting-code` | Document source APIs and generate documentation artifacts. |
| `$start-task` | Prepare a local task branch. |
| `$commit-changes` | Create reviewed local commits. |
| `$push-changes` | Explicitly publish existing commits. |
| `$merging-default` | Explicitly merge a task branch locally. |
| `$releasing-version` | Explicitly prepare version and changelog changes. |

## Templates

| Template | Responsibility |
| --- | --- |
| [`agents.template.md`](templates/agents.template.md) | Base structure used by `craftsman` for Codex custom agents. |
| [`analysis-plan.template.md`](templates/analysis-plan.template.md) | Analysis plan structure used by `data_analyst`. |
