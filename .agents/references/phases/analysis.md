# Analysis plan phases

Phases of the implementation plan of an analysis methods document, in execution order, and the
analysis rules of the phases of [common.md](common.md) that analysis plans use.

## Rules for every phase

These rules apply to every phase of `tester`, `coder`, and `cleaner` in an analysis
implementation plan, including `<agent>: validation-fix`.

- Read the increment, its `Files`, `Image`, `Language`, methods steps, and acceptance criteria,
  and the language and image of the Input checks section, from the implementation plan. Take
  every path and file name from the Analysis layout keys in `{Agents_file}`, resolved for the
  analysis.
- Run every command under the execution rules in `{Agents_file}`: an increment's scripts and
  checks in its image, the `{Analysis_Images_file}` entry named by its `Image` ID; the reference
  subset script, the synthetic data generator, the input checks, and the setup tests in the image
  of the input checks; the execution runner (`run-tests.sh` in `{Analysis_Test_Code_Folder}`) and
  the image checks on the host.
- Lint each file under the same execution rules: each script and report source in its
  increment's image; each test file in the image of the increment it tests, and the setup tests
  in the image of the input checks; each `{Analysis_Shared_Functions_file}` in the image of any
  increment of its language; the input checks, the synthetic data generator, and the reference
  subset script in the image of the input checks; `run-tests.sh`, the image checks, and
  `run-analysis.sh` on the host or in any image that provides the lint checks of their language.
- An increment is GREEN when `run-tests.sh increment <NN>` passes: the increment's scripts run
  and its checks pass, reusing the earlier increments' outputs in `{Analysis_Test_Run_Folder}`.
  When it fails, run `run-tests.sh synthetic <NN>` to locate the error; handle missing or stale
  earlier outputs in no other way.
- The full run, `run-tests.sh synthetic` without `NN`, empties `{Analysis_Test_Run_Folder}` and
  runs the image checks, the setup tests, the input checks, and every `synthetic` increment with
  its checks. Only `cleaner: analysis-refactor` and `coder: full-validation` use it; otherwise
  the image checks, the setup tests, and the input checks run only in their Setup phases and
  when `run-tests.sh synthetic <NN>` locates an error.
- The test support code is the test configuration, `run-tests.sh`, the reference subset script,
  the synthetic data generator, and the input checks. Once `coder: test-setup` is GREEN, it is
  frozen: only a Setup phase changes it, and an `<agent>: validation-fix` may fix lint findings
  in it without changing its behavior. When another phase needs to change it, or it fails
  functionally, stop and report it; the change needs an `engineer: replanning` that resets
  `tester: test-setup` and `coder: test-setup`, and also `tester: real-input-check` when the
  change affects the input checks.
- Read or run nothing on the user's real inputs, except as `tester: real-input-check` defines.

## `coder: renumber`

- **Meaning**: Rename the files of renumbered increments to their new `NN`.
- **Skill**: none.
- **Steps**:
  1. In one pass, rename the computation scripts, render scripts, and `.Rmd` sources of
     renumbered increments to their new `NN` with plain `mv`, in a collision-free order, such as
     highest number first or through temporary names.
  2. Update every hardcoded reference to the old names, such as the `.Rmd` path in render
     scripts, the provenance file name and `script` row, header `Usage:` paths, and calls or
     sources between scripts, so that provenance file names follow the script's `NN`.
  3. Change nothing else, run nothing in an image, and use no Git commands.
- **Evidence**: each rename, with its old and new name, and the references updated.
- **Stops**: none of its own.

## `tester: image-check`

- **Meaning**: Write the permanent check of one tier-4 image, in RED.
- **Skill**: testing-unit.
- **Steps**:
  1. Write the image check of the image that the marker names, as testing-unit's analysis
     profile defines it.
  2. Run it. RED is valid only when the image is missing or lacks a required package; any other
     failure, such as a syntax error or a missing host tool, is not. When the image already exists
     and passes, report that instead of RED.
  3. Lint the image check with the linting skill and fix findings in it.
- **Evidence**: the image check's path, its command and result, and the RED reason, or that the
  image already passes.
- **Stops**: a failure that is not valid RED.

## `coder: image-build`

- **Meaning**: Write the image's recipe, build it, and add its registry entry, to GREEN.
- **Skill**: building-container-images.
- **Steps**:
  1. Run tester's image check from the brief and confirm the expected RED. When tester reported
     that the image already exists and passes, change nothing and report it.
  2. Build the image that the marker names with building-container-images, which ends with the
     image check passing.
- **Evidence**: the skill's output.
- **Stops**: the skill's stops.

## `engineer: software-versions`

- **Meaning**: Fill the software versions and effective parameters of the tier-4 images.
- **Skill**: planning-analysis, in its Software versions mode.
- **Steps**:
  1. Fill only `Version` and `Effective parameters` of the Software and effective parameters
     rows marked `pending image-build`, from the Contents of each tier-4 image's entry in
     `{Analysis_Images_file}` and the documentation of those versions.
  2. Change nothing else in the implementation plan, and reset no markers.
- **Evidence**: the rows filled, with each version and the documentation used.
- **Stops**: the documentation of a version is unavailable, or a tier-4 image has no registry
  entry.

## `tester: test-setup`

- **Meaning**: Write the setup tests of the test support code, in RED.
- **Skill**: testing-unit.
- **Steps**:
  1. After `coder: renumber`, rename the test files of renumbered increments to their new `NN`
     and update the script names they call.
  2. Write or update the setup tests that testing-unit's analysis profile defines.
  3. Run them with the framework of the input checks' language and confirm RED. RED is valid only
     when they fail because the test support code or the test inputs are missing or do not meet
     the implementation plan; syntax, framework, and image errors are not.
  4. Lint the changed test files with the linting skill and fix findings in them.
- **Evidence**: the setup tests and renamed files, the exact commands and results, and the
  expected failure reason.
- **Stops**: a rule of Input data, Configuration, or Test data cannot be checked as written.

## `coder: test-setup`

- **Meaning**: Write the test support code and create the test inputs, to GREEN.
- **Skill**: coding-spec.
- **Steps**:
  1. Run tester's setup tests from the brief and confirm the expected RED.
  2. Write or rewrite the reference subset script, the synthetic data generator, the input
     checks, the test configuration, and `run-tests.sh`, as coding-spec's analysis profile defines
     them. After `coder: renumber`, also update the script list of `run-tests.sh`.
  3. Create the test inputs in `{Analysis_Test_Inputs_Folder}` with the reference subset script
     and the synthetic data generator.
  4. Run the setup tests with `run-tests.sh setup` until GREEN.
  5. Lint the changed files with the linting skill and fix findings in them.
- **Evidence**: the files written, the test inputs created, the exact commands and results, and
  the lint results.
- **Stops**: a Test data rule cannot be applied; a reference resource is not at its Location,
  naming the missing file; or a setup test is invalid or contradicts the implementation plan;
  never change the test.

## `coder: real-config`

- **Meaning**: Write the real configuration from Configuration.
- **Skill**: coding-spec.
- **Steps**:
  1. Write `{Analysis_Real_Config_file}` with `ANALYSIS_ID`, `ANALYSIS_VERSION` set to the
     implementation plan's `Version`, the output folders set to the version folders of the
     Analysis layout, and every `INPUT_<NAME>`, `REF_<NAME>`, and global parameter key of
     Configuration with its Real value.
  2. Verify that every required key is set. Do not read the inputs or run anything in an image.
- **Evidence**: the file path and the keys set.
- **Stops**: a key of Configuration has no Real value.

## `tester: real-input-check`

- **Meaning**: Run the input checks on the real inputs.
- **Skill**: none.
- **Steps**:
  1. Run `run-tests.sh input-check`.
  2. Do not read or print the real inputs in any other way, and do not change the inputs or the
     checks to make them pass.
- **Evidence**: the command and its result, with the failure messages only.
- **Stops**: any input check fails.

## `tester: post-run-checks`

- **Meaning**: Write checks that run only after the user's full run.
- **Skill**: testing-unit.
- **Steps**:
  1. Write the increment's output checks, as testing-unit's analysis profile defines them, to run
     only in the `post-run` mode of `run-tests.sh`.
  2. Run `run-tests.sh increment <NN>`, which runs no script of a `post-run` increment, and
     confirm that the checks load and are skipped. Do not attempt RED or run the increment's
     script.
  3. Lint the changed test files with the linting skill and fix findings in them.
- **Evidence**: the checks written, and the command and result that show them skipped.
- **Stops**: none of its own.

## `coder: post-run-implementation`

- **Meaning**: Implement the increment, validated with lint and syntax checks only.
- **Skill**: coding-spec.
- **Steps**:
  1. Implement exactly the increment's methods steps.
  2. Lint the changed files with the linting skill, including its syntax checks, and fix findings
     in them. Never run the script.
- **Evidence**: the changed files and the lint results.
- **Stops**: a method cannot be applied as the methods document states it, or a required tool is
  missing from the image.

## `cleaner: analysis-refactor`

- **Meaning**: Refactor all analysis code once.
- **Skill**: coding-spec.
- **Steps**:
  1. Run the full run, `run-tests.sh synthetic`, and confirm GREEN before changing code.
  2. Refactor the computation scripts, render scripts, report sources, and shared functions of
     every increment, as their `Files` list them, only where a concrete readability,
     consistency, maintainability, or duplication problem exists. Shared functions may move to
     `{Analysis_Shared_Functions_file}`.
  3. Preserve behavior: the same outputs, file names, provenance, seeds, and configuration keys,
     and every script still runnable line by line. Do not modify the real configuration, the
     tests, the test support code, the test inputs, the image recipes, or `run-analysis.sh`.
  4. Run the full run again and confirm GREEN, validating `post-run` increments with lint and
     syntax checks only, and lint the changed files with the linting skill, fixing findings in
     them.
- **Evidence**: the changed files, the refactoring decisions, the GREEN commands and results, and
  the lint results, or a no-change result with its reason.
- **Stops**: the full run fails before refactoring.

## `coder: run-script`

- **Meaning**: Write `run-analysis.sh`.
- **Skill**: coding-spec.
- **Steps**:
  1. Write or rewrite `run-analysis.sh` as coding-spec's analysis profile defines it.
  2. Lint it with the linting skill and fix findings in it. Never execute it.
- **Evidence**: the file and the lint results.
- **Stops**: none of its own.

## `dev_ops: code-documentation`

- **Meaning**: Add comments to the analysis code.
- **Skill**: documenting-code.
- **Steps**:
  1. Document the scripts, shared functions, and report sources of the implementation plan, as
     documenting-code's analysis profile defines it.
  2. Check that every added or removed line in the diff is blank, a full-line comment starting
     with `#` after indentation, or part of an HTML comment in a `.Rmd` file, and that every
     shebang is unchanged.
  3. Lint each changed file with the linting skill; fix findings only in comments.
- **Evidence**: the documented files, the diff check, and the lint results.
- **Stops**: the documentation or a lint finding needs a change other than comments.

## Analysis rules of common phases

Each of these rules follows the entry of its phase in [common.md](common.md).

### `tester: remove-tests`

- Do not confirm GREEN. An increment is removed only at a new version, which leaves
  `tester: test-setup` pending, so the test inputs and configuration are not yet current; the
  full run of `coder: full-validation` covers the remaining increments.

### `tester: test`

- Write only the output checks of the increment's acceptance criteria and Expected outputs, as
  testing-unit's analysis profile defines them.
- Run the checks with `run-tests.sh increment <NN>`, for the baseline when the increment already
  has checks, and for RED. When it fails for a reason other than valid RED, run
  `run-tests.sh synthetic <NN>` to locate the error.
- RED is valid only when the increment's checks fail because its outputs are missing or
  malformed, including because its script does not exist yet, while the test inputs, the
  configuration, `run-tests.sh`, the images, the framework, and the earlier increments' outputs
  work.
- For a modified increment whose acceptance criteria are unchanged, report that the existing
  checks still apply instead of RED; it is not a stop.
- Stop on any failure that is not valid RED.

### `coder: implementation`

- When tester reported that the existing checks still apply, proceed without RED.
- Implement exactly the increment's methods steps, which the formal checks do not bound, not
  only the minimum change that turns them GREEN.
- The targeted tests and the relevant fast suite are `run-tests.sh increment <NN>`. When it
  fails, run `run-tests.sh synthetic <NN>` to locate the error.
- Stop when a method cannot be applied as the methods document states it, a required tool is
  missing from the image, or the increment cannot produce non-empty outputs from the test inputs.

### `coder: full-validation`

- The complete test suite is the full run, `run-tests.sh synthetic` without `NN`. Never run the
  `post-run` or `input-check` modes of `run-tests.sh`, anything on the real inputs, or
  `run-analysis.sh`.
- Also report the result of the image checks, the setup tests, the input checks, and each
  increment's checks, and the increment or check of every failure.
