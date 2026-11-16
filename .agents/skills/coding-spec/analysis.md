# Analysis implementation guidelines

These guidelines apply to the computation scripts, report documents, render scripts, shared
functions, and configuration files of an analysis plan in `{Analysis_Plans_Folder}`. Take every
path and file name from the Analysis layout keys in `{Agents_file}`, resolved for the plan's
analysis; the plan never redefines them.

The keywords "MUST", "MUST NOT", "SHOULD", etc. are to be interpreted as described in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

## Configuration

- Scripts run from the repository root and take no command-line parameters. Each loads exactly
  one configuration file at its top, from the path in the `ANALYSIS_CONFIG` environment variable,
  defaulting to the resolved `{Analysis_Real_Config_file}`.
- The configuration is a `KEY=value` file with optional double quotes, `#` comment lines, and
  `${VAR}` expansion, and no other code.
- Required keys: `ANALYSIS_ID`, `PLAN_VERSION`, `RESULTS_DIR`, `FIGURES_DIR`, `REPORTS_DIR`, and
  every `INPUT_<NAME>` key in the plan's input table. Validate that each is set before use.
- The real configuration, `{Analysis_Real_Config_file}`, points to the real inputs and to the
  plan version's `{Analysis_Results_Version_Folder}`, `{Analysis_Figures_Version_Folder}`, and
  `{Analysis_Reports_Version_Folder}`. The test configuration, `{Analysis_Test_Config_file}`,
  points to the test subset in `{Analysis_Test_Subset_Folder}` and sets `RESULTS_DIR`,
  `FIGURES_DIR`, and `REPORTS_DIR` to `${ANALYSIS_OUTPUT_ROOT}/results`,
  `${ANALYSIS_OUTPUT_ROOT}/figures`, and `${ANALYSIS_OUTPUT_ROOT}/reports`. The test runner sets
  `ANALYSIS_OUTPUT_ROOT`.
- Code MUST be identical for both configurations: no mode flags, subset-specific branches, or
  hardcoded data paths.
- Each script MUST remain runnable line by line in an interactive session. Do not use
  command-line arguments, `quit()`, or a `main()` entry point.

## Outputs

- Create the configured folders when absent. Write only inside them, overwrite only the script's
  own outputs, and never modify inputs or other versions' folders.

## Provenance

- Each computation script, in any language and verification mode, writes exactly one provenance
  file, `{Analysis_Provenance_file}`, named after the script and always at the root of
  `RESULTS_DIR`. Render scripts MUST NOT write provenance.
- At its start, the script deletes its own provenance file. At its end, after all its other
  outputs, it writes the file, which therefore shows that the last run completed.
- The file is a TSV with the header `key` and `value` and exactly these rows, in this order:
  - `analysis_id` and `plan_version`, from the configuration.
  - `script`: the script's path relative to the repository root.
  - `config`: the configuration file path as given, not its expanded values.
- It MUST NOT record timestamps, host names, user names, or any other value that changes between
  identical runs.

## Randomness

- Set the seed declared by the plan immediately before each random step, as a constant in the
  code, so both configurations use the same seed.

## Reports

- Reports read only files in `RESULTS_DIR` and `FIGURES_DIR`, never raw inputs. The `.Rmd`
  writes no files, and its render script writes only the rendered HTML into `REPORTS_DIR`. Draw
  report figures inline only; definitive figures are saved by computation scripts.
- Run in a report only the simple, cheap analyses the plan assigns to it; keep costly computation
  in computation scripts.
- Prose is limited to neutral statements of what each table or figure shows and which file or
  methodology step produced it. Do not describe, summarize, or interpret values.
- Each report source is a `{Analysis_Report_Source_file}` with the `NN` of its report increment.
  Its render script is a `{Analysis_Script_file}` with the same `NN` and slug; it loads the
  configuration and renders into `REPORTS_DIR`.

## Phases

Read the increment, its files, its image, and its methodology from the plan. Run every command
of an increment phase in the increment's image, the `{Analysis_Images_file}` entry named by its
`Image` ID, under the execution rules in `{Agents_file}`; `renumber`, `real-config`, and
`remove-code` only move, write, or delete files.
Lint each script in its increment's image, each test file in the image of the increment it tests,
and each `{Analysis_Shared_Functions_file}` in the image of any increment of its language.
Every phase except `subset-implementation`, which follows tester's RED, is a direct phase.

- `renumber`: in one pass, rename the computation scripts, render scripts, and `.Rmd` sources of
  renumbered increments to their new `NN` with plain `mv`, in a collision-free order such as
  highest number first or through temporary names. Update every hardcoded reference to the old
  names, such as the `.Rmd` path in render scripts, the provenance file name and `script` row,
  header `Usage:` paths, and calls or sources between scripts, so provenance file names follow
  the script's `NN`. Change nothing else, and use no git commands.
- `real-config`: write `{Analysis_Real_Config_file}` with `PLAN_VERSION` set to the plan version,
  the output folders set to the plan version's Analysis layout version folders, and every
  `INPUT_<NAME>` key of the plan's input table. Verify that every required key is set.
- `subset-implementation`: implement exactly the increment's methodology, which the formal checks
  do not bound. When tester reports, instead of RED, that the existing checks still apply to a
  modified increment, proceed without RED. Reach GREEN as the testing profile defines it, run the
  linting skill on the changed files, and return both pieces of evidence.
- `post-run-implementation`: implement exactly the increment's methodology. Validate it only with
  lint and syntax checks; never run the script.
- `remove-code`: delete the removed increment's code, the files its Removed entry lists.

## Loading the configuration

Write the resolved `{Analysis_Real_Config_file}` path, not the placeholder, as the default, so
that each script stays runnable line by line.

R, after the `library()` calls:

```r
config_path <- Sys.getenv(
  "ANALYSIS_CONFIG",
  "{Analysis_Real_Config_file}"
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
    "ANALYSIS_CONFIG", "{Analysis_Real_Config_file}"
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
config_path="${ANALYSIS_CONFIG:-{Analysis_Real_Config_file}}"
set -a
source "$config_path"
set +a
: "${RESULTS_DIR:?}" "${PLAN_VERSION:?}" "${INPUT_READS:?}"
```
