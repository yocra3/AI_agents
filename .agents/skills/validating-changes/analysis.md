# Analysis validation

Use these rules for the `full-validation` phase of an analysis plan in `{Analysis_Plans_Folder}`.
Take every path and file name from the Analysis layout keys in `{Agents_file}`, resolved for the
plan's analysis, and read each increment's `Image` ID and `Language` from the plan.

## Suite

Run the execution runner in `{Analysis_Test_Code_Folder}` in its default `subset` mode, over
every `subset` increment from the first. Do not run `post-run` checks. Never execute
`run-analysis.sh`.

## Lint environments

Lint each in-scope file under the execution rules in `{Agents_file}`:

- each script and report source in its increment's image, the `{Analysis_Images_file}` entry
  named by its `Image` ID in the plan;
- each test file in the image of the increment it tests;
- each `{Analysis_Shared_Functions_file}` in the image of any increment of its language;
- the execution runner, the test-subset script, and `run-analysis.sh` on the host or in any image
  that provides the lint checks of their language.

## Report

Also report the result of each increment's checks and the increment of every failure.
