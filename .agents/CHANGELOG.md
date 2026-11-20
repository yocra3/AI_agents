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
- Renamed project keys: `Analysis_Plans_Folder` to `Analysis_Methods_Folder`,
  `Analysis_Plan_file` to `Analysis_Methods_file` (`<analysis-id>.methods.md`) and
  `Analysis_Test_Subset_Folder` to `Analysis_Test_Inputs_Folder`. The `subset` verification mode
  and phases become `synthetic`, and `PLAN_VERSION` and the provenance row `plan_version` become
  `ANALYSIS_VERSION` and `analysis_version`.

### Removed

- `analysis_coordinator`; its work moves to `implementation_coordinator` and the phases of the
  implementation plan.
- The analysis plan template, `analysis-plan.template.md`.

### Upgrade notes

- `builder` is now `implementation_coordinator`; in Claude Code, launch it with
  `claude --agent implementation-coordinator`. `analysis_coordinator` is removed: methods
  documents also go through `implementation_coordinator`.
- Write new analyses as methods documents with `data_analyst`; `engineer` derives their
  implementation plans. No existing analysis plan is migrated.
- Rerun `project-bootstrap` to refresh `AGENTS.md`, and update `CLAUDE.md` by hand: their
  analysis keys and agent names changed, and `AGENTS.md` now needs the recipes and images folders
  and the container execution rules. Ignore the built images folder in Git, and consider denying
  Claude Code's `Read` tool on the data folders in `.claude/settings.json`.
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
