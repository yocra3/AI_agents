# Specification plan phases

Phases of the Steps of a specification implementation plan that only specification plans use;
`tester: test`, `coder: implementation`, and the Removed and Finalization phases are in
[common.md](common.md), and the Nextflow-only phases in [nextflow.md](nextflow.md).

## Rules for every phase

These rules apply to every phase of `tester`, `coder`, and `cleaner` in a specification
implementation plan, including `<agent>: validation-fix`.

- When the phase acts on a step, read the step, its tasks, `Depends on`, and the acceptance
  criteria mapped to it from the implementation plan, and their requirements from the
  specification.
- Use the test data of the implementation plan's Test data and artifacts, and run tests and
  tools in the environment and containers of its Environment and reproducibility section.
- Never edit an imported nf-core component. When an error is traced to one, such as a test that
  fails because of it, stop and report it; the user decides how to resolve it, such as with
  another version or a patch.

## `cleaner: refactor`

- **Meaning**: Refactor the step's code without changing its behavior.
- **Skill**: writing-code.
- **Steps**:
  1. Run the step's targeted tests and confirm GREEN before changing code.
  2. Refactor only the production code that the step changed, and only where a concrete
     readability, consistency, maintainability, or duplication problem exists. Otherwise change
     nothing.
  3. Run the targeted tests after each refactoring change, and the relevant fast suite before
     returning.
  4. Lint the changed files with the linting skill and fix findings in them.
- **Evidence**: the changed files, the refactoring decisions, the GREEN commands and results, and
  the lint results, or a no-change result with its reason.
- **Stops**: the step's tests are not GREEN before refactoring.

## `coder: direct-implementation`

- **Meaning**: Make the step's planned change without RED, because no test can observe it.
- **Skill**: writing-code.
- **Steps**:
  1. Make only the step's planned change.
  2. Run the relevant fast suite.
  3. Lint the changed files with the linting skill and fix findings in them.
- **Evidence**: the changed files, and the suite and lint commands and results.
- **Stops**: the change needs behavior that a test can observe.
