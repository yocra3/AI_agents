# Analysis validation

Use these rules for the `full-validation` phase of the implementation plan of an analysis methods
document, `{Plans_Folder}/<analysis-id>.plan.md` for `{Analysis_Methods_file}`. Take every path
and file name from the Analysis layout keys in `{Agents_file}`, resolved for the analysis, and
read each increment's `Image` ID and `Language`, and the image and language of the input checks,
from the implementation plan.

## Suite

Run the execution runner in `{Analysis_Test_Code_Folder}` in its default `synthetic` mode, over
every `synthetic` increment from the first. This mode also runs the permanent image checks and
the input checks on the synthetic inputs. Do not run `post-run` checks, the runner's
`input-check` mode, or any other check on the real inputs, and never execute `run-analysis.sh`.

## Lint environments

Lint each in-scope file under the execution rules in `{Agents_file}`:

- each script and report source in its increment's image, the `{Analysis_Images_file}` entry
  named by its `Image` ID in the implementation plan;
- each test file in the image of the increment it tests;
- each `{Analysis_Shared_Functions_file}` in the image of any increment of its language;
- the input checks, the synthetic data generator, and the reference subset script in the image
  of the input checks;
- the execution runner, the image checks, and `run-analysis.sh` on the host or in any image that
  provides the lint checks of their language.

## Report

Also report the result of the image checks, of the input checks, and of each increment's checks,
and the increment or check of every failure.
