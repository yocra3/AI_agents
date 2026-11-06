# Analysis testing with formal checks

Use these rules for the increments of an analysis plan in every language. Tests check the formal
acceptance criteria of the plan through output files. They never validate experimental results.
Tests, the execution runner, and the test-subset script live in `<tests>`, that is
`{Analysis_Tests_Folder}/<analysis-id>`. Read the increment, its acceptance criteria, and its
verification mode from the plan, and run every command in the plan's container image under the
execution rules in `{Agents_file}`.

## Allowed and forbidden checks

These rules override the skill's general guidance on reference outputs and test doubles.

- Check only formal properties: file existence at the configured path, format and parseability,
  column names and types, row counts relative to an input (for example, one row per sample in the
  samplesheet, read at check time), successful execution, the provenance file and its plan
  version, seed reproducibility, and report rendering and sections.
- Do not use reference outputs or snapshots of values, and do not assert statistics, p-values,
  effect sizes, numbers of significant features, or any other value that depends on the results.
  Do not fix row counts to the test subset's size.
- Test scripts from the outside through their output files; do not call their internal functions
  or inspect their variables, so tests survive refactoring.

## Test subset

Create the test subset in `{Analysis_Test_Data_Folder}/<analysis-id>/` with the tracked
test-subset script, applying the plan's subsetting rule exactly. Read the real inputs without
modifying them. Recreate the subset only in the `test-setup` phase. If the rule cannot be applied,
or a `subset` increment cannot produce meaningful output on the subset, stop and report it instead
of changing the rule.

## Frameworks

Use the framework of the increment's language, and name each test file with the increment's
two-digit `NN` and slug in the framework's pattern. All frameworks share the same execution
runner, which executes once per test session through the framework's session-level setup
mechanism.

## Execution and check modes

Execution and checking are separate. The `ANALYSIS_TEST_MODE` environment variable selects the
mode, and the same checks run in both.

- `subset` (default): the execution runner sets `ANALYSIS_CONFIG` to the test configuration and
  `ANALYSIS_OUTPUT_ROOT` to `<tests>/results/subset/`, emptied before each run. It runs the
  scripts and render scripts of the `subset` increments in plan order, up to the increment under
  test, records each exit status, and stops at the first failure. Checks then read the folders
  defined by the test configuration. Nothing is written to the versioned folders or to tracked
  files.
- `post-run`: nothing is executed. Checks load the real configuration and read the `vN` folders
  written by the user's full run, read-only.
- Skip mode-specific checks with an explicit reason: exit status and reproducibility checks run in
  `subset` mode only, and checks of `post-run` increments run in `post-run` mode only. In
  `post-run` mode, a script's provenance file shows that it completed.
- Report the exact test commands for both modes.

## Phases

- `test-setup`: create or regenerate the test subset, the test configuration, and the runner.
  After `coder: renumber`, also rename the test files of renumbered increments to their new `NN`
  and update the script names they call and the runner's script list. Confirm that the subset
  follows the plan's rule, that `test.conf` declares every required key with `PLAN_VERSION` set to
  the plan version, and that the runner starts in the container. It has no RED.
- `subset-test`: write the checks for the increment. RED is valid only when the increment's checks fail
  because its outputs are missing or malformed, including because its script does not exist yet,
  while the subset, configuration, runner, container, framework, and earlier increments work.
  For a modified increment whose acceptance criteria are unchanged, report that the existing checks
  still apply instead of RED.
- `post-run-checks`: write checks that run only in `post-run` mode. Confirm that they load and are
  skipped in `subset` mode. Do not attempt RED or run the increment's script.
- `remove-tests`: remove the tests of removed criteria or increments. Then confirm GREEN, as
  defined below, for the remaining `subset` increments whose phases are complete. Skip this
  confirmation while a Setup phase is pending, because the subset and configurations are not yet
  current.
- GREEN means every check of the current and earlier `subset` increments passes in `subset` mode.

## Reports

- Render each report through its render script in `subset` mode. Check the exit status, that the
  rendered file exists in the configured reports folder, and that its headings contain the sections
  specified by the plan, in order.
- Check that rendering creates or modifies no file in the results or figures folders, by comparing
  their file listings and checksums before and after rendering.
- Do not assert values shown in tables or figures, or computed by the report.

## Reproducibility

When a criterion requires it, run the execution a second time with `ANALYSIS_OUTPUT_ROOT` set to
`<tests>/results/rerun/` and compare the result files of both runs byte for byte. Exclude figures
and rendered reports, whose metadata may embed timestamps, unless the plan requires them.
