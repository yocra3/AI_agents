# Analysis testing with formal checks

Use these rules for the tests of the implementation plan of an analysis methods document,
`{Plans_Folder}/<analysis-id>.plan.md` for `{Analysis_Methods_file}`, in every language. Output
checks test the implementation plan's formal acceptance criteria through output files and never
validate experimental results. Image checks test the tier-4 images, and setup tests test the test
support code: the test configuration, `{Analysis_Test_Config_file}`, and the execution runner
`run-tests.sh`, the reference subset script, the synthetic data generator, and the input checks.
Tests live with the test support code in `{Analysis_Test_Code_Folder}`, but these rules write
only tests and their static data. Every other path comes from the Analysis layout keys in `{Agents_file}`. Read each
increment, its acceptance criteria, and its verification mode from the implementation plan.

Under the execution rules in `{Agents_file}`, each increment's checks run in the increment's
image, the `{Analysis_Images_file}` entry named by its `Image` ID, and the setup tests run in the
image of the implementation plan's Input checks section.

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
the entry and its image file exist, that the image provides every package of the image's Contents
in the Images table, the test framework and the linter listed there, and rmarkdown and Pandoc
when listed, and that each version given there matches. Contents give only the versions that the
methods document fixes; the check tests no other version, since the build resolves them. A
missing entry or image file means the image is missing.

## Setup tests

Write the setup tests in the language of the Input checks section, with its framework. They test
the test support code from the outside, through the files it writes, its exit status, and its
messages, and check that:

- the reference subset script derives each `REF_<NAME>` subset as its Subset rule states and
  keeps the resource's headers;
- the synthetic data generator writes each `INPUT_<NAME>` as Input data, read with
  `{Agents_Folder}/references/analysis-inputs.md`, and its generation rule and planted signal in
  Test data require, and a second run writes byte-identical files;
- the input checks pass on the test inputs and fail, with the expected message, on a temporary
  broken copy of one synthetic input, such as one without a used column;
- the test configuration sets `ANALYSIS_ID`, `ANALYSIS_VERSION` to the implementation plan's
  `Version`, every `INPUT_<NAME>`, `REF_<NAME>`, and global parameter key of Configuration to its
  Test value, and `RESULTS_DIR`, `FIGURES_DIR`, and `REPORTS_DIR` to the `results`, `figures`, and
  `reports` subfolders of `${ANALYSIS_OUTPUT_ROOT}`.

Write second runs and broken copies only in temporary folders, and delete them.

## Test data

Tests use the reference subsets and synthetic data in `{Analysis_Test_Inputs_Folder}`, which the
test support code creates, and never read the user's `INPUT_<NAME>` data.

## Frameworks

Each increment's output checks use the framework of the language profile for the increment's
`Language`, in the increment's image. Name each test file with the increment's two-digit `NN` and
slug in the framework's pattern.

## Check modes

The execution runner, `run-tests.sh`, runs the checks and, for analysis, replaces the
session-level setup of the language profiles. Its `increment <NN>` mode runs the checks of one
increment; its `synthetic [NN]` mode runs the image checks, the setup tests, the input checks,
and the checks of every `synthetic` increment, up to `NN` when given; its `setup` mode runs only
the setup tests; and its `post-run` mode runs only the output checks. It sets
`ANALYSIS_TEST_MODE` to `synthetic` in its `increment` and `synthetic` modes and to `post-run` in
its `post-run` mode; in these rules, `synthetic` mode and `post-run` mode mean that value.

- In `synthetic` mode, checks read the folders defined by the test configuration. In `post-run`
  mode, they load the real configuration and read the version folders written by the user's full
  run, read-only.
- Skip mode-specific checks with an explicit reason: exit status and reproducibility checks run in
  `synthetic` mode only, and checks of `post-run` increments run in `post-run` mode only.

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
