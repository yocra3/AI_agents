# Changelog

Changelog of AI_agents, the agent framework: every change to this repository and the upgrade
notes for the projects that install it. `install.py` copies this file into each project; a
project records its own changes in its root `CHANGELOG.md`, never here.

Versions follow semantic versioning. The installed version is in `.agents/VERSION`.

## Unreleased

Restructuring of the analysis workflow and of agent generation: an analysis is approved as a
readable methods document, one implementation workflow executes specifications and methods
documents alike, and the agents of every environment are generated from neutral sources.

### Added

- `implementation-coordinator` delegates contract validation to `reviewer` after the user's
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
  recipe that `coder` builds in Setup, with `tester: image-check` and `coder: image-build`.
  `engineer: software-versions` then records the versions of the tier-4 software in the plan.
- Project keys `Analysis_Recipes_Folder`, `Analysis_Images_Folder` and the container execution
  rules in the `AGENTS.md` template.
- The phase reference, `.agents/references/phases/` (`common.md`, `specs.md`, `nextflow.md` and
  `analysis.md`): one entry per phase of the implementation plans and per delegation that is not
  a plan marker, with its meaning, skill, steps, evidence and stops. `planning-specs` and
  `planning-analysis` read it, and delegates receive their entry verbatim.
- Skill `agent-delegation` for `implementation-coordinator`: what each delegate's brief holds,
  the evidence required back, retries and failure routing, with `full-validation` failures fixed
  as `<agent>: validation-fix`.
- `planning-specs` records the specification's approval commit in the plan header, stops when the
  specification has none or differs from it in anything other than `Status`, and replans from the
  diff since that commit: it resets the markers of affected steps and of Finalization, appends new
  steps, and adds Removed entries for removed steps or criteria.
- Neutral agent sources, `.agents/agents/<name>.md`, one per agent: the frontmatter holds the
  name, the description, the model profile, the reasoning effort, the skills the agent may use,
  the Codex sandbox and the Claude Code tools, and the body the instructions. The generator
  `.agents/scripts/generate_agents.py` writes `.claude/agents/*.md`, `.codex/agents/*.toml`, and
  `docs/catalog.md` from them; `--check` lists out-of-date files. It rejects a source whose
  `skills` differ from the skills its Skills section names, or whose profile is unknown.
- Configuration file `.agents/config/model-profiles.md`: the Codex and Claude Code model of each
  profile, `high`, `medium` and `low`. It replaces the model equivalence of `README.md`. The
  generated catalog shows each agent's profile and skills.
- Reference `.agents/references/framework-principles.md` and skill `maintaining-framework`, which
  `craftsman` follows for every framework change.
- `install.py` warns when the Wave CLI is not on `PATH`, and when the ToolUniverse CLI is neither
  on `PATH` nor an executable at the target's declared `ToolUniverse_CLI`.
- Repository-only files, not installed in projects: `docs/programming-workflow.md` and
  `docs/analysis-workflow.md`, the detailed workflow documentation; `docs/catalog.md`, the
  generated catalog of agents, skills, templates, and references; `eval/README.md`, the design of
  an evaluation kit, not yet implemented; and `AGENTS.md`, with `CLAUDE.md` importing it, the
  instructions for agents that work on this repository.

### Changed

- `builder` is renamed `implementation-coordinator` and coordinates specifications and methods
  documents. It runs the phases that the implementation plan declares, Finalization included,
  and manages only the statuses.
- Analysis plans become two documents: a methods document with the scientific decisions, written
  by `data-analyst` with the user, and an implementation plan in `{Plans_Folder}`, written by
  `engineer` with `planning-analysis`, with the images, test data rules, seeds, increments,
  outputs and acceptance criteria.
- A methods document records its changes in a version control table; changes to how results are
  computed need a new `Version`, which only the user sets.
- Both contracts use the statuses `Draft`, `Approved`, `Planned`, `Coded`, `Verified` and
  `Released`. An analysis reaches `Verified` after the user's implementation review, full run
  and `post-run` checks, and `releasing-version` also releases methods documents.
- `engineer` selects the container images while planning, with `selecting-container-images`,
  instead of `data-analyst`. It adds the registry entries of the images it selects, `coder` those
  of the tier-4 images it builds, and each entry gets a `Source` field.
- `implementation-coordinator` validates a `Draft` contract on the current branch and creates the
  task branch only when validation reports no blocking findings, just before the approval commit,
  `docs(<spec-slug-id>): approve specification` or `docs(<analysis-id>): approve methods vN`.
- `implementation-coordinator` commits the implementation plan after planning, with the
  `Planned` status and any ER model, as `docs(<spec-slug-id>): plan specification` or
  `docs(<analysis-id>): plan methods vN`. In analysis Setup it commits after `coder: renumber`,
  each `tester: image-check` and `coder: image-build` pair, `engineer: software-versions`, the
  `tester: test-setup` and `coder: test-setup` pair, `coder: real-config` and
  `tester: real-input-check`, instead of once for the whole section; a phase that ends in RED is
  never committed alone.
- In specification plans, each step's Execution is a checkbox list of phase markers, the only
  progress record, instead of a free-form `agent:phase` sequence: `tester: test`,
  `coder: implementation` and `cleaner: refactor` by default, `coder: direct-implementation` for
  a step that no test can observe, and for Nextflow `coder: import-nf-core` for an import and
  `tester: reference-validation` and `coder: reference-generation` before the default phases of a
  component with reference outputs. The default phases replace `tester: production-test`,
  `coder: production-implementation` and `cleaner: production-refactor`, and Nextflow rules are
  added to their briefs in such a step.
- Specification plans also get a Removed section, with `tester: remove-tests` and
  `coder: remove-code`, and a Finalization section with `coder: full-validation` and
  `reviewer: implementation-review`. Tasks are plain bullets, the specification flow says "step"
  throughout, and each acceptance criterion maps to exactly one step, the one whose tests verify
  it.
- The Blockers section of the implementation plans belongs to `implementation-coordinator`, which
  records each stop there and clears resolved entries on resume.
- Analysis `synthetic` increments use the same `tester: test` and `coder: implementation` phases
  as specification steps, and the analysis Finalization review is
  `reviewer: implementation-review`, with the `reviewing-implementation` skill.
- The Nextflow reference implementation profile of `writing-code` applies to the
  `coder: reference-generation` phase.
- Skill profiles keep only conventions: their phase procedures, such as the Phases sections of the
  `analysis.md` profiles of `writing-code` and `testing-unit` and the phase sections of the
  Nextflow testing profile, move to the phase reference. `testing-unit` holds the only general
  definition of valid RED, and phase entries add only their own cases.
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
- `full-validation` becomes the `coder: full-validation` phase instead of a skill. Criterion: a
  skill holds substantial knowledge of its own, is used by several phases or agents, or makes
  sense outside a plan; a procedure that only chains other skills inside the coordinator's flow is
  a phase.
- Renamed project keys: `Analysis_Plans_Folder` to `Analysis_Methods_Folder`,
  `Analysis_Plan_file` to `Analysis_Methods_file` (`<analysis-id>.methods.md`) and
  `Analysis_Test_Subset_Folder` to `Analysis_Test_Inputs_Folder`. The `subset` verification mode
  becomes `synthetic`, and `PLAN_VERSION` and the provenance row `plan_version` become
  `ANALYSIS_VERSION` and `analysis_version`.
- `.codex/agents` is no longer the source of the agents: the Codex and Claude Code agents are
  both generated from the neutral sources.
- `craftsman` is neutral between environments: it uses the skill-creator skill and the official
  documentation of each environment instead of Codex-only skills, and edits the neutral sources
  with `maintaining-framework`, which replaces its procedure for keeping `.claude/agents` in sync.
  It no longer suggests prompt optimizers as research aids; sending repository content to
  external services, installing packages, or adopting external prompts or skills still requires
  an explicit user request and a review of provenance and fit.
- Every agent follows the common structure of the agent template, `agents.template.md`: Role,
  Goal, Skills, the agent's own sections, Boundaries, and Output, with tools only in the
  frontmatter. Agents no longer describe phase procedures: `tester`, `coder`, `cleaner`, and
  `engineer`, `reviewer` and `dev-ops` when delegated, follow the phase instructions of the
  delegation and return the evidence they request, and the descriptions of `tester` and `cleaner`
  no longer name phases. Only `implementation-coordinator` names markers, for its commit points,
  status and stops; it stops on its own conditions and on any stop that a delegate reports from
  its phase entry, which holds the phase-specific stops, such as a failed
  `tester: real-input-check` or missing image-build permissions.
- Each agent's Skills section lists every skill it may use, and in Codex every other skill is
  disabled for it: `reviewer`, for example, can use only `validating-contracts` and
  `reviewing-implementation`. `project-bootstrap`, `push-changes` and `merging-default` belong to
  no agent and run only in the main session. Claude Code subagents cannot restrict skills, so
  there the Skills section is the only restriction.
- Models follow three profiles: `high` (`gpt-6-sol`, `claude-opus-5-5`) for `analyst`,
  `architect`, `craftsman`, `data-analyst`, `engineer`, `implementation-coordinator`,
  `product-owner` and `reviewer`; `medium` (`gpt-6-sol`, `claude-sonnet-5-5`) for `coder`,
  `tester` and `cleaner`; and `low` (`gpt-6-luna`, `claude-haiku-5-5`) for `dev-ops`. The only
  model that changes is `cleaner`'s in Codex, from `gpt-6-luna` to `gpt-6-sol`; efforts are
  unchanged.
- Agent names are hyphenated in every text, such as `implementation-coordinator`, and the analysis
  Finalization marker is `dev-ops: code-documentation`. The generated Codex agents keep the
  underscore form in their `name` field.
- `README.md` keeps the rules common to both workflows and, for each workflow, a summary and its
  figure; the detailed workflow documentation moves to `docs/`.
- Skill `coding-spec` is renamed `writing-code`, with the same conventions, and its folder
  `nextflow_guidelines/` is renamed `nextflow-guidelines/`.
- Shared templates live in `.agents/references/templates/`: `agents.template.md` and
  `container-images.template.md` move there from `.agents/templates/`, which is removed, and
  `spec.template.md` from `generating-specs`; the new `analysis-methods.template.md` is there too.
  The EARS guide moves from `generating-specs` to `.agents/references/EARS.md`, since
  `validating-contracts` and `planning-analysis` also read it. Material that only one skill uses
  stays in that skill, such as a plan template, and `craftsman`'s research sources,
  `.agents/references/craftsman-sources.md`, move into `maintaining-framework` as
  `references/research-sources.md`.

### Removed

- `analysis-coordinator`; its work moves to `implementation-coordinator` and the phases of the
  implementation plan.
- The analysis plan template, `analysis-plan.template.md`.
- Skill `validating-changes`; its rules are the `coder: full-validation` phase.
- `.claude/scripts/generate_agents.py`, replaced by `.agents/scripts/generate_agents.py`.
- `default_subagent_model` and `default_subagent_reasoning_effort` from `.codex/config.toml`:
  every generated Codex agent sets its own model and reasoning effort. The file keeps `[agents]`
  with `enabled` and `max_concurrent_threads_per_session`.
- `.agents/CODEX.md`; its content is in `README.md`, `docs/`, and the generated catalog.

### Upgrade notes

- `builder` is now `implementation-coordinator`; in Claude Code, launch it with
  `claude --agent implementation-coordinator`. `analysis-coordinator` is removed: methods
  documents also go through `implementation-coordinator`.
- Write new analyses as methods documents with `data-analyst`; `engineer` derives their
  implementation plans. The analysis plans of 0.9.0 are not migrated.
- Rerun `project-bootstrap` to refresh `AGENTS.md`, and update `CLAUDE.md` by hand: their
  analysis keys and agent names changed, and `AGENTS.md` now needs the recipes and images folders
  and the container execution rules. Every text now uses the hyphenated agent names, so
  `CLAUDE.md` no longer needs to map `product_owner` to `product-owner`, nor the model
  equivalence between Codex and Claude Code. Ignore the built images folder in Git, and consider
  denying Claude Code's `Read` tool on the data folders in `.claude/settings.json`.
- Specification plans of 0.9.0 do not follow the new format of
  `.agents/skills/planning-specs/plan.template.md`. Before resuming one with
  `implementation-coordinator`, update it by hand: add the `Approval commit` header with the
  specification's last approval commit; put the steps in a Steps section and turn each step's
  Execution into checkbox markers, marking `[x]` the phases already done, with the phase names
  `tester: test`, `coder: implementation`, `cleaner: refactor`, or `coder: direct-implementation`,
  and for Nextflow `coder: import-nf-core`, `tester: reference-validation`, and
  `coder: reference-generation`, where `tester: production-test`,
  `coder: production-implementation`, and `cleaner: production-refactor` become `tester: test`,
  `coder: implementation`, and `cleaner: refactor`; turn its task checkboxes into plain bullets;
  rename the `Plan increment` column of Acceptance criteria coverage to `Step`; add an empty
  Removed section and a Finalization section with unchecked `coder: full-validation` and
  `reviewer: implementation-review`; and write its Blockers in the template's format, or
  `None.`.
- Agents are generated from `.agents/agents/`. If the project changed its installed agents in
  `.codex/agents` or `.claude/agents`, move those changes into the agent's source and regenerate
  both with `python3 .agents/scripts/generate_agents.py`; a changed model goes in
  `.agents/config/model-profiles.md` or the agent's `profile`. The project's own agents,
  without a source, are listed and never changed. A project's own skill in `.agents/skills/` is
  disabled in Codex for every generated agent until a source lists it in `skills`.
- `coding-spec` is now `writing-code`. Replace the old name in the project's own files, such as
  its own agents and skills or `CLAUDE.md`, and move any change the project made to a
  `coding-spec` file, such as a language profile, to the same file in
  `.agents/skills/writing-code/`.
- Shared templates and the EARS guide moved to `.agents/references/`. Replace
  `.agents/templates/`, `generating-specs/spec.template.md` and `generating-specs/EARS.md` in the
  project's own files, and move any change the project made to those files to their new paths.
  Do the same for `.agents/references/craftsman-sources.md`, now
  `.agents/skills/maintaining-framework/references/research-sources.md`.
- The installer never replaces an existing `.codex/config.toml`. Its `default_subagent_model`
  and `default_subagent_reasoning_effort` do not affect the generated agents, which set their own
  model and effort; remove them by hand unless the project wants them for its own subagents.
- The installer deletes the files of the removed agents, `builder` and `analysis-coordinator`,
  of the analysis plan template, of the `validating-changes` and `coding-spec` skills, of
  `.claude/scripts/generate_agents.py` and `.agents/CODEX.md`, and the old copies of the moved
  templates, EARS guide and research sources, unless the project modified them; it then keeps them, and you can
  delete them yourself. A project installed without a manifest only gets them listed.

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
