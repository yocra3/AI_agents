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
  `run-analysis.sh` run, and image checks of tier-4 images. An image check runs only when its
  image is built, in `tester: image-check` and `coder: image-build`, and stays in the repository
  as the record of the image's requirements, used to diagnose a later failure of the image; no
  other phase and no mode of `run-tests.sh` runs it.
- Container images in four tiers: the project registry, BioContainers, Seqera Containers and a
  recipe that `coder` builds in Setup, with `tester: image-check` and `coder: image-build`. When
  the Tech Stack declares a language version, such as `R 4.4`, an image of tiers 1 to 3 qualifies
  only with that version of the language, and a tier-4 image is built on it. The plan gives a
  tier-4 image only its requirements, with no base image and no versions except those that the
  methods document fixes, and its Software rows say `pending image-build`. The image check
  requires every package and the fixed versions. `building-container-images` chooses
  the base image of the ecosystem from its reference `base-images.md`, such as `rocker/r-ver`
  with a dated Posit Package Manager snapshot, `bioconductor/bioconductor_docker`, `python` or
  `mambaorg/micromamba`, at its latest stable release, pinned by tag and digest; resolves the
  latest stable package versions with the native package manager, never development, pre-release
  or floating ones; pins them in the recipe; and records the installed versions in the registry
  entry. It stops when a fixed version cannot be installed. When the image check fails after the
  build, `coder: image-build` is retried like a failed GREEN: the retry removes the uncommitted
  entry and image file of the failed attempt and builds again under the same ID; a committed
  entry is never changed, and a rebuilt image gets a new ID. `engineer: software-versions` then
  fills the pending versions and effective parameters from that entry, and a replanning that adds
  a tier-4 image, also by re-resolving an image, resets it.
- Project keys `Analysis_Recipes_Folder`, `Analysis_Images_Folder` and the container execution
  rules in the `AGENTS.md` template.
- The Tech Stack of the `AGENTS.md` template declares, per language, with its version when the
  project requires one, the test framework, the linter and the recommended packages for support
  tasks, and one output format for the project's R Markdown reports, with the rule to name any
  other package in the implementation plan; its free text keeps only the technologies without a
  language line, such as Apptainer or Docker, or a database. Nextflow has its own language line,
  such as `Nextflow 25.04`, whose toolchain and version `linting`, `testing-unit` and
  `writing-code` use.
  `project-bootstrap` proposes the blueprint's defaults, which the user accepts, edits or
  declines: R testthat, lintr with styler, and individual tidyverse packages, readxl, arrow,
  ggplot2, patchwork, scales, ggrepel, future and furrr;
  Python pytest, ruff, pandas, numpy, pyarrow, matplotlib and seaborn; Bash bats and shellcheck;
  Nextflow nf-test, and `nextflow lint` with the nf-core tools lint of the project's own
  components; reports `BiocStyle::html_document` with knitr, DT and kableExtra. `linting` and
  `testing-unit` use the declared linter and test framework, otherwise those of their profiles;
  `selecting-container-images` requires the declared test framework and linter in each image, and
  it and `planning-analysis` stop when a language has none; `planning-analysis` declares the
  support packages of each image starting from the declared packages, with the package of the
  report format in every report's image; and `writing-code` renders reports in the declared
  format, otherwise `html_document`, always self-contained.
- Project key `Nextflow_Reference_Folder` for Nextflow projects, by default
  `{Project_Folder}/reference-data/<spec-slug-id>/`, read by `planning-specs`, which stops
  without it only when a new component needs a reference implementation, and `writing-code`:
  the reference generation and validation scripts go in its versioned `scripts/`, instead of
  `{Specs_Folder}/<spec-slug-id>.reference/` or, as `planning-specs` said,
  `{Plans_Folder}/<spec-slug-id>.reference/`; the generated inputs, outputs and manifests go in
  its `results/`, ignored by Git.
- The phase reference, `.agents/references/phases/` (`common.md`, `specs.md`, `nextflow.md` and
  `analysis.md`): one entry per phase of the implementation plans and per delegation that is not
  a plan marker, with its meaning, skill, steps, evidence and stops. `planning-specs` and
  `planning-analysis` read it, and delegates receive their entry verbatim.
- Skill `agent-delegation` for `implementation-coordinator`: what each delegate's brief holds,
  the evidence required back, retries and failure routing, with `full-validation` failures fixed
  as `<agent>: validation-fix` by the agent whose phase changed the file, `cleaner` for the files
  that a refactoring phase changed last. A test that `coder` reports as invalid, or whose RED
  does not reproduce, goes back to `tester`'s phase, and becomes a stop only when `tester`
  confirms it valid, with a valid RED when it did not reproduce.
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
- Repository-only files, not installed in projects: `docs/programming-workflow.md` and
  `docs/analysis-workflow.md`, the detailed workflow documentation; `docs/catalog.md`, the
  generated catalog of agents, skills, templates, and references; `eval/README.md`, the design of
  an evaluation kit, not yet implemented; and `AGENTS.md`, with `CLAUDE.md` importing it, the
  instructions for agents that work on this repository.

### Changed

- `builder` is renamed `implementation-coordinator` and coordinates specifications and methods
  documents. It runs the phases that the implementation plan declares, Finalization included,
  and manages only the statuses; on a `Verified` or `Released` contract it does nothing. On
  resume at `Coded` without the user's approval, it first runs the phases before Finalization
  that a replanning left pending, keeping `Coded`, then the pending Finalization phases, and
  repeats `coder: full-validation` and `reviewer: implementation-review` only when a phase before
  them was pending, instead of always repeating them.
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
  of the tier-4 images it builds, and each entry gets a `Source` field; its Contents record the
  versions installed in the image. Each image also provides the support packages, those that no
  methods step names, that the implementation plan declares for its increments or the input
  checks, in Software rows with `Effective parameters` `none`; a replanning re-resolves an image
  only on the user's request, for a methods change, or when implementation shows that the image
  fails, such as for a missing support package, as a new image with a new ID, to which move only
  the Software and effective parameters rows of the increments and input checks for which it is
  re-resolved. The old image keeps its other rows, its Images row and its Setup pair while
  anything still uses it; when nothing does, the plan drops its Images row and Setup pair, and a
  Removed entry with only `tester: remove-tests` deletes its image check; its registry entry
  stays.
- `implementation-coordinator` validates a `Draft` contract on the current branch and creates the
  task branch only when validation reports no blocking findings, just before the approval commit,
  `docs(<spec-slug-id>): approve specification` or `docs(<analysis-id>): approve methods vN`.
  `start-task` keeps all of a contract's work on its task branch: when that branch is already
  active, pending changes that belong to the contract and its implementation plan, such as
  Blockers entries, no longer block; unrelated pending changes still do.
- `implementation-coordinator` commits the implementation plan after planning, with the
  `Planned` status and any ER model, as `docs(<spec-slug-id>): plan specification` or
  `docs(<analysis-id>): plan methods vN`, and the plan after each replanning, as
  `docs(<spec-slug-id>): replan specification` or `docs(<analysis-id>): replan methods vN`. In
  analysis Setup it commits after `coder: renumber`, each `tester: image-check` and
  `coder: image-build` pair, `engineer: software-versions`, the `tester: test-setup` and
  `coder: test-setup` pair, `coder: real-config` and `tester: real-input-check`, instead of once
  for the whole section; a phase that ends in RED is never committed alone.
- `commit-changes` follows Conventional Commits 1.0.0: blank lines between header, body and
  footers; the types `feat`, `fix`, `test`, `perf`, `refactor`, `style`, `docs`, `build`, `ci`,
  `chore` and `revert`, each with its meaning; as scope, the contract identifier for every commit
  of a contract and otherwise the area that changes; a header of at most 72 characters, ideally
  about 50, and a body wrapped at 72; and a `BREAKING CHANGE:` footer, besides `!`, that says
  what an upgrader must do. `releasing-version` also counts that footer as a major change.
- In specification plans, each step's Execution is a checkbox list of phase markers, the only
  progress record, instead of a free-form `agent:phase` sequence: `tester: test`,
  `coder: implementation` and `cleaner: refactor` by default, `coder: direct-implementation` for
  a step that no test can observe, and for Nextflow `coder: import-nf-core` for an import and
  `tester: reference-validation` and `coder: reference-generation` before the default phases of a
  component with reference outputs. The default phases replace `tester: production-test`,
  `coder: production-implementation` and `cleaner: production-refactor`, and Nextflow rules are
  added to their briefs in such a step, and to the briefs of `<agent>: validation-fix` in a plan
  with such a step. The Nextflow profile of `testing-unit` runs every nf-test with `--ci`, never
  `--update-snapshot`, in every step, not only in a step with reference outputs; only such a step
  has snapshots, derived from its reference outputs, and the nf-tests of other steps state their
  expectations as explicit assertions.
- `planning-specs` plans Nextflow per specification, not per project: a specification that changes
  no Nextflow code gets no Nextflow planning; one that changes only wiring, channels, configuration,
  parameters or the internals of existing components gets the default phases, without a component
  search or a reference implementation, and its plan's Component design classifies an internal
  change to an existing local component as `modify-local`; and one that needs new processing uses
  `nfcore-component-reuse` only for that processing, with a reference implementation for each new
  component that requires reference outputs. `generating-specs` loads its Nextflow profile when the
  specified behavior will be implemented with Nextflow or nf-core.
- Specification plans also get a Removed section, with `tester: remove-tests` and
  `coder: remove-code`, and a Finalization section with `coder: full-validation` and
  `reviewer: implementation-review`. Tasks are plain bullets, the specification flow says "step"
  throughout, and each acceptance criterion maps to exactly one step, the one whose tests verify
  it.
- The Blockers section of the implementation plans belongs to `implementation-coordinator`, which
  records each stop there and clears resolved entries on resume.
- Analysis `synthetic` increments use the same `tester: test` and `coder: implementation` phases
  as specification steps, and the analysis Finalization review is
  `reviewer: implementation-review`, with the `reviewing-implementation` skill. Its analysis
  rules block costly, inferential or model-based computation in a report that the report's entry
  in Reports does not list, and a statistical test or model in a computation script that no
  methods step states; a descriptive table, file or figure that the methods document does not ask
  for and that changes no required result is non-blocking, with the recommendation to remove it
  or add it to Results to report, either in a revision of the current `Version` or in a new
  `Version`, as the user decides.
- The Nextflow reference implementation profile of `writing-code` applies to the
  `coder: reference-generation` phase.
- Skill profiles keep only conventions: their phase procedures, such as the Phases sections of the
  `analysis.md` profiles of `writing-code` and `testing-unit`, and the phase sections and the
  snapshot order of the Nextflow testing profile, move to the phase reference. `testing-unit` holds
  the only general definition of valid RED, and phase entries add only their own cases.
- Only the `linting` skill lints, in the steps of the phases that write or change code or tests,
  and each of those phases returns its lint results; `writing-code`, `documenting-code` and
  `importing-nf-core` no longer lint on their own. Where each analysis file is linted, which the
  `analysis.md` profiles of `writing-code`, `documenting-code` and `validating-changes` each
  stated, is now only in the analysis profile of `linting`. `linting` adds `nextflow lint` for
  Nextflow scripts and configuration, and the Python docstring check that `documenting-code`
  ran, only when a task adds or changes docstrings.
- `writing-code` and `documenting-code` no longer run tests. `documenting-code` runs only
  documentation checks, such as the documentation build, doctests or `R CMD check --no-tests`,
  and only outside an implementation plan, whose phase instructions decide the checks.
- Imported nf-core components are never linted, when imported, by a later phase, or by
  `coder: full-validation`: a component in nf-core is assumed to have passed nf-core lint.
  `importing-nf-core` checks instead that `modules.json` records the pinned SHA, and
  `nf-core modules lint` and `nf-core subworkflows lint` lint only the project's own components.
  Agents never edit an imported component: an error traced to one, such as a failing test, stops
  the workflow, and the user decides how to resolve it, such as with another version or a patch.
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
  outputs), `synthetic [NN]` (the full run from scratch, with the setup tests and the input
  checks), `setup` (the setup tests only), `post-run` and `input-check`. An
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
- The `AGENTS.md` template holds only the content of `AGENTS.md`: every `Analysis_*` key,
  `Analysis_Methods_Folder` included, is in its Analysis layout section, its Analysis workflow
  section only says which agents run as main sessions and to validate with `reviewer` before
  authorizing. The blueprint holds the values and defaults, and `project-bootstrap` decides when
  to include each section and key.
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
  its phase entry and that `agent-delegation` does not route to a retry or to replanning; the
  phase entry holds the phase-specific stops, such as a failed `tester: real-input-check` or
  missing image-build permissions. `product-owner`, `analyst` and `architect` leave to their
  skills the procedures that the skills state, such as one specification per work item, and keep
  a clarification gate that asks the skill's questions with AskUserQuestion and waits for the
  answers. The topics of those questions are in the skills: `generating-prd` also asks about
  priorities, constraints and success criteria, and `generating-add` about boundaries, data
  ownership, interfaces and operations.
- Each agent's Skills section lists every skill it may use, and in Codex every other skill is
  disabled for it: `reviewer`, for example, can use only `validating-contracts` and
  `reviewing-implementation`. `project-bootstrap`, `push-changes` and `merging-default` belong to
  no agent and run only in the main session. Claude Code subagents cannot restrict skills, so
  there the Skills section is the only restriction. `dev-ops` makes the local release commit of
  an authorized release with `commit-changes`, as `releasing-version` now states.
- Models follow three profiles: `high` (`gpt-6-sol`, `claude-opus-5-5`) for `analyst`,
  `architect`, `craftsman`, `data-analyst`, `engineer`, `implementation-coordinator`,
  `product-owner` and `reviewer`; `medium` (`gpt-6-sol`, `claude-sonnet-5-5`) for `coder`,
  `tester` and `cleaner`; and `low` (`gpt-6-luna`, `claude-haiku-5-5`) for `dev-ops`. The only
  model that changes is `cleaner`'s in Codex, from `gpt-6-luna` to `gpt-6-sol`; efforts are
  unchanged.
- Agent names are hyphenated in every text, such as `implementation-coordinator`, and the analysis
  Finalization marker is `dev-ops: code-documentation`. The generated Codex agents keep the
  underscore form in their `name` field.
- `README.md` keeps the rules common to both workflows and, for each workflow, a summary and a
  simplified figure of the steps that the user sees; the detailed workflow documentation and
  figures move to `docs/`. Its new Requirements section lists
  the framework's external tools, who uses each, when it is needed and what happens without it.
- Skill `coding-spec` is renamed `writing-code`, with the same conventions, and its folder
  `nextflow_guidelines/` is renamed `nextflow-guidelines/`. `planning-specs/test_data.md` is
  renamed `test-data.md`.
- Shared templates live in `.agents/references/templates/`: `agents.template.md` and
  `container-images.template.md` move there from `.agents/templates/`, which is removed, and
  `spec.template.md` from `generating-specs`, now with the limits of at most 3 user stories and
  9 acceptance criteria that `generating-specs` and `validating-contracts` apply; the new
  `analysis-methods.template.md` is there too.
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
- `CLAUDE_CODE_SUBAGENT_MODEL`, and its `env` block, from `.claude/settings.json`: every
  generated Claude Code agent sets its own model. The file keeps its `permissions.deny` rules.
- `default_subagent_model` and `default_subagent_reasoning_effort` from `.codex/config.toml`:
  every generated Codex agent sets its own model and reasoning effort. The file keeps `[agents]`
  with `enabled` and `max_concurrent_threads_per_session`.
- `.agents/CODEX.md`; its content is in `README.md`, `docs/`, and the generated catalog.
- From the `AGENTS.md` template: the base analysis folder keys `Analysis_Scripts_Folder`,
  `Analysis_Tests_Folder`, `Analysis_Reports_Folder`, `Analysis_Results_Folder`,
  `Analysis_Figures_Folder` and `Analysis_Test_Data_Folder`, which no skill or agent reads and
  which the blueprint keeps only to compose the Analysis layout defaults; `Custom_Agents_Folder`;
  the `feat`, `fix` and `chore` prefixes, which `start-task` and `commit-changes` define; and the
  line "Replace template values with verified project information."

### Upgrade notes

- `builder` is now `implementation-coordinator`; in Claude Code, launch it with
  `claude --agent implementation-coordinator`. `analysis-coordinator` is removed: methods
  documents also go through `implementation-coordinator`.
- Write new analyses as methods documents with `data-analyst`; `engineer` derives their
  implementation plans. The analysis plans of 0.9.0 are not migrated.
- Rerun `project-bootstrap` to refresh `AGENTS.md`, or edit it by hand, and update `CLAUDE.md` by
  hand: their analysis keys and agent names changed. `AGENTS.md` now needs the recipes and images
  folders and the container execution rules; in the Tech Stack, one line per language with its test
  framework, linter and recommended packages, and a Reports line with the R Markdown output format
  and packages, with the languages removed from its free text; and, in a Nextflow project, a
  Nextflow line in the Tech Stack, which gives the toolchain and version that `testing-unit`,
  `linting` and `writing-code` use, and `Nextflow_Reference_Folder`, which `planning-specs` requires
  when a new component needs a reference implementation. It no longer needs the base analysis folder
  keys or `Custom_Agents_Folder`. Without a declared test framework and linter for a language,
  `planning-analysis` and `selecting-container-images` stop; without a report format, reports keep
  `html_document`. Every text now uses the hyphenated agent names, so `CLAUDE.md` no longer needs to
  map `product_owner` to `product-owner`, nor the model equivalence between Codex and Claude Code.
  Ignore the built images folder in Git, and consider denying Claude Code's `Read` tool on the data
  folders in `.claude/settings.json`.
- In a Nextflow project, move each reference implementation's versioned scripts from
  `{Specs_Folder}/<spec-slug-id>.reference/` or `{Plans_Folder}/<spec-slug-id>.reference/` to
  `scripts/` of `Nextflow_Reference_Folder`, and its generated data from
  `{Project_Folder}/reference-data/<spec-slug-id>/` to `results/`, or regenerate it there. Ignore
  only the `results/` folders in Git, and update the paths that implementation plans cite.
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
  Likewise, an existing `.claude/settings.json` is never replaced and keeps
  `CLAUDE_CODE_SUBAGENT_MODEL`, which applies only to subagents without a `model` of their own,
  not to the generated agents; you may remove it.
- The installer deletes the files of the removed agents, `builder` and `analysis-coordinator`,
  of the analysis plan template, of the `validating-changes` and `coding-spec` skills, of
  `.claude/scripts/generate_agents.py` and `.agents/CODEX.md`, and the old copies of the moved
  templates, EARS guide and research sources and of the renamed `planning-specs/test_data.md`,
  unless the project modified them; it then keeps them, and you can delete them yourself. In a
  project installed without a manifest, it deletes none of them and lists only those that Git
  tracks in `.agents/skills`, `.agents/templates`, `.codex/agents`, `.claude/agents` and
  `.claude/scripts`.

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
