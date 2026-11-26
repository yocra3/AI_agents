# Global Placeholder Blueprint

Values and defaults of the placeholders of `AGENTS.template.md`. The base analysis folders only
compose the defaults of the Analysis layout keys and are not written to `{Agents_file}`.

## Required

- `{Root_Folder}`: repository root containing product and agent files.
- `{Agents_Folder}`: the agent framework folder: agent sources, skills, references,
  configuration, scripts, and its changelog.
- `{Agents_file}`: global project instructions file.
- `{Project_Folder}`: product requirements and architecture documentation folder.
- `{Briefing_file}`: short product briefing file.
- `{Specs_Folder}`: feature, fix, and maintenance specifications folder.
- `{Plans_Folder}`: implementation plans folder.

## Analysis workflow

Required only when the project uses `data-analyst` and analysis methods documents.

Base folders, resolved inside the layout values below:

- `{Analysis_Scripts_Folder}`: tracked computation scripts, render scripts, shared functions, and
  configurations.
- `{Analysis_Tests_Folder}`: tracked analysis tests, separate from the scripts; test run outputs
  are ignored.
- `{Analysis_Reports_Folder}`: tracked report sources; rendered reports are ignored.
- `{Analysis_Results_Folder}` and `{Analysis_Figures_Folder}`: ignored outputs.
- `{Analysis_Test_Data_Folder}`: ignored test inputs, one folder per analysis, below
  `{Project_Folder}`.

Analysis layout keys, each with its default unless the project confirms another layout. Keep the
pattern variables as written.

- `{Analysis_Methods_Folder}`: no default. It must not be, or be inside, `{Specs_Folder}` or
  `{Plans_Folder}`; implementation plans go in `{Plans_Folder}`.
- `{Analysis_Methods_file}`: `{Analysis_Methods_Folder}/<analysis-id>.methods.md`
- `{Analysis_Images_file}`: `{Project_Folder}/container-images.md`
- `{Analysis_Recipes_Folder}`: no default; tracked recipes of tier-4 container images, shared by
  all analyses.
- `{Analysis_Images_Folder}`: no default; ignored built image files, shared by all analyses.
- `{Analysis_Script_file}`: `{Analysis_Scripts_Folder}/<analysis-id>/<NN>-<slug>.<ext>`
- `{Analysis_Shared_Functions_file}`: `{Analysis_Scripts_Folder}/<analysis-id>/functions.<ext>`
- `{Analysis_Real_Config_file}`: `{Analysis_Scripts_Folder}/<analysis-id>/config/real.conf`
- `{Analysis_Test_Config_file}`: `{Analysis_Scripts_Folder}/<analysis-id>/config/test.conf`
- `{Analysis_Report_Source_file}`: `{Analysis_Reports_Folder}/<analysis-id>/<NN>-<slug>.Rmd`
- `{Analysis_Results_Version_Folder}`: `{Analysis_Results_Folder}/<analysis-id>/vN/`
- `{Analysis_Figures_Version_Folder}`: `{Analysis_Figures_Folder}/<analysis-id>/vN/`
- `{Analysis_Reports_Version_Folder}`: `{Analysis_Reports_Folder}/<analysis-id>/vN/`
- `{Analysis_Test_Code_Folder}`: `{Analysis_Tests_Folder}/<analysis-id>/`
- `{Analysis_Test_Inputs_Folder}`: `{Analysis_Test_Data_Folder}/<analysis-id>/`
- `{Analysis_Test_Run_Folder}`: `{Analysis_Tests_Folder}/<analysis-id>/results/synthetic/`
- `{Analysis_Test_Rerun_Folder}`: `{Analysis_Tests_Folder}/<analysis-id>/results/rerun/`
- `{Analysis_Provenance_file}`: `<RESULTS_DIR>/<NN>-<slug>.provenance.tsv`

Container execution rules, with no defaults:

- `{Container_Engine}`: Apptainer, which builds images with `fakeroot`, or Docker. It runs every
  image, and `building-container-images` writes and builds tier-4 recipes for it.
- `{Container_Run_Rule}`: how to run a command in the image of an `{Analysis_Images_file}` entry,
  from the repository root, with the bind mounts that make the repository and the configured
  input paths visible in it.
- `{Container_Image_Availability}`: what makes an image available on the user's machine, which
  `run-analysis.sh` checks before each run. A tier-4 image is available when its image file exists
  in `{Analysis_Images_Folder}`. For a registry image of tiers 1 to 3, state the project's rule,
  for example an image file pulled from its URI into a cache folder, or a pull by digest when it
  runs.
- `{Container_Build_Permissions}`: that building tier-4 images needs build permissions, Apptainer
  `fakeroot` for the user or access to the Docker daemon, and whether the user has them. Without
  them, `coder` stops at `coder: image-build` and states what to ask the administrator for.

Data access: when the project has an analysis workflow, recommend in the bootstrap report that
the user deny Claude Code's `Read` tool on the folders that hold the real data and reference
resources, in the project's `.claude/settings.json`, with one deny rule per folder the user names,
such as `Read(/data/**)` for a folder below the repository root or `Read(//abs/path/**)` for an
absolute path. Do not write the file. The rule blocks only the file-reading tools; the exploration
rules of `defining-analysis-inputs` still apply to commands.

`{ToolUniverse_CLI}`: path of the ToolUniverse `tu` executable, used by
`searching-tooluniverse-catalog`. No default: only the path the user gives, never a guessed or
derived one.

## Nextflow

`{Nextflow_Reference_Folder}`: reference implementation of a Nextflow component, default
`{Project_Folder}/reference-data/<spec-slug-id>/`. Its `scripts/` holds the versioned generation
and validation scripts, and its `results/` the generated inputs, outputs and manifests, ignored by
Git.

## Tech Stack

One line per language of the Tech Stack, with its toolchain and recommended packages:

- `{Language}`: the language, such as R, Python, Bash, or Nextflow, followed by its version when
  the project requires one, such as `R 4.4`.
- `{Test_Framework}` and `{Linter}`: the toolchain the repository already uses, otherwise the
  default of the language: R testthat, and lintr with styler; Python pytest and ruff; Bash bats
  and shellcheck; Nextflow nf-test, and `nextflow lint` with the nf-core tools lint of the
  project's own components.
- `{Language_Packages}`: suggested by default for R dplyr, tidyr, tibble, purrr, stringr,
  forcats, readr, readxl, arrow, ggplot2, patchwork, scales, ggrepel, future, and furrr, as
  individual packages, not the `tidyverse` meta-package; for Python pandas, numpy, pyarrow,
  matplotlib, and seaborn. No default for other languages.

The Reports line, for a project with R Markdown reports:

- `{Report_Format}`: one output format for every report of the project. Default
  `BiocStyle::html_document`; alternatives `rmdformats::readthedown`, `rmdformats::downcute`,
  `rmdformats::robobook`, `rmdformats::material`, `prettydoc::html_pretty`, and
  `bookdown::html_document2`.
- `{Report_Packages}`: suggested by default knitr, DT, and kableExtra.

## Common derivations

- `{Briefing_file}` commonly resolves to `{Project_Folder}/briefing.md`.
- `{Specs_Folder}` commonly resolves below `{Project_Folder}`.
- `{Plans_Folder}` commonly resolves below `{Project_Folder}`.

Derivations are conventions, not fixed paths. Confirm any value that is absent or ambiguous.
Skills may define additional placeholders when a workflow requires them.

## Standard project artifact

`project-bootstrap` creates `{Root_Folder}/CHANGELOG.md` from `CHANGELOG.template.md` when the file
does not exist. An existing changelog is preserved. This fixed default is the changelog consumed by
`releasing-version`.

## Template content

The following named placeholders guide generation but do not need to remain as global path keys:

- `{Product_Name}`, `{Product_Summary}`, `{Product_Characteristics}`: concise product context.
- `{Tech_Stack}`: technologies that apply to the project and have no language line, such as
  Apptainer or Docker, or a database.
- `{Setup_Command}`, `{Build_Command}`, `{Run_Command}`, `{Test_Command}`: verified project commands.
- `{Deploy_Command}`: deployment command when the project has one.
- `{Profiles}`: optional Markdown profiles mapped to their language, framework, or test scope.
- `{Folder_Structure}`: concise structure observed in the repository, with only its top-level
  folders and what has no key of its own.
- `{Development_OS}`, `{Development_Shell}`, `{Git_Remote}`, `{Default_Branch}`: observed local and
  repository environment values.

A key value may cite another key written in `{Agents_file}`; the pattern variables of the layout,
such as `<analysis-id>` and `<spec-slug-id>`, are part of the value.
