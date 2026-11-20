# Analysis implementation guidelines

These guidelines apply to the computation scripts, report documents, render scripts, shared
functions, real configuration, image recipes, and `run-analysis.sh` of the implementation plan of
an analysis methods document, `{Plans_Folder}/<analysis-id>.plan.md` for
`{Analysis_Methods_file}`. Take every path and file name from the Analysis layout keys in
`{Agents_file}`, resolved for the analysis; the implementation plan never redefines them.

The keywords "MUST", "MUST NOT", "SHOULD", etc. are to be interpreted as described in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

## Configuration

- Computation and render scripts run from the repository root and take no command-line
  parameters; the `run-analysis.sh` wrapper of the `run-script` phase is the only exception.
  Each loads exactly one configuration file at its top, from the path in the `ANALYSIS_CONFIG`
  environment variable, defaulting to the resolved `{Analysis_Real_Config_file}`.
- The configuration is a `KEY=value` file with optional double quotes, `#` comment lines, and
  `${VAR}` expansion, and no other code.
- Required keys: `ANALYSIS_ID`, `ANALYSIS_VERSION`, `RESULTS_DIR`, `FIGURES_DIR`, `REPORTS_DIR`,
  and every `INPUT_<NAME>`, `REF_<NAME>`, and global parameter key of the implementation plan's
  Configuration. Validate that each key a script uses is set before use.
- The real configuration, `{Analysis_Real_Config_file}`, points to the real inputs and to the
  version's `{Analysis_Results_Version_Folder}`, `{Analysis_Figures_Version_Folder}`, and
  `{Analysis_Reports_Version_Folder}`. The test configuration, `{Analysis_Test_Config_file}`,
  points to the test inputs in `{Analysis_Test_Inputs_Folder}` and sets `RESULTS_DIR`,
  `FIGURES_DIR`, and `REPORTS_DIR` to `${ANALYSIS_OUTPUT_ROOT}/results`,
  `${ANALYSIS_OUTPUT_ROOT}/figures`, and `${ANALYSIS_OUTPUT_ROOT}/reports`. The test runner sets
  `ANALYSIS_OUTPUT_ROOT`.
- Input paths may be absolute or relative to the repository root, also inside a manifest. When
  writing a path, prefer a relative one; keep a path outside the repository absolute.
- Code MUST be identical for both configurations: no mode flags, test-specific branches, or
  hardcoded data paths.
- Each computation and render script MUST remain runnable line by line in an interactive
  session. Do not use command-line arguments, `quit()`, or a `main()` entry point.

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
  - `analysis_id` and `analysis_version`, from the configuration.
  - `script`: the script's path relative to the repository root.
  - `config`: the configuration file path as given, not its expanded values.
- It MUST NOT record timestamps, host names, user names, or any other value that changes between
  identical runs.

## Randomness

- Set the seed declared by the implementation plan immediately before each random step, as a
  constant in the code, so both configurations use the same seed.

## Reports

- Reports read only files in `RESULTS_DIR` and `FIGURES_DIR`, never raw inputs. The `.Rmd`
  writes no files, and its render script writes only the rendered HTML into `REPORTS_DIR`. Draw
  report figures inline only; definitive figures are saved by computation scripts.
- Run in a report only the simple, cheap calculations of its entry in the implementation plan's
  Reports; keep costly computation in computation scripts.
- Prose is limited to neutral statements of what each table or figure shows and which file or
  methods step produced it. Do not describe, summarize, or interpret values.
- Each report source is a `{Analysis_Report_Source_file}` with the `NN` of its report increment.
  Its render script is a `{Analysis_Script_file}` with the same `NN` and slug; it loads the
  configuration and renders into `REPORTS_DIR`.

## Phases

Read the increment, its files, its image, and its methods steps from the implementation plan. Run
every command of an increment phase in the increment's image, the `{Analysis_Images_file}` entry
named by its `Image` ID, under the execution rules in `{Agents_file}`; `renumber`, `real-config`,
and `remove-code` only move, write, or delete files.
Lint each script in its increment's image, each test file in the image of the increment it tests,
each `{Analysis_Shared_Functions_file}` in the image of any increment of its language, and
`run-analysis.sh` with the Bash lint checks in any image that provides them or on the host.
`image-build` and `synthetic-implementation` follow tester's RED; every other phase is a direct
phase.

- `renumber`: in one pass, rename the computation scripts, render scripts, and `.Rmd` sources of
  renumbered increments to their new `NN` with plain `mv`, in a collision-free order such as
  highest number first or through temporary names. Update every hardcoded reference to the old
  names, such as the `.Rmd` path in render scripts, the provenance file name and `script` row,
  header `Usage:` paths, and calls or sources between scripts, so provenance file names follow
  the script's `NN`. Change nothing else, and use no git commands.
- `image-build`: build the tier-4 image that the marker names with building-container-images,
  which writes its recipe, builds it, and adds its registry entry. Reach GREEN with tester's image
  check. When Docker or `fakeroot` permissions are missing, stop and report what to ask the
  administrator for.
- `real-config`: write `{Analysis_Real_Config_file}` with `ANALYSIS_ID`, `ANALYSIS_VERSION` set to
  the implementation plan's `Version`, the output folders set to the version folders of the
  Analysis layout, and every `INPUT_<NAME>`, `REF_<NAME>`, and global parameter key of
  Configuration with its Real value. Verify that every required key is set. Do not read the
  inputs.
- `synthetic-implementation`: implement exactly the increment's methods steps, which the formal
  checks do not bound. When tester reports, instead of RED, that the existing checks still apply
  to a modified increment, proceed without RED. Reach GREEN as the testing profile defines it, run
  the linting skill on the changed files, and return both pieces of evidence.
- `post-run-implementation`: implement exactly the increment's methods steps. Validate it only
  with lint and syntax checks; never run the script.
- `remove-code`: delete the removed increment's code, the files its Removed entry lists.
- `run-script`: write or rewrite `run-analysis.sh`, as defined below. Validate it only with lint;
  never execute it.

## Final refactoring

In `cleaner: analysis-refactor`, the single final refactoring phase of an analysis, refactor once
the computation scripts, render scripts, report sources, and shared functions of every increment
of the implementation plan, as its `Files` list them.

- Preserve behavior: the same outputs, file names, provenance, seeds, and configuration keys, and
  every script still runnable line by line.
- Shared functions may move to `{Analysis_Shared_Functions_file}`.
- Do not modify the test or real configurations, the tests or their supporting test artifacts,
  such as the runner, the input checks, the image checks, the synthetic data generator, and the
  reference subset script, the test inputs, the image recipes, or `run-analysis.sh`.
- Reach GREEN as the testing profile defines it, and validate `post-run` increments with lint and
  syntax checks only.

## run-analysis.sh

`run-analysis.sh` has no `NN` prefix and lives in the folder of `{Analysis_Script_file}`. It is a
plain Bash script with `set -euo pipefail`, run on the host from the repository root, with no
SLURM headers or dry-run mode. It does not set `ANALYSIS_CONFIG`, so every step uses the default
real configuration. Its optional positional arguments `[FROM [TO]]` are inclusive `NN` bounds: no
arguments run everything, `run-analysis.sh 10` resumes from `10`, and `run-analysis.sh 13 16`
runs `13` to `16`.

On every run, also with `[FROM [TO]]`, it runs these steps in order and stops at the first
failure:

1. Check that the image of the input checks and the image of every script it will run are
   available under the execution rules in `{Agents_file}`, for example that an image file exists.
   A missing image stops the run with a message that names its image ID and the
   `{Analysis_Images_file}` entry or the implementation plan's Images row that provides it.
2. Run the input checks in their image, making the configured input paths visible in it as the
   execution rules require. A failure stops the run with their messages and states that no script
   ran and that the inputs must be fixed first.
3. Run every computation script and render script of the implementation plan in the range,
   including `post-run` increments, in `NN` order, each in its increment's image under the
   execution rules. Before each script, print one line with the script's `NN`, file name, and
   start time, and no other logging.

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
  "ANALYSIS_ID", "ANALYSIS_VERSION", "RESULTS_DIR", "FIGURES_DIR",
  "INPUT_COUNTS", "REF_ANNOTATION"
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
: "${RESULTS_DIR:?}" "${ANALYSIS_VERSION:?}" "${INPUT_READS:?}" "${REF_GENOME:?}"
```
