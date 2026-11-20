# Analysis testing with formal checks

Use these rules for the `tester` phases of the implementation plan of an analysis methods
document, `{Plans_Folder}/<analysis-id>.plan.md` for `{Analysis_Methods_file}`, in every
language. Output checks test the implementation plan's formal acceptance criteria through output
files and never validate experimental results. Input checks test the inputs, and image checks
test the tier-4 images. The supporting test artifacts are the test configuration,
`{Analysis_Test_Config_file}`, and the execution runner, the reference subset script, the
synthetic data generator, the input checks, and the image checks, which live with the tests in
`{Analysis_Test_Code_Folder}`. Every other path comes from the Analysis layout keys in
`{Agents_file}`. Read each increment, its acceptance criteria, and its verification mode from the
implementation plan.

Under the execution rules in `{Agents_file}`, each increment's scripts and checks run in the
increment's image, the `{Analysis_Images_file}` entry named by its `Image` ID. The reference
subset script, the synthetic data generator, and the input checks run in the image of the
implementation plan's Input checks section, in its language.

## Allowed and forbidden output checks

These rules override the skill's general guidance on reference outputs and test doubles.

- Check only formal properties: file existence at the configured path, format and parseability,
  column names and types, row counts relative to an input (for example, one row per sample in the
  samplesheet, read at check time), successful execution, the provenance files as defined below,
  seed reproducibility, and report rendering and sections.
- Do not use reference outputs or snapshots of values, and do not assert statistics, p-values,
  effect sizes, numbers of significant features, or any other value that depends on the results.
  Do not fix row counts to the size of the test inputs.
- Test scripts from the outside through their output files; do not call their internal functions
  or inspect their variables, so tests survive refactoring.

## Image checks

Write one permanent image check per tier-4 image, a Bash script run on the host that finds the
image through its `{Analysis_Images_file}` entry and runs read-only commands in it. It checks that
the entry and its image file exist and that the image provides every package of the image's
Contents in the Images table at its version, the test framework and the linter listed there, and
rmarkdown and Pandoc when listed. A missing entry or image file means the image is missing.

## Input checks

The input checks read the configuration in `ANALYSIS_CONFIG`, defaulting to the resolved
`{Analysis_Real_Config_file}`, and check every `INPUT_<NAME>` and `REF_<NAME>` key it sets, with
the same code for synthetic and real inputs. They check:

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
data; they never read the user's `INPUT_<NAME>` data. Create both in
`{Analysis_Test_Inputs_Folder}`, only in `test-setup`, with tracked deterministic scripts that
apply the implementation plan's Test data rules exactly.

- **Reference subset script**: derives each `REF_<NAME>` subset from the real resource at its
  Real value in the implementation plan's Configuration, read-only, or from the nf-core
  test-datasets that its Source names, and keeps the resource's headers. When a resource is not
  at its Location, stop and name the missing file.
- **Synthetic data generator**: writes each `INPUT_<NAME>` with the format, compression, and
  structure of Input data, the generation rule and planted signal of the implementation plan,
  identifiers taken from the reference subsets, every design level with at least its minimum
  replicates, and every relation between inputs. A synthetic manifest lists synthetic files in
  `{Analysis_Test_Inputs_Folder}`. It sets the Generator seed once at its start and writes
  compressed files without timestamps, so that every run writes the same bytes.

If a rule cannot be applied, or a `synthetic` increment cannot produce non-empty outputs from the
test inputs, stop and report it instead of changing the rule.

## Frameworks

Each increment's output checks use the framework of the language profile for the increment's
`Language`, in the increment's image. Name each test file with the increment's two-digit `NN` and
slug in the framework's pattern.

## Execution and check modes

The `ANALYSIS_TEST_MODE` environment variable selects the runner's mode. The execution runner runs
on the host, because scripts run in different images, and may therefore drive several frameworks.
For analysis, it replaces the session-level setup of the language profiles. It passes the
environment variables of this section into each container and makes the configured input paths
visible in it, as the execution rules require.

- `synthetic` (default): run every image check, then the input checks with `ANALYSIS_CONFIG` set
  to the test configuration, and stop at the first failure. Then set `ANALYSIS_OUTPUT_ROOT` to
  `{Analysis_Test_Run_Folder}`, emptied before each run, and run the scripts and render scripts of
  the `synthetic` increments, each in its increment's image, in implementation plan order up to
  the increment under test; record each exit status and stop at the first failure. Then run each
  increment's checks in that increment's image with its framework; the checks read the folders
  defined by the test configuration. Nothing is written to the versioned folders or to tracked
  files.
- `post-run`: no script is executed; the runner runs only the output checks, each increment's in
  its image. They load the real configuration and read the version folders written by the user's
  full run, read-only.
- `input-check`: run only the input checks, with `ANALYSIS_CONFIG` set to the resolved
  `{Analysis_Real_Config_file}`.
- Skip mode-specific checks with an explicit reason: exit status and reproducibility checks run in
  `synthetic` mode only, and checks of `post-run` increments run in `post-run` mode only.
- Report the exact test commands for every mode.

## Phases

- `image-check`: write the image check of the tier-4 image that the marker names and run it. RED
  is valid only when the image is missing or lacks a required package; any other failure, such as
  a syntax error or a missing host tool, is not. When the image already exists and passes, report
  that instead of RED.
- `test-setup`: write or rewrite the reference subset script, the synthetic data generator, the
  input checks, the test configuration, and the runner, then create the test inputs. After
  `coder: renumber`, also rename the test files of renumbered increments to their new `NN` and
  update the script names they call and the runner's script list. Confirm that:
  - the reference subsets and the synthetic inputs follow the Test data rules, and a second
    generator run writes byte-identical files;
  - the input checks pass on the test inputs and fail, with the expected message, on a temporary
    broken copy of one synthetic input, such as one without a used column; delete the copy;
  - `{Analysis_Test_Config_file}` sets `ANALYSIS_ID`, `ANALYSIS_VERSION` to the implementation
    plan's `Version`, every `INPUT_<NAME>`, `REF_<NAME>`, and global parameter key of
    Configuration to its Test value, and `RESULTS_DIR`, `FIGURES_DIR`, and `REPORTS_DIR` to the
    `results`, `figures`, and `reports` subfolders of `${ANALYSIS_OUTPUT_ROOT}`;
  - the runner launches each script and each increment's checks in that increment's image.
  It has no RED.
- `real-input-check`: run the runner in `input-check` mode and report its result with the failure
  messages only. Do not read or print the real inputs in any other way, and do not change the
  inputs or the checks to make them pass.
- `synthetic-test`: write the output checks for the increment. RED is valid only when the
  increment's checks fail because its outputs are missing or malformed, including because its
  script does not exist yet, while the test inputs, configuration, runner, images, image and input
  checks, framework, and earlier increments work. For a modified increment whose acceptance
  criteria are unchanged, report that the existing checks still apply instead of RED.
- `post-run-checks`: write checks that run only in `post-run` mode. Confirm that they load and are
  skipped in `synthetic` mode. Do not attempt RED or run the increment's script.
- `remove-tests`: remove the tests of removed criteria or increments. Then confirm GREEN, as
  defined below, for the remaining `synthetic` increments whose phases are complete. Skip this
  confirmation while a Setup phase is pending, because the test inputs and configurations are not
  yet current.
- GREEN means that the runner passes in `synthetic` mode: the image checks, the input checks, and
  every check of the current and earlier `synthetic` increments.

## Provenance

Check the `{Analysis_Provenance_file}` of every computation script executed up to the increment
under test in `synthetic` mode, or of every computation script of the implementation plan in
`post-run` mode. Each is a TSV with the header `key` and `value` and exactly the rows
`analysis_id`, `analysis_version`, `script`, and `config`, in this order, with `analysis_version`
equal to the implementation plan's `Version`. In `post-run` mode, the provenance file shows that
its script completed.

## Reports

- Render each report through its render script in `synthetic` mode. Check the exit status, that
  the rendered file exists in the configured reports folder, and that its headings contain the
  headings of the increment's entry in the implementation plan's Reports, in order.
- Check that rendering creates or modifies no file in the results or figures folders, by comparing
  their file listings and checksums before and after rendering.
- Do not assert values shown in tables or figures, or computed by the report.

## Reproducibility

When a criterion requires it, run the execution a second time with `ANALYSIS_OUTPUT_ROOT` set to
`{Analysis_Test_Rerun_Folder}` and compare the criterion's files in `RESULTS_DIR` of both runs
byte for byte. Compare only files in `RESULTS_DIR`; never compare figures or rendered reports,
whose metadata may embed timestamps.
