# Analysis implementation plan template

Use this template for `{Plans_Folder}/<analysis-id>.plan.md`, the single implementation plan of
the methods document `{Analysis_Methods_file}` with the same `<analysis-id>`, `analysis-<slug>`.
`engineer` owns the content; `implementation_coordinator` changes only the execution markers
and Blockers.
Write acceptance criteria with the EARS guide in
`{Agents_Folder}/skills/generating-specs/EARS.md`.

```markdown
# Implementation plan: <analysis-id>

- **Methods document**: `<resolved {Analysis_Methods_file}, relative to the repository root>`
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

## Blockers

None.
```

## Phases

Every marker names its phase as `<agent>: <phase>`. The agents' skills and profiles define how
each phase is done; this table gives its meaning.

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
| Finalization | `reviewer: implementation-review` | Review the implementation against the methods document and this implementation plan. |
| Finalization | `dev_ops: code-documentation` | Add comments to the analysis code. |

## Content rules

- The implementation plan holds the engineering decisions only. Every scientific decision comes
  from the methods document; never add, choose, or change one here.
- It defines only what is specific to the analysis. Folders, file locations, configuration files,
  and provenance come from the Analysis layout in `{Agents_file}`; standard configuration keys,
  such as `ANALYSIS_ID`, `ANALYSIS_VERSION`, `RESULTS_DIR`, `FIGURES_DIR`, and `REPORTS_DIR`, come
  from the coding profile. Never copy a phase's general rules into it.
- Paths may be absolute or relative to the repository root. Write them relative to the repository
  root, and keep a path outside the repository absolute.
- `Version` always equals the methods document's `Version`. `Approval commit` is the approval
  commit it was last planned from.
- It has no change markers; its history is in Git.

## Software and effective parameters

- One row per package that a methods step or a report uses, with the version that
  selecting-container-images resolves and the image that provides it.
- Digest is the image's digest for tiers 1 to 3, and `registry` for tier 4: `coder` records it in
  `{Analysis_Images_file}` under the image ID at `coder: image-build`.
- Effective parameters lists, for each step, the values that the resolved version uses for the
  key parameters that the document leaves at their defaults, meaning those that can change the
  results, such as thresholds, test or fit types, filtering, and normalization. Take them from
  the documentation of that version. They record defaults and are never decisions.
- The table is the source for the manuscript. It is never copied into the methods document.

## Images

- Every increment and the input checks run in exactly one image of the Images table, as
  selecting-container-images selects it. The image of the input checks also runs the synthetic
  data generator and the reference subset script.
- A tier-4 image's Image is its recipe path in `{Analysis_Recipes_Folder}`, its Contents give the
  base image and every package with its version, and it has one `tester: image-check` and
  `coder: image-build` pair in Setup. When a missing Wave CLI sent the image to tier 4, its Tier
  is `4 recipe, Wave CLI missing`.

## Configuration

- One row per `INPUT_<NAME>` and `REF_<NAME>` key of Input data, with the same key and its
  Location as Real value. Test values point to the synthetic inputs and reference subsets in
  `{Analysis_Test_Inputs_Folder}`.
- One row per global parameter of the methods document, with its value as Real value. The Test
  value equals the Real value unless the synthetic data require another one; then Test value
  states why.

## Input checks

- Input checks check the Input data of the methods document and every technical requirement of
  this section.
- A technical requirement is what a step's functions require of an input that Input data does
  not state, such as integer counts for `DESeq2::DESeqDataSetFromMatrix`, a sorted and indexed
  BAM, or the same chromosome naming in two inputs. Derive it only from what the functions
  require.
- In large formats, such as BAM, CRAM, FASTQ, VCF, and BCF, a technical requirement can be
  checked only in the header and in the relations with other inputs.

## Test data

- Synthetic inputs: one rule per `INPUT_<NAME>` key. The data have the format, compression, and
  structure of Input data and are plausible: reasonable distributions, real identifiers taken
  from the reference subsets, such as gene IDs from the annotation subset, every level of each
  design variable with its reference level and at least its minimum replicates, and every
  relation between inputs. The generator sets the Generator seed.
- Planted signal: enough signal that no `synthetic` step produces empty outputs, for example a
  set of features with a large difference between the levels of each comparison. It is not a
  scientific decision: tests never check values.
- Reference subsets: one rule per `REF_<NAME>` key that derives a small, deterministic subset of
  the real resource at its Location, such as one chromosome, or the nf-core test-datasets of that
  resource when they exist.

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
- The Removed section holds one entry per increment removed at a new version, with the phases
  `tester: remove-tests` then `coder: remove-code`, and is empty when no increment has been
  removed. An entry lists all the increment's old files, for example
  `Removed: 04-report.Rmd, 04-report.sh`, and takes no number in the increment sequence.
- Finalization always has the five phases of the template, in that order.

## Blockers

- Blockers belong to `implementation_coordinator`: one entry per stop, written as
  `- **<cited section, step, increment, or phase>**: <stop condition, as reported>`, or `None.`.
  `engineer` writes `None.` in a new implementation plan and never changes Blockers.
