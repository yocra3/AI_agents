# Global Placeholder Blueprint

Define these values in the project's global agent instructions.

## Required

- `{Root_Folder}`: repository root containing product and agent files.
- `{Agents_Folder}`: folder containing reusable project skills and workflow resources.
- `{Custom_Agents_Folder}`: folder containing Codex custom agent definitions.
- `{Agents_file}`: global project instructions file.
- `{Project_Folder}`: product requirements and architecture documentation folder.
- `{Briefing_file}`: short product briefing file.
- `{Specs_Folder}`: feature, fix, and maintenance specifications folder.
- `{Plans_Folder}`: implementation plans folder.

## Analysis workflow

Required only when the project uses `data_analyst` and `analysis_coordinator`:

- `{Analysis_Plans_Folder}`: analysis plans. It must not be, or be inside, `{Specs_Folder}` or
  `{Plans_Folder}`.
- `{Analysis_Scripts_Folder}`: tracked computation scripts, render scripts, shared functions, and
  configurations.
- `{Analysis_Tests_Folder}`: tracked analysis tests, separate from the scripts; test run outputs
  are ignored.
- `{Analysis_Reports_Folder}`: tracked report sources; rendered reports are ignored.
- `{Analysis_Results_Folder}` and `{Analysis_Figures_Folder}`: ignored outputs.
- `{Analysis_Test_Data_Folder}`: ignored test subsets, below `{Project_Folder}`.

The Analysis layout keys place each analysis's files inside these folders; the template's
Analysis layout section explains their role and pattern variables. Fill each with its default
unless the project confirms another layout, and keep the pattern variables as written.

- `{Analysis_Plan_file}`: `{Analysis_Plans_Folder}/<analysis-id>.md`
- `{Analysis_Script_file}`: `{Analysis_Scripts_Folder}/<analysis-id>/<NN>-<slug>.<ext>`
- `{Analysis_Shared_Functions_file}`: `{Analysis_Scripts_Folder}/<analysis-id>/functions.<ext>`
- `{Analysis_Real_Config_file}`: `{Analysis_Scripts_Folder}/<analysis-id>/config/real.conf`
- `{Analysis_Test_Config_file}`: `{Analysis_Scripts_Folder}/<analysis-id>/config/test.conf`
- `{Analysis_Report_Source_file}`: `{Analysis_Reports_Folder}/<analysis-id>/<NN>-<slug>.Rmd`
- `{Analysis_Results_Version_Folder}`: `{Analysis_Results_Folder}/<analysis-id>/vN/`
- `{Analysis_Figures_Version_Folder}`: `{Analysis_Figures_Folder}/<analysis-id>/vN/`
- `{Analysis_Reports_Version_Folder}`: `{Analysis_Reports_Folder}/<analysis-id>/vN/`
- `{Analysis_Test_Code_Folder}`: `{Analysis_Tests_Folder}/<analysis-id>/`
- `{Analysis_Test_Subset_Folder}`: `{Analysis_Test_Data_Folder}/<analysis-id>/`
- `{Analysis_Test_Run_Folder}`: `{Analysis_Tests_Folder}/<analysis-id>/results/subset/`
- `{Analysis_Test_Rerun_Folder}`: `{Analysis_Tests_Folder}/<analysis-id>/results/rerun/`
- `{Analysis_Provenance_file}`: `<RESULTS_DIR>/<NN>-<slug>.provenance.tsv`

The analysis profiles also require execution rules in `{Agents_file}` that state how to run a
command in an increment's container image.

## Common derivations

- `{Briefing_file}` commonly resolves to `{Project_Folder}/briefing.md`.
- `{Specs_Folder}` commonly resolves below `{Project_Folder}`.
- `{Plans_Folder}` commonly resolves below `{Project_Folder}`.
- `{Custom_Agents_Folder}` commonly resolves to Codex's project custom-agent folder.

Derivations are conventions, not fixed paths. Confirm any value that is absent or ambiguous.
Skills may define additional placeholders when a workflow requires them.

## Standard project artifact

`project-bootstrap` creates `{Root_Folder}/CHANGELOG.md` from `CHANGELOG.template.md` when the file
does not exist. An existing changelog is preserved. This fixed default is the changelog consumed by
`releasing-version`.

## Template content

The following named placeholders guide generation but do not need to remain as global path keys:

- `{Product_Name}`, `{Product_Summary}`, `{Product_Characteristics}`: concise product context.
- `{Tech_Stack}`: only technologies that apply to the project.
- `{Setup_Command}`, `{Build_Command}`, `{Run_Command}`, `{Test_Command}`: verified project commands.
- `{Deploy_Command}`: deployment command when the project has one.
- `{Profiles}`: optional Markdown profiles mapped to their language, framework, or test scope.
- `{Folder_Structure}`: concise structure observed in the repository, including the resolved
  agent, skill, project, specification, and plan paths.
- `{Development_OS}`, `{Development_Shell}`, `{Git_Remote}`, `{Default_Branch}`: observed local and
  repository environment values.

Replace these values while generating `{Agents_file}`. Omit an optional section or command when it
does not apply; do not leave anonymous or unresolved placeholders in the generated file. Key
values may cite other global keys, and the Analysis layout's pattern variables are not
placeholders.
