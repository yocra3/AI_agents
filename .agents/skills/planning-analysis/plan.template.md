# Analysis implementation plan template

Use this template for `{Plans_Folder}/<analysis-id>.plan.md`, the single implementation plan of
the methods document `{Analysis_Methods_file}` with the same `<analysis-id>`, `analysis-<slug>`.
`engineer` owns the content; `implementation_coordinator` changes only the execution markers.
Write acceptance criteria with the EARS guide in
`{Agents_Folder}/skills/generating-specs/EARS.md`.

```markdown
# Implementation plan: <analysis-id>

- **Methods document**: `<resolved {Analysis_Methods_file}>`
- **Version**: `vN`
- **Approval commit**: `<hash>` `docs(<analysis-id>): approve methods vN`

## Software and effective parameters

| Package | Version | Image | Digest | Effective parameters | Steps |
| --- | --- | --- | --- | --- | --- |
| `<package>` | `<resolved version>` | `<image ID>` | `<sha256:...>, or registry` | `<name = value for each key parameter that the document does not fix, or none>` | `<M1, M2, or report increment>` |

## Images

| ID | Tier | Image | Contents | Used by |
| --- | --- | --- | --- | --- |
| `<ID>` | `<1 registry, 2 BioContainers, 3 Seqera Containers, or 4 recipe>` | `<URI, or recipe path for tier 4>` | `<base for tier 4>; <packages with versions>; tests: <framework>; lint: <linter>; <rmarkdown and Pandoc, if present>` | `<increment numbers, input checks>` |

## Configuration

| Key | Meaning | Real value | Test value |
| --- | --- | --- | --- |
| `INPUT_<NAME>` | <input from Input data> | `<Location in the methods document>` | `<synthetic file or folder in {Analysis_Test_Inputs_Folder}>` |
| `REF_<NAME>` | <reference resource from Input data> | `<Location in the methods document>` | `<reference subset in {Analysis_Test_Inputs_Folder}>` |
| `<KEY>` | <global parameter, with its comparison> | `<value in the methods document>` | `<value; when it differs, why>` |

## Input checks

- **Language**: `<R | Python | Bash>`
- **Image**: `<image ID>`

| Input | Technical requirement | Derived from |
| --- | --- | --- |
| `<INPUT_ or REF_ key, with column or field>` | <requirement> | `<step and package::function>` |

## Test data

- **Generator seed**: `<integer>`

| Input | Generation rule | Planted signal |
| --- | --- | --- |
| `INPUT_<NAME>` | <format and structure, distributions, identifiers and their source, design levels and replicates> | <signal that keeps every synthetic step from producing empty outputs, or none> |

| Resource | Subset rule | Source |
| --- | --- | --- |
| `REF_<NAME>` | <deterministic rule, with seed if sampled> | `<real resource at its Location, or nf-core test-datasets path>` |

## Seeds

| Step | Increment | Seed |
| --- | --- | --- |
| `<M3>` | `<n>` | `<integer>` |

## Removed

<!-- One entry per removed increment; leave this section empty in a new plan. -->

### Removed: `<old file>`, `<old file>`

- [ ] `tester: remove-tests`
- [ ] `coder: remove-code`

## Setup

- [x] `coder: renumber`
- [ ] `tester: image-check` (`<tier-4 image ID>`)
- [ ] `coder: image-build` (`<tier-4 image ID>`)
- [ ] `tester: test-setup`
- [ ] `coder: real-config`
- [ ] `tester: real-input-check`

## Increments

### Increment 1: <title>

- **Kind**: `<computation | report>`
- **Language**: `<R | R Markdown | Python | Bash>`
- **Image**: `<image ID>`
- **Verification**: `<synthetic | post-run>`
- **Files**: `<NN>-<slug>.<ext>`
- **Methods**: `<M1, M2, or none>`
- **Results**: `<results from Results to report, or none>`
- **Depends on**: `<increment numbers or none>`
- **Acceptance criteria**: `<AC1, AC2>`
- **Execution**:
  - [ ] `tester: synthetic-test`
  - [ ] `coder: synthetic-implementation`

## Finalization

- [ ] `cleaner: analysis-refactor`
- [ ] `coder: run-script`
- [ ] `coder: full-validation`
- [ ] `reviewer: implementation-review`
- [ ] `dev_ops: code-documentation`

Phase constraints:

- `cleaner: analysis-refactor`: this is the implementation plan's single final refactoring
  phase; shared functions may move to `{Analysis_Shared_Functions_file}`; do not modify the test
  or real configurations, the tests, the input checks, the synthetic data generator, the
  reference subset script, the test inputs, or the image recipes.
- `reviewer: implementation-review`: the methods document is the contract and this
  implementation plan is its implementation plan; check point by point that the code implements
  the methods steps as stated, with the software and images of this plan, and meets the
  acceptance criteria; do not judge whether the methods are appropriate; report missing
  implementation plan items, methods deviations, costly or inferential computation inside a
  report, and interpretive text as blocking, and cheap additions beyond the implementation plan
  as non-blocking; check that `run-analysis.sh` runs the input checks and checks every image it
  uses before the first script, then lists every increment's scripts in `NN` order, each with its
  increment's image. Use the `full-validation` report as evidence.
- `dev_ops: code-documentation`: this phase is declared by the implementation plan and is
  therefore requested; it changes comments only.

## Reports

### Report of increment <n>: <title>

1. `<exact heading>`: <results shown, files read from RESULTS_DIR or FIGURES_DIR, and any simple calculation>
2. `<exact heading>`: <content>

## Expected outputs

| Output | Increment | Folder | File name | Format | Columns and types | Rows | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<name>` | `<n>` | `<RESULTS_DIR, FIGURES_DIR, or REPORTS_DIR>` | `<file>` | `<format>` | `<name: type, ...> or not-applicable` | `<relative to an input, e.g. one per sample in INPUT_METADATA> or not-applicable` | `<result from Results to report, or none>` |

## Acceptance criteria

| ID | Criterion | Increment |
| --- | --- | --- |
| AC1 | `<EARS criterion>` | `<n>` |
```

## Phases

Every marker names its phase as `<agent>: <phase>`. The agents' profiles define how each phase is
done; this table gives its meaning.

| Section | Phase | Meaning |
| --- | --- | --- |
| Removed | `tester: remove-tests` | Remove the tests of the removed increment. |
| Removed | `coder: remove-code` | Delete the files that the Removed entry lists. |
| Setup | `coder: renumber` | Rename the files of renumbered increments to their new `NN`. |
| Setup | `tester: image-check` | Write the permanent check of one tier-4 image, in RED. |
| Setup | `coder: image-build` | Write the image's recipe, build it, and add its registry entry (GREEN). |
| Setup | `tester: test-setup` | Write the reference subsets, the synthetic data generator, the input checks, the test configuration, and the runner. |
| Setup | `coder: real-config` | Write the real configuration from Configuration. |
| Setup | `tester: real-input-check` | Run the input checks on the real inputs. |
| Increments | `tester: synthetic-test` | Write the increment's checks and confirm RED on synthetic data. |
| Increments | `coder: synthetic-implementation` | Implement the increment and reach GREEN on synthetic data. |
| Increments | `tester: post-run-checks` | Write checks that run only after the user's full run. |
| Increments | `coder: post-run-implementation` | Implement the increment, validated with lint and syntax checks only. |
| Finalization | `cleaner: analysis-refactor` | Refactor all analysis code once. |
| Finalization | `coder: run-script` | Write `run-analysis.sh`. |
| Finalization | `coder: full-validation` | Run the complete test suite and lint every changed file. |
| Finalization | `reviewer: implementation-review` | Review the implementation against the methods document and this plan. |
| Finalization | `dev_ops: code-documentation` | Add comments to the analysis code. |

## Content rules

- The implementation plan holds the engineering decisions only. Every scientific decision comes
  from the methods document; never add, choose, or change one here.
- The plan defines only what is specific to the analysis. Folders, file locations, configuration
  files, and provenance come from the Analysis layout in `{Agents_file}`; standard configuration
  keys, such as `ANALYSIS_ID`, `ANALYSIS_VERSION`, `RESULTS_DIR`, `FIGURES_DIR`, and
  `REPORTS_DIR`, come from the coding profile.
- `Version` always equals the methods document's `Version`. `Approval commit` is the approval
  commit the plan was last planned from.
- The plan has no change markers; its history is in Git.

## Software and effective parameters

- One row per package that a methods step or a report uses, with the version resolved once, at
  planning, in the tier order below, and the image that provides it.
- Tier order: (1) the project registry, (2) BioContainers, (3) Seqera Containers, (4) a recipe.
  A registry image that already has the package wins even without its latest version, unless the
  methods document fixes another version. A new image, of tiers 2 to 4, uses the latest version
  available, or the version that the document fixes.
- Digest is the image's digest for tiers 1 to 3, and `registry` for tier 4: `coder` records it in
  `{Analysis_Images_file}` under the image ID at `coder: image-build`.
- Effective parameters lists, for each step, the values that the resolved version uses for the
  key parameters that the document leaves at their defaults, meaning those that can change the
  results, such as thresholds, test or fit types, filtering, and normalization. Take them from
  the documentation of that version. They record defaults and are never decisions.
- The table is the source for the manuscript. It is never copied into the methods document.

## Images

- Every increment and the input checks run in exactly one image of the Images table. An image
  provides the tools of every increment that names it and, for their language, the test framework
  and the linter. The image of a report increment also provides rmarkdown and Pandoc. The image
  of the input checks provides the tools that read each input format, such as `samtools` for BAM
  headers.
- Each image has an ID made of a short name and a version, such as `r-deseq2-v1`. Tier-1 images
  keep their registry ID. Tier-2 and tier-3 images have a registry entry, with their digest, when
  the plan is written. A tier-4 image's Image is its recipe path in `{Analysis_Recipes_Folder}`,
  its Contents give the base image and every package with its version, and it has one
  `tester: image-check` and `coder: image-build` pair in Setup.

## Configuration

- One row per `INPUT_<NAME>` and `REF_<NAME>` key of Input data, with the same key and its
  Location as Real value. Test values point to the synthetic inputs and reference subsets in
  `{Analysis_Test_Inputs_Folder}`.
- One row per global parameter of the methods document, with its value as Real value. The Test
  value equals the Real value unless the synthetic data require another one; then Test value
  states why.

## Input checks

- Input checks check the Input data of the methods document: every used column or field with its
  type and constraints, the design variables with their levels, reference level, and minimum
  replicates, the relations between inputs, the files that a manifest lists, and the existence,
  version, and assembly of every reference resource, read from its headers when its format
  carries them. They also check every technical requirement of this section.
- A technical requirement is what a step's functions require of an input that Input data does
  not state, such as integer counts for `DESeq2::DESeqDataSetFromMatrix`, a sorted and indexed
  BAM, or the same chromosome naming in two inputs. Derive it only from what the functions
  require.
- In large formats, such as BAM, CRAM, FASTQ, VCF, and BCF, check the header and the relations
  with other inputs; check the full content only of tables and matrices.
- A failure message states which check failed, in which column or field, and how many times,
  never a value.
- The input checks run on the synthetic inputs in every test run, which checks the generator; on
  the real inputs in `tester: real-input-check`; and at the start of every `run-analysis.sh` run.

## Test data

- Tests use synthetic data instead of the user's data and real reference resources reduced to a
  subset. They never use the user's real data.
- Synthetic inputs: one rule per `INPUT_<NAME>` key. The data have the format, compression, and
  structure of Input data and are plausible: reasonable distributions, real identifiers taken
  from the reference subsets, such as gene IDs from the annotation subset, every level of each
  design variable with its reference level and at least its minimum replicates, and every
  relation between inputs. `tester` writes the generator in `tester: test-setup` as a versioned,
  deterministic script with the Generator seed.
- Planted signal: enough signal that no `synthetic` step produces empty outputs, for example a
  set of features with a large difference between the levels of each comparison. It is not a
  scientific decision: tests never check values.
- Reference subsets: one rule per `REF_<NAME>` key that derives a small, deterministic subset of
  the real resource at its Location, such as one chromosome, or the nf-core test-datasets of that
  resource when they exist. `tester` creates them in `tester: test-setup` and stops, naming the
  missing file, when the resource is not at its Location.
- The generator, the reference subset script, and the input checks run in the image of the input
  checks.

## Seeds

- One row per methods step with a random component, and the generator seed in Test data. The
  methods document never holds seeds.

## Increments

- Each increment produces one computation script or one report. `Files` lists file names only;
  their folders come from `{Analysis_Script_file}` and `{Analysis_Report_Source_file}`. A report
  increment's files are its `.Rmd` source and its render script, with the same `NN` and slug.
- `NN` in a file name is the increment number, two digits zero-padded (`01`, `02`, ...), and also
  the execution order: the user runs the scripts in `NN` order. An increment may depend only on
  earlier increments.
- A computation increment implements the methods steps in `Methods`, or has `Methods: none` when
  it only saves figures of Results to report from existing results. Every methods step belongs
  to exactly one computation increment, in execution order. A report increment has
  `Methods: none`.
- `Results` lists the results of Results to report that the increment produces as an output file
  or a report section. Every result is produced by at least one increment.
- Use `synthetic` unless a step cannot run on synthetic data even with planted signal, for
  example an external tool that needs full references or large resources. A `synthetic`
  increment must not depend on a `post-run` increment; declare such an increment `post-run` too.
- Execution per increment:
  - `synthetic`: `tester: synthetic-test`, then `coder: synthetic-implementation`.
  - `post-run`: `tester: post-run-checks`, then `coder: post-run-implementation`.

## Reports

- `engineer` decides from Results to report how many reports there are, how each is structured,
  and which sections it has. Each report is one report increment with one entry here: a numbered
  list, in order, where each item is the exact section heading followed by its content.
- Reports read only files in `RESULTS_DIR` and `FIGURES_DIR`. They may compute only simple
  calculations, descriptive and deterministic on existing results, such as counts, proportions,
  means, or the first N, and may draw figures inline. Anything inferential or model based, such
  as a test, p-values, a fit, or clustering, belongs to a computation increment that implements
  its methods step. Every definitive figure is saved in `FIGURES_DIR` by a computation increment.
- Reports never interpret, conclude, or discuss. Rendering a report creates or modifies no file
  in `RESULTS_DIR` or `FIGURES_DIR`.

## Expected outputs and acceptance criteria

- Expected outputs list only the analysis's own outputs, never provenance files. `RESULTS_DIR`,
  `FIGURES_DIR`, and `REPORTS_DIR` resolve to the methods version's
  `{Analysis_Results_Version_Folder}`, `{Analysis_Figures_Version_Folder}`, and
  `{Analysis_Reports_Version_Folder}`.
- Acceptance criteria are formal only: file existence, format, column names and types, row
  counts relative to an input, successful execution, seed reproducibility on synthetic data,
  report rendering, and report sections. A reproducibility criterion applies only to an increment
  with a row in Seeds and covers its outputs in `RESULTS_DIR`. Never write a provenance criterion.
  Name outputs by their configuration folder, for example `RESULTS_DIR/de-results.tsv`. Never
  depend on analysis results, such as a number of significant genes, or on the size of the test
  data, such as a fixed number of rows.
- A report's criterion refers to its entry in Reports, for example "contains the sections of the
  report of increment 4, in order", instead of listing the headings again.
- Every acceptance criterion maps to exactly one increment, and every increment has at least one.

## Removed, Setup, and Finalization

- The section order Removed, Setup, Increments, Finalization is the execution order.
- Setup phases, in order: `coder: renumber`; one `tester: image-check` and `coder: image-build`
  pair per tier-4 image, in the order of the Images table; `tester: test-setup`;
  `coder: real-config`; `tester: real-input-check`. Omit the image pairs when there is no tier-4
  image. The `coder: renumber` marker is complete except at a new version in which some increment
  number changes.
- The Removed section holds one entry per removed increment, with the phases
  `tester: remove-tests` then `coder: remove-code`, and is empty when no increment has been
  removed. An entry lists all the increment's old files, for example
  `Removed: 04-report.Rmd, 04-report.sh`, and takes no number in the increment sequence.
- Finalization always has the five phases of the template, in that order, with their phase
  constraints copied unchanged.
