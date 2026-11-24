# Nextflow phases

Nextflow-only phases of the Steps of a specification implementation plan, as planning-specs
assigns them, and the Nextflow rules of some other phases. The rules for every phase of
[specs.md](specs.md) also apply to them.

## `coder: import-nf-core`

- **Meaning**: Import the step's nf-core component with nf-core tools.
- **Skill**: importing-nf-core.
- **Steps**:
  1. Import the component with importing-nf-core, with the component type, remote name, and
     pinned `nf-core/modules` commit SHA of the implementation plan's Component design and the
     pipeline root of its header. Write no local tests or wiring.
- **Evidence**: the skill's report.
- **Stops**: the skill's stops.

## `tester: reference-validation`

- **Meaning**: Write the validations of the reference outputs before they exist, in RED.
- **Skill**: testing-unit.
- **Steps**:
  1. Verify that the resolved reference inputs are usable.
  2. Write executable validations of the reference outputs from the input, prerequisite, output,
     and validation contracts of the implementation plan.
  3. Run them and confirm RED. Do not generate the reference outputs, create production nf-tests,
     or create snapshots.
  4. Lint the changed test files with the linting skill and fix findings in them.
- **Evidence**: the validations written, the exact commands and results, the expected failure
  reason, and the lint results.
- **Stops**: missing source data, runtime dependencies, or required tools; they are environment
  failures, not valid RED.

## `coder: reference-generation`

- **Meaning**: Generate the test prerequisites and reference outputs until their validations are
  GREEN.
- **Skill**: writing-code, with its Nextflow reference implementation profile.
- **Steps**:
  1. Run tester's validations from the brief and confirm the expected RED.
  2. Write the generation scripts and produce every concrete input, companion file, test
     prerequisite, and reference output that the implementation plan requires, independently of
     the production component.
  3. Run the validations until GREEN. Every command that exercises the reference behavior uses
     the same image, `apptainer exec --cleanenv` invocation, and bind mounts as the RED run; the
     harness may run on the host.
  4. Lint the generation scripts with the linting skill and fix findings in them.
  This phase does not implement the production component or advance the specification to
  `Coded`.
- **Evidence**: the paths and checksums of the generated files, the commands, the validation
  results, and the lint results.
- **Stops**: a validation is invalid or contradicts the specification; never change it.

## Nextflow rules of other phases

Each of these rules follows the entry of its phase, in a step that has
`tester: reference-validation`.

### `tester: test`

- Confirm that the step's reference validations are GREEN before writing tests; stop when they
  are not.
- Write or extend the production nf-tests, with every expectation and snapshot derived from the
  verified reference outputs before the production implementation. Defer no snapshot until after
  GREEN.
- Run them with `nf-test test <test-path> --ci` and the repository options. Missing snapshots,
  invalid fixtures, and unavailable dependencies are not valid RED.
- Also return the snapshots written.

### `coder: implementation`

- Implement the production component. Run the nf-tests with `--ci`, never with
  `--update-snapshot`.
- Never change a snapshot or a reference implementation; stop when a snapshot is invalid or
  contradicts the specification.

### `cleaner: refactor`

- Refactor only the production component. Never change tests, snapshots, reference
  implementations, or generated fixtures.
- Run the nf-tests with `--ci`, never with `--update-snapshot`.
