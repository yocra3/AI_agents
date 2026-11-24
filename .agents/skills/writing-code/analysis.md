# Analysis implementation guidelines

These guidelines apply to the computation scripts, report documents, render scripts, shared
functions, real configuration, test support code, and `run-analysis.sh` of the implementation
plan of an analysis methods document, `{Plans_Folder}/<analysis-id>.plan.md` for
`{Analysis_Methods_file}`. The test support code is the test configuration,
`{Analysis_Test_Config_file}`, and the execution runner `run-tests.sh`, the reference subset
script, the synthetic data generator, and the input checks, which live with the tests in
`{Analysis_Test_Code_Folder}`. Take every path and file name from the Analysis layout keys in
`{Agents_file}`, resolved for the analysis; the implementation plan never redefines them.

The keywords "MUST", "MUST NOT", "SHOULD", etc. are to be interpreted as described in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

## Configuration

- Computation and render scripts run from the repository root and take no command-line
  parameters; the `run-analysis.sh` wrapper is the only exception.
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
  `${ANALYSIS_OUTPUT_ROOT}/figures`, and `${ANALYSIS_OUTPUT_ROOT}/reports`. The execution runner
  sets `ANALYSIS_OUTPUT_ROOT`.
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

- Write the seed declared by the implementation plan as a constant in the code, so both
  configurations use the same seed.

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

## Input checks

The input checks are written in the language of the implementation plan's Input checks section
and run in its image. They read the configuration in `ANALYSIS_CONFIG`, defaulting to the
resolved `{Analysis_Real_Config_file}`, and check every `INPUT_<NAME>` and `REF_<NAME>` key it
sets, with the same code for synthetic and real inputs. They check:

- the Input data section of the methods document, as `{Agents_Folder}/references/analysis-inputs.md`
  defines it: that each Location exists, with the files of a folder's pattern; the format and its
  compression; the structure of the format's family; every constraint of each used column or
  field, missing values included; each design variable's levels, reference level, and minimum
  replicates per level, or its ID pattern and number of levels when its levels identify people;
  the relations between inputs; and, for each reference resource, its version and assembly when
  its format's headers carry them;
- manifests: every listed path exists and every listed file meets its declared format;
- every technical requirement in the implementation plan's Input checks section.

Rules:

- Accept absolute paths and paths relative to the repository root, also inside a manifest.
- Accept columns, fields, and files that no methods step uses.
- In large formats, such as BAM, CRAM, FASTQ, VCF, and BCF, check the header, or the first
  records of a FASTQ file, and the relations with other inputs. Check the full content only of
  tables and matrices.
- Run every check and report every failure before exiting with a failing status. Each failure
  message states which check failed, the key and the column or field, and how many times. Never
  print a value read from the inputs, such as a cell, an identifier, a path, or a header line;
  names that the methods document declares, such as columns and design levels, are allowed.
- Never modify or copy the inputs, and write no files.

## Test data

Tests use real reference resources reduced to a subset and synthetic data instead of the user's
data. The reference subset script and the synthetic data generator are tracked deterministic
scripts, in the language of the Input checks section and run in its image, that create them in
`{Analysis_Test_Inputs_Folder}` by applying the implementation plan's Test data rules exactly.
They never read the user's `INPUT_<NAME>` data.

- **Reference subset script**: derives each `REF_<NAME>` subset from the real resource at its
  Real value in the implementation plan's Configuration, read-only, or from the nf-core
  test-datasets that its Source names, and keeps the resource's headers.
- **Synthetic data generator**: writes each `INPUT_<NAME>` with the format, compression, and
  structure of Input data, the generation rule and planted signal of the implementation plan,
  identifiers taken from the reference subsets, every design level with at least its minimum
  replicates, and every relation between inputs. A synthetic manifest lists synthetic files in
  `{Analysis_Test_Inputs_Folder}`. It sets the Generator seed once at its start and writes
  compressed files without timestamps, so that every run writes the same bytes.

## Execution runner

The execution runner is `run-tests.sh` in `{Analysis_Test_Code_Folder}`, run as
`run-tests.sh <mode> [NN]`. It runs on the host, because scripts run in different images, and may
therefore drive several frameworks. For analysis, it replaces the session-level setup of the
testing frameworks. It sets `ANALYSIS_TEST_MODE` for the checks to `synthetic` in the `increment`
and `synthetic` modes and to `post-run` in the `post-run` mode, passes the environment variables
of this section into each container, and makes the configured input paths visible in it, as the
execution rules require.

In the `increment` and `synthetic` modes, it sets `ANALYSIS_CONFIG` to the test configuration
and `ANALYSIS_OUTPUT_ROOT` to `{Analysis_Test_Run_Folder}`. It runs each script and render
script in its increment's image, recording each exit status and stopping at the first failure,
then each increment's checks in that increment's image with its framework. The checks read the
folders defined by the test configuration. Nothing is written to the versioned folders or to
tracked files.

- `increment <NN>`: run only the scripts and render scripts of increment `NN`, then its checks,
  reusing the earlier increments' outputs already in `{Analysis_Test_Run_Folder}`, which it does
  not empty. For a `post-run` increment, it runs no script, and its checks skip.
- `synthetic [NN]` (default): the full run from scratch. Run every image check, then the setup
  tests in the image of the input checks, then the input checks, and stop at the first failure.
  Then empty `{Analysis_Test_Run_Folder}` and run the scripts and render scripts of the
  `synthetic` increments in implementation plan order, up to increment `NN` when given, then
  their checks.
- `setup`: run only the setup tests, in the image of the input checks.
- `post-run`: no script is executed; the runner runs only the output checks, each increment's in
  its image. They load the real configuration and read the version folders written by the user's
  full run, read-only.
- `input-check`: run only the input checks, with `ANALYSIS_CONFIG` set to the resolved
  `{Analysis_Real_Config_file}`.

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
