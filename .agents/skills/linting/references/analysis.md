# Analysis lint environments

Where each file of the implementation plan of an analysis methods document is linted. Run each
check under the container execution rules in `{Agents_file}`, in the images of the
implementation plan, as their `{Analysis_Images_file}` entries define them: an increment's image
is the entry named by its `Image` ID, and the image of the input checks is the one of the Input
checks section.

- Each script and report source: in its increment's image.
- Each test file: in the image of the increment it tests; the setup tests in the image of the
  input checks.
- Each `{Analysis_Shared_Functions_file}`: in the image of any increment of its language.
- The input checks, the synthetic data generator, and the reference subset script: in the image
  of the input checks.
- `run-tests.sh`, the image checks, and `run-analysis.sh`: on the host or in any image that
  provides the lint checks of their language.
