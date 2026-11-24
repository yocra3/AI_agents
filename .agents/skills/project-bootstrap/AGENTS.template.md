# Agents Instructions

- **Root_Folder**: {Root_Folder}
- **Agents_Folder**: {Agents_Folder}
- **Agents_file**: {Agents_file}
- **Project_Folder**: {Project_Folder}
- **Briefing_file**: {Briefing_file}
- **Specs_Folder**: {Specs_Folder}
- **Plans_Folder**: {Plans_Folder}
- **Nextflow_Reference_Folder**: {Nextflow_Reference_Folder} (reference implementation of a
  Nextflow component: versioned generation and validation scripts in `scripts/`; generated
  inputs, outputs and manifests in `results/`, ignored by Git)
- **ToolUniverse_CLI**: {ToolUniverse_CLI} (path of the ToolUniverse `tu` executable, used by
  `searching-tooluniverse-catalog`)

## Product Overview

{Product_Name} is {Product_Summary}.

{Product_Characteristics}

## Technical Implementation

### Tech Stack

{Tech_Stack}

- **{Language}**: tests {Test_Framework}; lint {Linter}; packages {Language_Packages}
- **Reports**: R Markdown, output `{Report_Format}`; packages {Report_Packages}

Prefer these packages for support tasks, such as data handling, file input and output, and
figures, and name any other in the implementation plan. Use another report format only when the
user asks for it.

### Technical profiles

{Profiles}

### Development workflow

```bash
# Set up the project
{Setup_Command}
# Build/Compile the project
{Build_Command}
# Run the project
{Run_Command}
# Test the project
{Test_Command}
# Deploy the project
{Deploy_Command}
```

### Folder structure
```text
{Folder_Structure}
```

### Analysis workflow

`data-analyst` and `implementation-coordinator` run as main sessions. Before authorizing
`implementation-coordinator` to execute a methods document, validate it by running `reviewer` as
a main session.

### Analysis layout

These keys hold every path and file-name pattern of an analysis. The analysis profiles cite them,
and implementation plans never redefine them. `<analysis-id>` is the methods document's ID
(`analysis-<slug>`), `<NN>-<slug>` is an increment's two-digit number and slug, `<ext>` is the
script language's extension, `vN` is the methods document's version, and `<RESULTS_DIR>` is the
configured results folder.

- **Analysis_Methods_Folder**: {Analysis_Methods_Folder} (analysis methods documents)
- **Analysis_Methods_file**: {Analysis_Methods_file}
- **Analysis_Images_file**: {Analysis_Images_file} (container image registry, shared by all
  analyses)
- **Analysis_Recipes_Folder**: {Analysis_Recipes_Folder} (versioned recipes of tier-4 container
  images)
- **Analysis_Images_Folder**: {Analysis_Images_Folder} (built image files, ignored by Git)
- **Analysis_Script_file**: {Analysis_Script_file} (computation and render scripts)
- **Analysis_Shared_Functions_file**: {Analysis_Shared_Functions_file} (one per language, no `NN`)
- **Analysis_Real_Config_file**: {Analysis_Real_Config_file}
- **Analysis_Test_Config_file**: {Analysis_Test_Config_file}
- **Analysis_Report_Source_file**: {Analysis_Report_Source_file}
- **Analysis_Results_Version_Folder**: {Analysis_Results_Version_Folder}
- **Analysis_Figures_Version_Folder**: {Analysis_Figures_Version_Folder}
- **Analysis_Reports_Version_Folder**: {Analysis_Reports_Version_Folder}
- **Analysis_Test_Code_Folder**: {Analysis_Test_Code_Folder} (tests, execution runner, reference
  subset script, synthetic data generator, input checks, and image checks)
- **Analysis_Test_Inputs_Folder**: {Analysis_Test_Inputs_Folder} (reference subsets and synthetic
  data)
- **Analysis_Test_Run_Folder**: {Analysis_Test_Run_Folder} (`synthetic` mode outputs)
- **Analysis_Test_Rerun_Folder**: {Analysis_Test_Rerun_Folder} (reproducibility rerun outputs)
- **Analysis_Provenance_file**: {Analysis_Provenance_file} (one per computation script, at the
  root of `RESULTS_DIR`)

### Container execution rules

Every analysis command runs in a container image, the `{Analysis_Images_file}` entry named by its
ID.

- **Engine**: {Container_Engine}
- **Run a command**: {Container_Run_Rule}
- **Image available**: {Container_Image_Availability}
- **Image build**: {Container_Build_Permissions}

## Environment
- **OS dev**: {Development_OS}
- **Terminal**: {Development_Shell}
- **Git remote**: {Git_Remote}
- **Default branch**: {Default_Branch}

## Behavior Guidelines

- Code and documentation must be in English.
- Chat responses must be in the language of the user prompt.
- Sacrifice grammar for conciseness when needed to fit response limits.

### Naming Conventions

Use slugs with hyphens for any identifiers or non code file names.
