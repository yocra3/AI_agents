# Analysis workflow

How an analysis methods document becomes tested analysis code that the user runs on the real
data. The rules common to both workflows are in the [README](../README.md#workflows); the phases
are defined in [`.agents/references/phases/`](../.agents/references/phases/).

## Sequence

1. `data-analyst` writes the methods document with the user, as a main session, and leaves it at
   `Draft`. It proposes each decision and explains it in plain language, and can search the
   [ToolUniverse](https://github.com/mims-harvard/ToolUniverse) catalog when the project declares
   `ToolUniverse_CLI` in `AGENTS.md`.
2. Recommended: the user validates it by running `reviewer` as the main session, and revises it
   with `data-analyst` until no blocking finding remains.
3. The user explicitly authorizes `implementation-coordinator` to execute the named methods
   document. The coordinator delegates `reviewer: contract-validation` on the current branch.
   With blocking findings, the document stays at `Draft`, no branch is created, and the findings
   go back to the user. Without them, the coordinator creates the task branch and commits the
   approval, `docs(<analysis-id>): approve methods vN`.
4. `engineer: planning` writes the single implementation plan with planning-analysis, which also
   selects the container images. The coordinator checks that the plan's `Version` equals the
   document's and commits it, `docs(<analysis-id>): plan methods vN`.
5. The coordinator runs the plan's phases in order: Removed, Setup, the increments in `NN` order,
   and Finalization, committing each one when it is green.
6. When every phase before Finalization is complete, the document is `Coded`. Finalization
   refactors the code, writes `run-analysis.sh`, runs a full validation and an implementation
   review, and adds comments.
7. The user reviews the implementation, runs the full analysis on the real data, and runs the
   `post-run` checks. With all three, the document is `Verified`.
8. On request, `dev-ops` releases a version, which sets `Released`.

The figure of this sequence is in the [README](../README.md#analysis-workflow).

## Documents

- The methods document, `{Analysis_Methods_file}` in `{Analysis_Methods_Folder}`, holds the
  scientific decisions and reads like the methods section of a paper: the question, the design,
  one short paragraph per methods step with its tool as `package::function` and every
  non-default value, the results to report, the input data, the global parameters, the
  references, and a version control table. `data-analyst` owns it.
- Input data follows `.agents/references/analysis-inputs.md`: fixed fields and a closed
  vocabulary. The user writes it, or `defining-analysis-inputs` helps by interview or, with
  explicit authorization for each path, by exploring the structure of the data. Only summaries of
  that structure reach the agent's context, never data values.
- The implementation plan, `{Plans_Folder}/<analysis-id>.plan.md`, holds the engineering
  decisions: the Software and effective parameters table, the images, the configuration, the
  input checks, the synthetic data and reference subset rules, the seeds, the increments, the
  reports, the expected outputs, and formal acceptance criteria. `engineer` stops and reports a
  scientific gap in the methods document instead of filling it.
- Paths come from the Analysis layout of the project's `AGENTS.md`, and the coding and testing
  conventions from the `analysis.md` profiles of writing-code and testing-unit.

## Phases

The coordinator delegates every phase with agent-delegation: the phase's entry, pasted verbatim
from the phase reference, follows the rules for every phase of analysis plans and is followed by
the analysis rules of that phase, when it has them.

| Section | Phases | Purpose |
| --- | --- | --- |
| Removed | `tester: remove-tests`, `coder: remove-code` | At a new version, remove the tests and files of a removed increment. |
| Setup | `coder: renumber` | At a new version that renumbers increments, rename their files. |
| Setup | `tester: image-check`, `coder: image-build`, per tier-4 image | A permanent image check in RED, then the recipe, the build, and the registry entry. |
| Setup | `engineer: software-versions` | After the last image pair, fill the versions and effective parameters of the tier-4 software. |
| Setup | `tester: test-setup`, `coder: test-setup` | The setup tests in RED, then the test support code and the test inputs to GREEN. |
| Setup | `coder: real-config`, `tester: real-input-check` | The real configuration, then the input checks on the real inputs. |
| Increments, `synthetic` | `tester: test`, `coder: implementation` | Formal output checks in RED, then the increment's script on the test inputs to GREEN. |
| Increments, `post-run` | `tester: post-run-checks`, `coder: post-run-implementation` | Checks that run only after the user's full run, then the script, validated with lint and syntax checks only. |
| Finalization | `cleaner: analysis-refactor`, `coder: run-script`, `coder: full-validation`, `reviewer: implementation-review`, `dev-ops: code-documentation` | Refactor all analysis code once, write `run-analysis.sh`, run the full validation, review read-only, and add comments. |

The delegations that are not plan markers, the retries, and the stops follow the
[programming workflow](programming-workflow.md#phases). A `full-validation` failure goes, as
`<agent>: validation-fix`, to `tester` for tests and image checks, to `cleaner` for a file that
`cleaner: analysis-refactor` changed, and to `coder` for any other file.

The coordinator commits each Removed entry, each increment, and each Finalization phase. In Setup
it commits `coder: renumber`, `engineer: software-versions`, `coder: real-config`, and
`tester: real-input-check` each on its own, and each RED and GREEN pair together: each
`tester: image-check` with its `coder: image-build`, and `tester: test-setup` with
`coder: test-setup`, so a phase that ends in RED is never committed alone.

## Test data and test support code

Agents never compute on the real data.

- Every script runs, inside its increment's image, on synthetic data with the format of the real
  data, made by a versioned generator with planted signal, and on deterministic subsets of the
  real reference resources.
- The test support code is the test configuration, the execution runner `run-tests.sh`, the
  reference subset script, the synthetic data generator, and the input checks. `tester` writes
  only tests and their static data; in Setup it writes the setup tests of that code in RED, and
  `coder` then writes the code and creates the test inputs until GREEN. Once GREEN, the code is
  frozen: only a Setup phase changes it. A lint finding in it may be fixed without changing its
  behavior; any other change, or a functional failure, goes to `engineer: replanning`, which
  resets both `test-setup` phases, and `tester: real-input-check` when the input checks change.
- On the real data, agents run only the input checks, which report failures without values.
- The same code runs on the test and real data, through two configuration files.
- Tests check form, not results: files, formats, columns, row counts relative to an input,
  provenance files, report sections, and reproducibility. They never check statistics or other
  values.

`run-tests.sh`, in `{Analysis_Test_Code_Folder}`, runs on the host and starts each script and
check in its image:

| Mode | What it runs | Used by |
| --- | --- | --- |
| `increment <NN>` | Increment `NN`'s scripts and checks, reusing the earlier increments' outputs. | RED and GREEN of `tester: test` and `coder: implementation`. |
| `synthetic [NN]` | The full run from scratch: image checks, setup tests, input checks, then every `synthetic` increment with its checks, up to `NN` when given. | `cleaner: analysis-refactor`, `coder: full-validation`, and `synthetic <NN>` to locate an `increment <NN>` failure. |
| `setup` | Only the setup tests. | `coder: test-setup`. |
| `input-check` | Only the input checks, on the real inputs. | `tester: real-input-check`. |
| `post-run` | Only the output checks, on the outputs of the user's full run. | The user, after the full run. |

## Container images

- Images come, in this order, from the project registry (`{Analysis_Images_file}`),
  BioContainers, Seqera Containers, or a recipe (tier 4). `engineer` selects them while planning,
  with selecting-container-images; without the Wave CLI, Seqera Containers images go to tier 4.
- `coder` builds each tier-4 image in Setup, after `tester` writes its permanent image check, and
  adds its registry entry. `engineer: software-versions` then fills the plan's versions and
  effective parameters of the tier-4 software from the registry.
- Recipes are versioned in `{Analysis_Recipes_Folder}`; built images are not.

## Versions and revisions

- The user sets the document's `Version`; agents only suggest a new one. The implementation plan
  keeps the same `Version`.
- A change after an approval reopens the document at `Draft`, through `data-analyst`, and needs a
  new authorization, validation, and approval commit. Each content change adds a row to the
  cumulative version control table, whose approved rows never change.
- Within a version, only new steps at the end whose output no existing step uses, changes to the
  results to report, references, and wording fit. A change to how results are computed, such as
  removing or modifying a methods step, a global parameter that a step uses, Design, or Input
  data, needs a new `Version`; `engineer` stops and suggests one when a same-version diff needs
  it.
- `engineer` replans from the diff since the approval commit. Within a version it only appends
  increments. At a new version it moves removed increments to Removed, renumbers the increments
  from `01` (`coder: renumber` renames their files), and resets the markers of every modified
  increment, of Finalization, and of the Setup phases that the change affects.
- Every version runs again from the start into new, empty output folders named after it (`vN`);
  no output of another version is reused.

## The user's full run

- `run-analysis.sh [FROM [TO]]` runs on the host with the real configuration. On every run it
  first checks that the images it needs are available and runs the input checks; then it runs
  every computation and render script in the range, `post-run` increments included, in `NN`
  order, each in its image. Without arguments it runs everything; `FROM` and `TO` are inclusive
  `NN` bounds.
- Its outputs go to the version folders of the Analysis layout.
- After the full run, the user runs `run-tests.sh post-run`; the coordinator reports these
  pending checks and their commands.
- Agents never interpret results or draft conclusions; reports state only what each table or
  figure shows.

## Status ownership

| Transition | Owner | When |
| --- | --- | --- |
| new → `Draft` | `data-analyst` | The methods document is written. |
| `Draft` → `Approved` | `implementation-coordinator` | After the user's authorization and a contract validation without blocking findings, in the approval commit. |
| `Approved` → `Planned` | `engineer` | After planning; the coordinator commits it with the plan. |
| `Planned` → `Coded` | `implementation-coordinator` | Every phase before Finalization is complete. |
| `Coded` → `Verified` | `implementation-coordinator` | The user approves the implementation review, after the full run and green `post-run` checks. |
| `Verified` → `Released` | `dev-ops` | During a requested release that includes the document. |
| any → `Draft` | `data-analyst` | A revision after an approval. |

`reviewer` never changes a status, and no transition can be skipped.
