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

- `{Analysis_Plans_Folder}`: analysis plans, named `analysis-<slug>.md`. It must not be, or be
  inside, `{Specs_Folder}` or `{Plans_Folder}`.
- `{Analysis_Scripts_Folder}`: tracked computation scripts and configurations, one
  `<analysis-id>/` subfolder per analysis.
- `{Analysis_Tests_Folder}`: tracked analysis tests, separate from the scripts, one
  `<analysis-id>/` subfolder per analysis; test run outputs go to its ignored `results/` subfolder.
- `{Analysis_Reports_Folder}`: tracked report sources; rendered reports go to ignored
  `<analysis-id>/vN/` subfolders.
- `{Analysis_Results_Folder}` and `{Analysis_Figures_Folder}`: ignored `<analysis-id>/vN/` outputs.
- `{Analysis_Test_Data_Folder}`: ignored test subsets, below `{Project_Folder}`.

The analysis profiles also require execution rules in `{Agents_file}` that state how to run
commands in a plan's container image.

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
does not apply; do not leave anonymous or unresolved placeholders in the generated file.
