# Nextflow implementation planning

Plan the Nextflow code that a specification changes, in the sections that its case, decided in
step 2 of planning-specs, applies. Resolve the design, concrete test fixtures, required
companions, derived test prerequisites, any reference generation, and ordered implementation
phases before implementation begins.

## Every Nextflow change

For every component or wiring that the specification changes or adds, define its implementation
phases in dependency order: the default phases of the plan template, unless New processing or
Reference implementation assigns others.

Record each of them, and each component that New processing reuses, in Component design with
one classification:

- `modify-local`: an internal change to an existing local component, which adds no new
  processing;
- `local-wiring`: local wiring, channels, configuration, or parameters that consume components;
- `reuse-local`, `import-nf-core`, or `new`: only for new processing, as New processing decides.

For each local executable component or local wiring that requires functional testing, resolve:

- concrete input fixtures;
- companions actually required by the selected component interface;
- derived test prerequisites required only to execute the test;
- the production test boundary and required verification evidence.

Do not prescribe test harnesses, helper scripts, snapshot/projection mechanics, or phase-internal
code structure in the plan. The responsible tester or coder chooses those mechanisms according to
its applicable profile and repository conventions.

A derived test prerequisite is test infrastructure produced from another fixture, such as an
index derived from a reference FASTA. It is not a product input unless the functional contract
explicitly makes it one.

Preserve any exact fixture or source constraint explicitly required by the specification.
Otherwise resolve the smallest compatible concrete fixtures according to
[test-data discovery](../test-data.md), with, for new processing, the test evidence that
`nfcore-component-reuse` reports.

## New processing

Use the `nfcore-component-reuse` skill for the requirements of the new processing only, and design
the final Nextflow structure from its result: the subworkflows, individual modules, channel
shapes, metadata, file formats, intermediate artifacts and dependencies that the functional
contract requires. Classify each component as Every Nextflow change lists, with that analysis as
evidence; a `new-required` gap that the selected composition does not eliminate becomes a `new`
local module or subworkflow. For each `new` component, record the closest existing candidate and
why its interface, supported configuration, aliasing, or composition cannot provide the behavior
without changing its implementation or breaking the contract of existing consumers.

Order the phases by dependency: reused or imported components before the new components that
consume them, and new modules before dependent subworkflows and higher-level local wiring.

For `reuse-local`, record the existing path and public interface, and plan no implementation phase
when the component is consumed unchanged; represent any new consuming behavior separately as
`local-wiring`.

For `import-nf-core`, plan one `coder: import-nf-core` phase, which uses `importing-nf-core`, and no
local TDD cycle or cleaner phase for the imported component. Record the exact component type,
remote name and pinned `nf-core/modules` commit SHA, and preserve the component's declared
containers. Add the exact pipeline root to the plan so `importing-nf-core` can execute without
inferring it.

For every reference command and new executable component, record an exact, architecture-compatible
container and an Apptainer-compatible URI. Prefer an immutable image from
`community.wave.seqera.io`; otherwise prefer a compatible BioContainers image. Use another source
only with a recorded justification. Never select `latest`; record the image digest or stable hash,
software version, Apptainer invocation, and required bind mounts.

## Reference implementation

Only for a new component that requires reference outputs. Resolve `{Nextflow_Reference_Folder}`
from `{Agents_file}`, and also resolve:

- the required reference outputs and the constraints ensuring their independence from
  production;
- the properties that must be validated for those reference outputs.

The reference method may use an existing tool or upstream component command, or an independent
Bash/Python implementation. It must not invoke, translate, or reuse the production implementation
that the later test will exercise.

Declare the component's phases in this order:

1. `tester: reference-validation`
2. `coder: reference-generation`
3. `tester: test`
4. `coder: implementation`
5. `cleaner: refactor`

`{Agents_Folder}/references/phases/nextflow.md` defines the first two, and the Nextflow rules
that the last three follow in such a step.

Reference generation and validation scripts and the generated reference data belong in
`{Nextflow_Reference_Folder}`. Record provenance, checksums, containers, commands and
reproduction information required to recreate the artifacts from an empty workspace.
