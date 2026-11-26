# Specification implementation plan template

Use this template for `{Plans_Folder}/<spec-slug-id>.plan.md`, the single implementation plan of
the specification `{Specs_Folder}/<spec-slug-id>.spec.md`. `engineer` owns the content;
`implementation-coordinator` changes only the execution markers and Blockers.

```markdown
# Implementation plan: <spec-slug-id>

- **Specification**: `<{Specs_Folder}/<spec-slug-id>.spec.md, relative to the repository root>`
- **Approval commit**: `<hash>` `docs(<spec-slug-id>): approve specification`
- **Pipeline root**: `<absolute path or not-applicable>`

## Environment and reproducibility

- **Execution environment**: `<required runtime, profiles, plugins and architecture constraints>`
- **Containers**: `<exact image URI and digest or stable hash for each reference command or new executable component; include Apptainer invocation and bind mounts, or not-applicable>`

## Test data and artifacts

| Boundary | Role | Path or materialization command | Format and semantics | Checksum |
| --- | --- | --- | --- | --- |
| `<boundary>` | <input | companion | prerequisite | reference-output | intermediate | output> | `<path or command>` | `<format, cardinality, metadata associations and tolerances>` | `<checksum, pending-reference-generation, or not-applicable>` |

## Component design

| Component | Classification | Contract and evidence | Source |
| --- | --- | --- | --- |
| `<component>` | `<reuse-local | import-nf-core | new | modify-local | local-wiring>` | `<public interface, channel shape and compatibility evidence>` | `<local path, or nf-core type/name/modules SHA, or not-applicable>` |

## Acceptance criteria coverage

| Acceptance criterion | Step | Verification |
| --- | --- | --- |
| `<criterion identifier>` | `<step number>` | `<test boundary and expected evidence>` |

## Removed

### Removed: <Step n: title, or criterion identifier>: `<file>`, `<file>`

- [ ] `tester: remove-tests`
- [ ] `coder: remove-code`

## Steps

### Step 1: <title>

<short description of the step; for a `coder: direct-implementation` step, why no test can observe it>

- **Depends on**: `<step numbers or none>`
- **Tasks**:
  - <one-line outcome-oriented task>
- **Execution**:
  - [ ] `tester: test`
  - [ ] `coder: implementation`
  - [ ] `cleaner: refactor`

## Finalization

- [ ] `coder: full-validation`
- [ ] `reviewer: implementation-review`

## Blockers

None.
```

## Phases

Every marker names its phase as `<agent>: <phase>`, one of the phases that
`{Agents_Folder}/references/phases/` defines for specification plans: `common.md` for Removed,
Finalization, `tester: test`, and `coder: implementation`, `specs.md` for the other Steps phases,
and `nextflow.md` for the Nextflow-only phases.

## Content rules

- The implementation plan holds the engineering decisions only. Every product decision comes from
  the specification; never add, choose, or change one here.
- Paths may be absolute or relative to the repository root. Write them relative to the repository
  root, and keep a path outside the repository absolute.
- `Approval commit` is the approval commit of the specification that the plan was last planned
  from.
- It has no change markers; its history is in Git.

## Acceptance criteria coverage

- One row per acceptance criterion of the specification. Every criterion maps to exactly one
  step, the one whose tests verify it, with its test boundary and expected evidence.
- A step may have no criterion, such as an intermediate step or a `coder: direct-implementation`
  step.

## Steps

- Steps are numbered from 1 in execution order, and a removed step's number is not reused. A
  step may depend only on earlier steps.
- Tasks are plain bullets, at most five, each an outcome that the delegated agent can verify
  without prescribed implementation tactics. The Execution markers are the only progress record.
- Execution per step:
  - By default: `tester: test`, `coder: implementation`, then `cleaner: refactor`.
  - `coder: direct-implementation` alone, only when the step has no behavior that a test can
    observe, such as configuration or scaffolding. The step's description states why.
  - Nextflow, as [Nextflow planning](references/nextflow.md) assigns them:
    `coder: import-nf-core` alone for an imported nf-core component, and
    `tester: reference-validation` and `coder: reference-generation` before the default phases,
    in the order that Nextflow planning gives, for a new component that requires reference
    outputs. Other Nextflow steps use the default.

## Removed, Finalization, and Blockers

- The section order Removed, Steps, Finalization is the execution order.
- The Removed section holds one entry per removed step or acceptance criterion whose code or tests
  must go, listing its files, with the phases `tester: remove-tests` then `coder: remove-code`,
  and is empty when nothing has been removed. An entry takes no step number.
- Finalization always has the two phases of the template, in that order.
- Blockers belong to `implementation-coordinator`: one entry per stop, written as
  `- **<cited section, criterion, step, or phase>**: <stop condition, as reported>`, or `None.`.
  `engineer` writes `None.` in a new plan and never changes Blockers.
