# Nextflow component testing with nf-test

Use this profile with the applicable nf-core testing conventions. Resolve paths, required plugins
and execution profiles from the repository.

## Reference validations

Validations of reference outputs use the input, prerequisite, output and validation contracts
resolved by the plan.

Validate declared filenames, provenance where relevant, formats, cardinality, metadata associations, semantic properties, tolerances, failure behavior and reproducibility. A successful command or nonempty file is insufficient when content is specified.

The test harness may run on the host, but commands exercising reference behavior must use the exact execution environment pinned by the plan. Do not fall back to undeclared host tools.

## Production nf-tests

Use process tests for new local modules and workflow tests for local subworkflows or wiring. Create missing tests or extend existing coverage; preserve unrelated coverage. Stub tests verify declared outputs and wiring but do not replace real functional tests.

Test inputs required by the final nf-test must be reproducibly available from a clean checkout.
Use exact snapshots for stable results and nf-test-native assertions or projections for
properties, formats, cardinality, metadata association and numerical tolerances.

The final production test exercises only the production component and its normal test inputs.
It does not materialize or read reference outputs or oracle artifacts, or execute
reference-generation, oracle-validation or projection helper scripts. Persist expected results
only through the normal `.nf.test.snap` file and explicit assertions in the `.nf.test`.

For module nf-tests, follow [module testing guidelines](./nf-core/testing_modules.md).

For subworkflow nf-tests, follow [subworkflow testing guidelines](./nf-core/testing_subworkflows.md).

## References

- [nf-test snapshots](https://www.nf-test.com/docs/assertions/snapshots/)
- [nf-test comparison mode](https://www.nf-test.com/docs/cli/test/#--ci)
