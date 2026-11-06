# Analysis implementation guidelines

These guidelines apply to the computation scripts, report documents, render scripts, and
configuration files of an analysis plan in `{Analysis_Plans_Folder}`.

The keywords "MUST", "MUST NOT", "SHOULD", etc. are to be interpreted as described in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

## Configuration

- Scripts run from the repository root and take no command-line parameters. Each loads exactly
  one configuration file at its top, from the path in the `ANALYSIS_CONFIG` environment variable,
  defaulting to `{Analysis_Scripts_Folder}/<analysis-id>/config/real.conf`.
- The configuration is a `KEY=value` file with optional double quotes, `#` comment lines, and
  `${VAR}` expansion, and no other code.
- Required keys: `ANALYSIS_ID`, `PLAN_VERSION`, `RESULTS_DIR`, `FIGURES_DIR`, `REPORTS_DIR`, and
  every `INPUT_<NAME>` key in the plan's input table. Validate that each is set before use.
- `real.conf` points to the real inputs and the versioned output folders. `test.conf` points to
  the test subset and places the output folders under `${ANALYSIS_OUTPUT_ROOT}`, set by the test
  runner.
- Code MUST be identical for both configurations: no mode flags, subset-specific branches, or
  hardcoded data paths.
- Each script MUST remain runnable line by line in an interactive session. Do not use
  command-line arguments, `quit()`, or a `main()` entry point.

## Outputs and provenance

- Create the configured folders when absent. Write only inside them, overwrite only the script's
  own outputs, and never modify inputs or other versions' folders.
- After all its other outputs, each computation script writes
  `RESULTS_DIR/<script-name>.provenance.tsv` with columns `key` and `value` and at least the rows
  `analysis_id`, `plan_version`, `script`, and `config`. It MUST NOT record timestamps, host
  names, or user names.

## Randomness

- Set the seed declared by the plan immediately before each random step, as a constant in the
  code, so both configurations use the same seed.

## Reports

- Reports read only files in `RESULTS_DIR` and `FIGURES_DIR`, never raw inputs, and write no
  files. Draw report figures inline only; definitive figures are saved by computation scripts.
- Run in a report only the simple, cheap analyses the plan assigns to it; keep costly computation
  in computation scripts.
- Prose is limited to neutral statements of what each table or figure shows and which file or
  methodology step produced it. Do not describe, summarize, or interpret values.
- Each report source is `{Analysis_Reports_Folder}/<analysis-id>/<NN>-<slug>.Rmd`, with the `NN`
  of its report increment. Its render script is
  `{Analysis_Scripts_Folder}/<analysis-id>/<NN>-<slug>.<ext>`, with the same `NN` and slug; it
  loads the configuration and renders into `REPORTS_DIR`.

## Phases

Read the increment, its files, and its methodology from the plan. Run every command in the plan's
container image under the execution rules in `{Agents_file}`. Every phase except
`subset-implementation`, which follows tester's RED, is a direct phase.

- `renumber`: in one pass, rename the computation scripts, render scripts, and `.Rmd` sources of
  renumbered increments to their new `NN` with plain `mv`, in a collision-free order such as
  highest number first or through temporary names. Update every internal reference to the old
  names, such as the `.Rmd` path in render scripts, hardcoded provenance file names or `script`
  rows, header `Usage:` paths, and calls or sources between scripts. Change nothing else, and use
  no git commands.
- `real-config`: write `real.conf` with `PLAN_VERSION` set to the plan version, the output folders
  set to the plan's `vN` folders, and every `INPUT_<NAME>` key of the plan's input table. Verify
  that every required key is set.
- `subset-implementation`: implement exactly the increment's methodology, which the formal checks
  do not bound. When tester reports, instead of RED, that the existing checks still apply to a
  modified increment, proceed without RED. Reach GREEN as the testing profile defines it, run the
  linting skill on the changed files, and return both pieces of evidence.
- `post-run-implementation`: implement exactly the increment's methodology. Validate it only with
  lint and syntax checks; never run the script.
- `remove-code`: delete the removed increment's code, the files its Removed entry lists.

## Loading the configuration

Write the resolved real configuration path, not the placeholder, as the default.

R, after the `library()` calls:

```r
config_path <- Sys.getenv(
  "ANALYSIS_CONFIG",
  "{Analysis_Scripts_Folder}/<analysis-id>/config/real.conf"
)
readRenviron(config_path)
config <- as.list(Sys.getenv(c(
  "ANALYSIS_ID", "PLAN_VERSION", "RESULTS_DIR", "FIGURES_DIR", "INPUT_COUNTS"
)))
stopifnot(all(nzchar(unlist(config))))
```

Python, standard library only, after the imports:

```python
import os
from pathlib import Path

config_path = Path(os.environ.get(
    "ANALYSIS_CONFIG", "{Analysis_Scripts_Folder}/<analysis-id>/config/real.conf"
))
config = {}
for line in config_path.read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#"):
        key, value = line.split("=", 1)
        key = key.strip()
        config[key] = os.path.expandvars(value.strip().strip('"'))
        os.environ[key] = config[key]  # later lines may reference this key
```

Bash, after `set -euo pipefail` (skip that line when running interactively):

```bash
config_path="${ANALYSIS_CONFIG:-{Analysis_Scripts_Folder}/<analysis-id>/config/real.conf}"
set -a
source "$config_path"
set +a
: "${RESULTS_DIR:?}" "${PLAN_VERSION:?}" "${INPUT_READS:?}"
```
