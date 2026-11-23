# Analysis documentation guidelines

These guidelines apply to the scripts, shared functions, and report sources of the
implementation plan of an analysis methods document. Where they are stricter than a language
profile, they take precedence. Documenting analysis code changes comments only.

## Rules

- Add or edit full-line comments only. Do not change code, strings, Python docstrings, YAML front
  matter, chunk options, report prose, or code-line whitespace, and do not append comments to code
  lines.
- Do not create `man/`, `NAMESPACE`, or other generated documentation, and do not run roxygen,
  pkgdown, Sphinx, or similar generators.
- Take purposes, inputs, and outputs from the methods document, the implementation plan, and the
  code. Describe what the code does and produces, never results, expectations, or
  interpretations.
- Document every shared function with its language's function comment block.

## Script headers

Place a `#` header at the top of every computation and render script, after any shebang:

```text
# Purpose: <what the script computes, citing the methods steps, e.g. M1-M2>
# Methods: <resolved {Analysis_Methods_file}>
# Usage: <Rscript|python3|bash> <script path>, from the repository root. Loads ANALYSIS_CONFIG,
#   or <resolved {Analysis_Real_Config_file}> by default.
# Inputs: <configuration keys and upstream files>
# Outputs: <files written to RESULTS_DIR, FIGURES_DIR, or REPORTS_DIR; for a computation script,
#   also its provenance file>
```

Resolve the layout keys from `{Agents_file}` for the analysis.

For a report, add one HTML comment `<!-- ... -->` after the YAML front matter with its purpose,
render script, and files read.

