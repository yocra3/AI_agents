---
name: coding-spec
description: Apply maintainable coding conventions while implementing or refactoring software. Use language profiles and repository conventions; do not activate for documentation-only work.
---

# Coding Conventions

Write the smallest clear change that preserves the repository's design and public contracts.

## Context precedence

1. Explicit task instructions.
2. Existing repository conventions and architecture.
3. Supplied Markdown language or framework profiles.
4. The general guidance below.

Load only profiles relevant to the changed files. The caller may provide any Markdown profile,
and polyglot changes may provide more than one.

## Bundled profiles

- Language guidelines, whenever the changed files use that language: [R](references/R.md),
  [R Markdown](references/rmarkdown.md) together with [R](references/R.md),
  [Python](references/python.md), [Bash](references/bash.md), and [Groovy](references/groovy.md).
- Nextflow scripts and configuration: [Nextflow](references/nextflow.md) together with
  [Groovy](references/groovy.md).
- nf-core modules and subworkflows: also the [nf-core guidelines index](references/nf-core.md),
  which selects the files in `nextflow_guidelines/`.
- Preparatory reference implementation of a Nextflow contract: also
  [Nextflow reference implementation](nextflow-reference.md).
- Scripts, reports, and configurations of an analysis plan: additionally the
  [analysis guidelines](analysis.md).

## General guidance

- Use domain language consistently in names and module boundaries.
- Keep responsibilities cohesive and dependencies directed toward stable interfaces.
- Prefer straightforward control flow and explicit error handling.
- Avoid speculative abstractions, generic utility modules, and unrelated cleanup.
- Preserve established public APIs unless the approved change requires an API change.
- Validate with the formatter, static checks, and tests defined by the repository or profile.

If a required global placeholder or profile path cannot be resolved, stop and report it rather
than inventing a project layout or toolchain.
