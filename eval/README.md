# Evaluation kit (design, not implemented)

This folder will hold a self-contained kit to evaluate the agent definitions end to end: scripts
that prepare a throwaway project and its data, scripted user prompts for each scenario, and
automatic checks. It is outside `.agents`, `.claude` and `.codex`, so `install.py` never copies it
into projects.

Status: design only. Nothing here is implemented yet. The first use is the pilot that validates
the restructuring into one implementation flow (version `1.0.0`).

## What can be automated

1. **Deterministic setup.** Scripts create a fresh Git repository, install the agents with
   `install.sh`, write a prefilled `AGENTS.md` and `CLAUDE.md`, and download and prepare the data.
   This makes every run repeatable.
2. **Scripted scenarios.** Each scenario is a file of prompts that plays the user, run
   non-interactively (`claude -p` in Claude Code, `codex exec` in Codex). Explicit authorizations
   are written in the prompt itself, for example "I authorize executing `analysis-airway` v1", so
   the explicit-approval rule still holds.
3. **Automatic checks.** Scripts verify each scenario with formal criteria only, like the
   framework's own tests:
   - expected files and statuses;
   - approval commit messages;
   - matching `Version` in the methods document and the implementation plan;
   - `reviewer`'s verdict in the negative cases;
   - no push, merge or tag.
4. **Data-leak detection.** The prepared data contain canary values: unique, made-up identifiers
   and values. After a run, a script searches the transcripts and generated documents for them. A
   hit means an agent put real data values into its context, which tests the exploration rules
   objectively.

## What cannot be automated well

- **The quality of `data_analyst`'s explanations for beginners.** A scripted user cannot judge
  whether an explanation is clear. A person reads the transcript.
- **Interaction.** In non-interactive mode agents cannot ask questions, so the script must answer
  everything in advance. `data_analyst` tends to ask, which can end in a stop rather than a
  realistic exchange.
- **Permissions.** Unattended runs need relaxed session permissions in the test repository. Limit
  them to that directory and never use them on real projects.

## Risks

- **Cost and usage limits.** A full run, with Opus coordinating many subagents, is expensive and
  can hit the 5-hour usage limit. Scenarios must run one at a time and be resumable.
- **Non-determinism.** Two runs never produce the same text, so checks must stay formal, never
  about exact content.
- **Codex.** It is not yet verified whether `codex exec` can start a specific custom agent as the
  main session. Verify it before promising parity between both tools.
- **Environment.** On the current cluster there is no `fakeroot` mapping for the user, no Wave
  CLI, no Docker and no host R. Image scenarios will then exercise the fallback paths: a tier-4
  recipe instead of Seqera Containers, and the stop that asks the administrator for build
  permissions. The kit should detect and record this instead of failing.

## Pilot design

**Data.** The Bioconductor `airway` dataset (Himes et al. 2014): 8 samples, 4 cell lines, treated
or untreated with dexamethasone.
- A samplesheet (manifest) with one row per sample: the path to its count file, the cell line and
  the treatment.
- One count file per sample.
- The Ensembl GRCh37 release 75 GTF as reference resource, matching the `airway` gene IDs.

This exercises manifests, design variables and relations between inputs.

**Expected methods**, which `data_analyst` writes with the scripted user:
1. Import with `DESeq2::DESeqDataSetFromHTSeqCount`, which reads the samplesheet.
2. Filtering of low-count genes.
3. DESeq2 with design `~ cell + dex`, treated versus untreated, Benjamini-Hochberg correction.
4. VST and PCA.
5. Gene symbol annotation from the GTF.

Results to report: PCA, MA plot, volcano plot and a table of differential genes.

**Scenarios**

| ID | Scenario | What it checks |
| --- | --- | --- |
| A | Drafting with input exploration | Inputs skill, context rules, canaries |
| B | Manual `reviewer` validation, plus a methods document with the multiple-testing correction omitted | Step cards and blocking verdict |
| C | Authorization and `implementation_coordinator` up to `Coded` | Approval, planning, Setup, increments, Finalization |
| D | The user's `run-analysis.sh` run and `post-run` checks up to `Verified` | Pre-checks and closing |
| E | A deliberate error in the real inputs | `real-input-check` and `run-analysis.sh` stop with messages that carry no values |
| F | Same-version revision that appends a final step | Increments are only appended |
| G | Changing the filter threshold without a new version, then with `v2` | Blocking, renumbering, empty version folders |
| H | Images | Fallback to a recipe without Wave; build stop or build success |
| I | A small programming specification | Regression of the delivery flow |
| J | Codex: A to D, plus subagent network access and main-session launch | Parity between tools |

**Order.** Run Claude Code first, end to end. Fix what fails through `craftsman` on the same
branch, then repeat in Codex.

## Judge agent

Formal checks stay as scripts: they are deterministic and cost nothing. A judge agent covers only
what a script cannot assess:
- whether `data_analyst` explains in plain language, proposes instead of asking, and gives
  alternatives with their consequences;
- whether `reviewer`'s findings are understandable and cite the affected section;
- whether stops were justified or unnecessary;
- whether any agent took a scientific decision that is not in the approved methods document, which
  is the pilot's main criterion.

To make it reliable:
- **Closed rubric.** Yes-or-no questions per scenario, each answer backed by a quote from the
  transcript. No 1-to-10 scores.
- **Separate context.** The judge never shares context with the run it evaluates, and preferably
  uses a different model, so it does not grade itself.
- **Calibration.** Before trusting it, compare its answers with two or three transcripts graded by
  hand.
- **Evaluation only.** The judge lives in `eval/`. It is not an agent of the framework and is never
  installed into projects.

## Repeated runs

Each repetition runs in a fresh repository. The report gives, for each check and each rubric
question, the share of runs that pass, and flags as unstable those that do not always pass. Cost
grows with the number of runs, so there are two tiers:
- **Cheap, many runs (10 or more).** `reviewer` on fixed methods documents: one valid, one with the
  multiple-testing correction omitted, and one with a change that needs a new version but keeps the
  old one. This measures the false positives and false negatives of contract validation, the gate
  of the whole flow. The same applies to `real-input-check` on inputs with a known error.
- **Expensive, few runs (2 or 3).** The full flow (scenarios C and D). Here the question is whether
  `engineer`'s decisions are stable: the number of increments, the images chosen, and the stops.

## Proposed layout

```text
eval/
  README.md            how to run, approximate cost, and what is reviewed by hand
  setup-project.sh     creates the test repository, installs, writes AGENTS.md and CLAUDE.md
  data/fetch-airway.sh downloads airway and the GTF, builds the samplesheet, inserts canaries
  fixtures/            prefilled AGENTS.md, and fixed methods documents for the reviewer runs
  scenarios/           one file per scenario (A to J) with the prompts that play the user
  judge/               the judge's instructions and one rubric per scenario
  run.sh               runs all scenarios or a selection, in Claude Code or Codex, N times each,
                       and saves the transcripts
  checks/              one check per scenario, plus the canary check
  report.sh            results table: scenario, check or rubric question, pass rate, unstable flag
```

Results and transcripts go to a folder ignored by Git.

## Decisions

1. **Selectable automation.** `run.sh` runs the whole evaluation or only the chosen scenarios, with
   a number of repetitions for each.
2. **Who builds it.** The main session builds the whole kit, prompts included. `craftsman` is not
   needed, because nothing here is installed into projects.
3. **Prompt language.** Spanish, as real users will write, which also checks that agents answer in
   the user's language.

## Open questions

- **CLI options.** How `claude -p` and `codex exec` start a given agent as the main session and
  control permissions. To be assessed when the kit is implemented; it shapes `run.sh` more than
  anything else.
