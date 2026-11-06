# Analysis documentation guidelines

These guidelines apply to the scripts, shared functions, and report sources of an analysis plan,
in the documentation phase after review. Where they are stricter than a language profile, they
take precedence. The phase changes comments only.

## Rules

- Add or edit full-line comments only. Do not change code, strings, Python docstrings, YAML front
  matter, chunk options, report prose, or code-line whitespace, and do not append comments to code
  lines.
- Do not create `man/`, `NAMESPACE`, or other generated documentation, and do not run roxygen,
  pkgdown, Sphinx, or similar generators.
- Take purposes, inputs, and outputs from the plan and the code. Describe what the code does and
  produces, never results, expectations, or interpretations.
- Document every shared function with its language's function comment block.

## Script headers

Place a `#` header at the top of every computation and render script, after any shebang:

```text
# Purpose: <what the script computes, citing the plan's methodology steps, e.g. M1-M2>
# Plan: {Analysis_Plans_Folder}/<analysis-id>.md
# Usage: <Rscript|python3|bash> <script path>, from the repository root. Loads ANALYSIS_CONFIG,
#   or the real-data configuration by default.
# Inputs: <configuration keys and upstream files>
# Outputs: <files written to RESULTS_DIR, FIGURES_DIR, or REPORTS_DIR, including provenance>
```

For a report, add one HTML comment `<!-- ... -->` after the YAML front matter with its purpose,
render script, and files read.

## Python

Write the script header and function documentation as `#` comment blocks instead of docstrings,
so the diff stays comments-only. Place a function's block immediately above `def`, with the
`Args:` and `Returns:` sections of a Google-style docstring.

## Validation

- Every added or removed line in the diff is blank, a full-line comment starting with `#` after
  indentation, or part of an HTML comment in a `.Rmd` file. The shebang is unchanged.
- The lint checks and the `subset` test suite still pass, run in the plan's container image under
  the execution rules in `{Agents_file}`.
