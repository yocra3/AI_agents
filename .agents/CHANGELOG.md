# Changelog

This file records the changes to the agent definitions of this repository (agents, skills,
templates and the installer) and the upgrade notes for installed projects. `install.py` copies it
into each project with `.agents/VERSION`. It is not the project's own changelog: projects keep
theirs at `{Root_Folder}/CHANGELOG.md`.

Versions follow semantic versioning. The installed version is in `.agents/VERSION`.

## Unreleased

Restructuring of the analysis workflow: an analysis is approved as a readable methods document,
and one implementation workflow executes specifications and methods documents alike.

### Added

- `implementation_coordinator` delegates contract validation to `reviewer` after the user's
  authorization and before the approval commit; a contract with blocking findings stays at
  `Draft`. `reviewer` can also validate a contract as a main session, which is recommended before
  authorizing.
- The analysis methods template, `analysis-methods.template.md`, and the input data reference,
  `.agents/references/analysis-inputs.md`, with fixed fields, a closed vocabulary and
  completeness criteria.
- Skills `defining-analysis-inputs`, `validating-contracts`, `planning-analysis`,
  `building-container-images` and `reviewing-implementation`.
- Synthetic test data from a versioned generator, reference subsets of the real resources, input
  checks that also run on the real inputs (`tester: real-input-check`) and at the start of every
  `run-analysis.sh` run, and permanent checks of tier-4 images.
- Container images in four tiers: the project registry, BioContainers, Seqera Containers and a
  recipe that `coder` builds in Setup.
- Project keys `Analysis_Recipes_Folder`, `Analysis_Images_Folder` and the container execution
  rules in the `AGENTS.md` template.
- Specification implementation plans get a phase catalog, as analysis plans have:
  `tester: test`, `coder: implementation` and `cleaner: refactor` by default,
  `coder: direct-implementation` for a step that no test can observe, and the Nextflow phases,
  with `coder: import-nf-core` for imports. `testing-unit` and `coding-spec` define the
  `remove-tests` and `remove-code` phases for specifications.
- `planning-specs` records the specification's approval commit in the plan header, stops when the
  specification has none or differs from it in anything other than `Status`, and replans from the
  diff since that commit: it resets the markers of affected steps and of Finalization, appends new
  steps, and adds Removed entries for removed steps or criteria.
- A Blockers section in both implementation plan templates, owned by
  `implementation_coordinator`, which records each stop there and clears resolved entries on
  resume.
- A Programming workflow section in the `AGENTS.md` template.
- The phase reference, `.agents/references/phases/` (`common.md`, `specs.md`, `nextflow.md` and
  `analysis.md`): one entry per phase of the implementation plans and per delegation that is not
  a plan marker, with its meaning, skill, steps, evidence and stops.
  `planning-specs` and `planning-analysis` read it, and delegates receive their entry verbatim.
- Skill `agent-delegation` for `implementation_coordinator`: what each delegate's brief holds,
  the evidence required back, retries and failure routing, with `full-validation` failures fixed
  as `<agent>: validation-fix`.
- Analysis Setup phases `coder: test-setup`, after `tester: test-setup`, and
  `engineer: software-versions`, after the last tier-4 image pair.

### Changed

- `builder` is renamed `implementation_coordinator` and coordinates specifications and methods
  documents. It runs the phases that the implementation plan declares, Finalization included,
  and manages only the statuses.
- Analysis plans become two documents: a methods document with the scientific decisions, written
  by `data_analyst` with the user, and an implementation plan in `{Plans_Folder}`, written by
  `engineer`, with the increments, images, seeds, outputs and acceptance criteria.
- A methods document records its changes in a version control table; changes to how results are
  computed need a new `Version`, which only the user sets.
- Both contracts use the statuses `Draft`, `Approved`, `Planned`, `Coded`, `Verified` and
  `Released`. An analysis reaches `Verified` after the user's implementation review, full run
  and `post-run` checks, and `releasing-version` also releases methods documents.
- `selecting-container-images` moves from `data_analyst` to `engineer`.
- `implementation_coordinator` validates a `Draft` contract on the current branch and creates the
  task branch only when validation reports no blocking findings, just before the approval commit.
- `implementation_coordinator` commits the implementation plan after planning, with the
  `Planned` status and any ER model, as `docs(<spec-slug-id>): plan specification` or
  `docs(<analysis-id>): plan methods vN`, and commits Setup after `coder: renumber`, each image
  pair, `tester: test-setup`, `coder: real-config` and `tester: real-input-check` instead of once
  for the whole section.
- In specification plans, each step's Execution is a checkbox list of phase markers, the only
  progress record, and its tasks are plain bullets. The specification flow says "step" throughout,
  and each acceptance criterion maps to exactly one step, the one whose tests verify it.
- `validating-contracts` and `engineer` identify a contract by its folder,
  `{Analysis_Methods_Folder}` or `{Specs_Folder}`, instead of its file name.
- The Nextflow reference implementation profile applies to the `coder: reference-generation`
  phase.
- Skill profiles keep only conventions: the phase procedures of `coding-spec`, `testing-unit` and
  `documenting-code`, with their Phases, Final refactoring and Removal sections, move to the phase
  reference. The implementation plan templates lose their Phases tables and keep their ordering
  and structure rules. `testing-unit` holds the only general definition of valid RED, and phase
  entries add only their own cases.
- Test support code moves from `tester` to `coder`. `tester` writes only tests and their static
  data; in Setup, `tester: test-setup` writes the setup tests of the reference subset script, the
  synthetic data generator, the input checks and the test configuration in RED, and
  `coder: test-setup` writes them and the execution runner, and creates the test inputs, to GREEN.
  Once GREEN, they are frozen: only a Setup phase changes them, and a `full-validation` failure
  in them is fixed only when it is a lint finding, without changing behavior; a functional
  failure goes to replanning, which resets `tester: test-setup` and `coder: test-setup`, and
  also `tester: real-input-check` when the change affects the input checks.
- The analysis execution runner is `run-tests.sh` in `{Analysis_Test_Code_Folder}`, with the
  modes `increment <NN>` (one increment's scripts and checks, reusing the earlier increments'
  outputs), `synthetic [NN]` (the full run from scratch, with the image checks, the setup tests
  and the input checks), `setup` (the setup tests only), `post-run` and `input-check`. An
  increment's RED and GREEN use `increment <NN>`, and `synthetic <NN>` locates a failure; only
  `cleaner: analysis-refactor` and `coder: full-validation` use the full run.
- Unified phase names: analysis `synthetic` increments use `tester: test` and
  `coder: implementation`, and the Nextflow steps with reference outputs use `tester: test`,
  `coder: implementation` and `cleaner: refactor`, with Nextflow rules added to their entries.
  They replace `tester: synthetic-test`, `coder: synthetic-implementation`,
  `tester: production-test`, `coder: production-implementation` and `cleaner: production-refactor`.
- `full-validation` becomes the `coder: full-validation` phase instead of a skill. Criterion: a
  skill holds substantial knowledge of its own, is used by several phases or agents, or makes
  sense outside a plan; a procedure that only chains other skills inside the coordinator's flow is
  a phase.
- Renamed project keys: `Analysis_Plans_Folder` to `Analysis_Methods_Folder`,
  `Analysis_Plan_file` to `Analysis_Methods_file` (`<analysis-id>.methods.md`) and
  `Analysis_Test_Subset_Folder` to `Analysis_Test_Inputs_Folder`. The `subset` verification mode
  and phases become `synthetic`, and `PLAN_VERSION` and the provenance row `plan_version` become
  `ANALYSIS_VERSION` and `analysis_version`.

### Removed

- `analysis_coordinator`; its work moves to `implementation_coordinator` and the phases of the
  implementation plan.
- The analysis plan template, `analysis-plan.template.md`.
- Skill `validating-changes`; its rules are the `coder: full-validation` phase.

### Upgrade notes

- `builder` is now `implementation_coordinator`; in Claude Code, launch it with
  `claude --agent implementation-coordinator`. `analysis_coordinator` is removed: methods
  documents also go through `implementation_coordinator`.
- Write new analyses as methods documents with `data_analyst`; `engineer` derives their
  implementation plans. No existing analysis plan is migrated.
- Rerun `project-bootstrap` to refresh `AGENTS.md`, and update `CLAUDE.md` by hand: their
  analysis keys and agent names changed, and `AGENTS.md` now needs the recipes and images folders,
  the container execution rules and the Programming workflow section. Ignore the built images
  folder in Git, and consider denying Claude Code's `Read` tool on the data folders in
  `.claude/settings.json`.
- Existing specification plans do not follow the new format. Before resuming one with
  `implementation_coordinator`, update it by hand: add the `Approval commit` header with the
  specification's last approval commit, turn each step's Execution into checkbox markers with the
  phase names of the catalog, marking `[x]` the phases already done, turn its task checkboxes into
  plain bullets, and add an empty Removed section and a Blockers section with `None.`.
- Existing analysis implementation plans: add `coder: test-setup` after `tester: test-setup` in
  Setup, marked `[x]` when `tester: test-setup` is complete, and, when the plan has tier-4 images,
  `engineer: software-versions` after the last image pair, marked `[x]`.
- Existing implementation plans with the old marker names: rename `tester: synthetic-test` and
  `coder: synthetic-implementation` to `tester: test` and `coder: implementation` in analysis
  plans, and `tester: production-test`, `coder: production-implementation` and
  `cleaner: production-refactor` to `tester: test`, `coder: implementation` and
  `cleaner: refactor` in specification plans, keeping each checkbox as it is.
- An analysis whose test support code has no `run-tests.sh` with the new modes: before resuming
  it, reset `tester: test-setup` and `coder: test-setup` to pending in its implementation plan.
- The installer deletes the files of the removed agents, `builder` and `analysis_coordinator`,
  and of the analysis plan template, unless the project modified them; it then keeps them, and
  you can delete them yourself. A project installed without a manifest only gets them listed.

## 0.9.0 - 2026-11-20

First versioned state: the agent definitions of commit `68f6dfc` plus the version marker.

### Added

- `.agents/VERSION`, the version of the agent definitions, and this changelog.
- `install.py` shows the source and installed versions with their commit hashes, records the
  version in `.agents/.install-manifest.json`, warns when the version being installed is lower
  than the installed one, and always overwrites `.agents/VERSION` in the target.

### Upgrade notes

- No action is needed. Projects installed before this version have a manifest without a version,
  so this install shows no downgrade warning; it records the version for the next one.
