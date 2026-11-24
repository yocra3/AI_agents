# Nextflow linting with Nextflow and nf-core tools

Use the repository's pinned Nextflow version and the available nf-core tools installation, and
confirm options with each command's `--help`. From the repository root, select the requested
scope:

- Scripts and configuration files: `nextflow lint <file>`, available from Nextflow 25.04. Fix:
  `nextflow lint -format <file>` formats files without errors; resolve errors by hand.
- Pipeline: `nf-core pipelines lint`.
- Module: `nf-core modules lint <module>`, for each of the project's own modules in scope.
- Subworkflow: `nf-core subworkflows lint <subworkflow>`, for each of the project's own
  subworkflows in scope.

Use component names, not file paths, and not `--all`, which also selects imported components.
Respect `.nf-core.yml`. For non-nf-core projects, report inapplicable conventions rather than
introducing nf-core structure solely to satisfy lint. These checks do not replace execution tests.

Never lint an imported nf-core component, such as those in `modules/nf-core/` and
`subworkflows/nf-core/`, with any check of any language: a component in nf-core is assumed to
have passed nf-core lint. When a check, such as `nf-core pipelines lint`, reports a finding in
one, report it and never fix it.

Official references: [nextflow lint](https://docs.seqera.io/nextflow/reference/cli/lint),
[pipelines](https://nf-co.re/docs/nf-core-tools/cli/pipelines/lint),
[modules](https://nf-co.re/docs/nf-core-tools/cli/modules/lint),
[subworkflows](https://nf-co.re/docs/nf-core-tools/cli/subworkflows/lint).
