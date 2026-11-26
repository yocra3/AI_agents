---
name: project-bootstrap
description: Initialize or refresh a project's global agent instructions, briefing, and changelog. Use only when explicitly invoked for project bootstrap.
---

# Project Bootstrap

Use [blueprint.md](./blueprint.md) to define the project's global placeholders and
[AGENTS.template.md](./AGENTS.template.md) to create or update `{Agents_file}`.
Use [CHANGELOG.template.md](./CHANGELOG.template.md) only when `{Root_Folder}/CHANGELOG.md` does
not already exist.

## Workflow

1. Resolve the required global path placeholders. Ask the user to confirm any value that cannot be
   resolved safely.
2. Review the existing `{Agents_file}`, `{Briefing_file}`, `{Root_Folder}/CHANGELOG.md`, repository
   structure, applicable technical profiles, and verified development commands.
3. Propose, for each language of the Tech Stack, the blueprint's toolchain and recommended
   packages and, for a project with R Markdown reports, its report format and packages. Ask the
   user to accept, edit, or decline each.
4. Render `{Agents_file}` from the template. Replace named content placeholders, include the
   observed folder structure, and omit optional fields that do not apply. Include:
   - the Analysis workflow, Analysis layout, and Container execution rules sections only when the
     project has an analysis workflow, with the layout's defaults and each execution rule
     confirmed with the user;
   - `Nextflow_Reference_Folder` only in a Nextflow project, whose Tech Stack has a Nextflow
     line;
   - `ToolUniverse_CLI` only when the user gives its path;
   - in the Tech Stack, only the toolchains, packages, and report format that the user accepted
     or edited, without the parts declined or empty lines; `{Tech_Stack}` only when a technology
     without a language line remains; the sentence on packages only when a line lists packages,
     and the one on the report format only with the Reports line.
5. Confirm that the generated file contains no anonymous or unresolved template placeholders.
6. Update `{Briefing_file}` with a short, feature-focused product summary.
7. Create `{Root_Folder}/CHANGELOG.md` from the changelog template when it is absent. Never replace
   or truncate an existing changelog.
8. Report the resolved global placeholders, selected profiles, commands, and changed files. For
   an analysis workflow, also give the blueprint's recommendation to deny `Read` on the data
   folders.

Do not infer paths that would move work outside `{Root_Folder}`. This skill is a manual
bootstrap workflow and must not be invoked implicitly by other agents.
