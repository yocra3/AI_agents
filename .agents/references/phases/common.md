# Common phases

Phases shared by specification and analysis implementation plans, and the delegations of
`implementation_coordinator` that are not plan markers; each plan type's own phases are in
[specs.md](specs.md), [nextflow.md](nextflow.md), and [analysis.md](analysis.md).

## `tester: remove-tests`

- **Meaning**: Remove the tests of a removed step, acceptance criterion, or increment.
- **Skill**: testing-unit.
- **Steps**:
  1. Remove only the tests of the removed item that the Removed entry names, and the static test
     data that only they use, from the files that the entry lists.
  2. Run the remaining relevant suite and confirm GREEN. The phase has no RED.
- **Evidence**: the removed tests and files, and the suite command and result.
- **Stops**: the remaining suite fails after the removal.

## `coder: remove-code`

- **Meaning**: Remove the code of a removed step, acceptance criterion, or increment from the
  files that the Removed entry lists.
- **Skill**: coding-spec.
- **Steps**:
  1. Remove only the code of the removed item from the files that the Removed entry lists,
     deleting a file that holds nothing else.
  2. Remove the references to that code that would no longer resolve. Change no other behavior.
- **Evidence**: the changed and deleted files, and the references removed.
- **Stops**: none of its own.

## `tester: test`

- **Meaning**: Write the failing tests of a step or increment and confirm RED.
- **Skill**: testing-unit.
- **Steps**:
  1. Run the relevant existing tests and record the baseline.
  2. Write or extend tests of the tasks of the step or increment and of the acceptance criteria
     mapped to it, at the cheapest boundary that observes the behavior, with expected results
     independent of any implementation.
  3. Run them and confirm RED, as testing-unit defines it.
  4. Lint the changed test files with the linting skill and fix findings in them.
- **Evidence**: the covered behavior and criteria, the changed files, the exact commands and
  results, and the expected failure reason.
- **Stops**: the tests pass before implementation, or the contract does not define the expected
  result.

## `coder: implementation`

- **Meaning**: Make the minimum change that turns the tests of a step or increment GREEN.
- **Skill**: coding-spec.
- **Steps**:
  1. Run tester's exact command from the brief and confirm the expected RED before editing code.
  2. Make the minimum production change that turns the tests GREEN, with no unrelated behavior
     or refactoring.
  3. Run the targeted tests and the relevant fast suite.
  4. Lint the changed files with the linting skill, fix the findings that the change introduced,
     and run the affected tests again. Report other findings without fixing them.
- **Evidence**: the RED reproduction, the changed files, the GREEN commands and results, the lint
  results, and unresolved work.
- **Stops**: the RED does not reproduce, or a test is invalid or contradicts the contract; never
  change the test.

## `coder: full-validation`

- **Meaning**: Run the complete test suite and lint every file changed on the task branch,
  without changing files.
- **Skill**: linting.
- **Steps**:
  1. Take as scope every file changed on the task branch: the files that differ between the
     working tree and the merge base with `{Default_Branch}`, plus untracked files, excluding
     deleted files. Use only read-only Git commands, for example:

     ```bash
     git diff --name-only --diff-filter=d "$(git merge-base {Default_Branch} HEAD)"
     git ls-files --others --exclude-standard
     ```

  2. Run the complete test suite with the project's test command from `{Agents_file}` when it
     defines one; otherwise run every test of the repository with the run command of its
     language's test framework. Run it in the execution environment that the implementation
     plan declares, when it declares one.
  3. Lint each in-scope file with the linting skill, without fixes. Skip files that have no lint
     profile.
  4. Edit no file, apply no lint fix, and fix no finding; only the suite's own outputs may be
     written.
- **Evidence**: the exact commands, the suite result, the lint result of each in-scope file, the
  skipped files, and the file of every failure.
- **Stops**: a required placeholder or the test command cannot be resolved.

## `reviewer: implementation-review`

- **Meaning**: Review the implementation against its contract and implementation plan.
- **Skill**: reviewing-implementation.
- **Steps**:
  1. Review the task branch with reviewing-implementation, with the contract, the implementation
     plan, and the `full-validation` report given in the brief. Change no file.
- **Evidence**: the skill's report, ending with its `Verdict:` line.
- **Stops**: the skill's stops.

## `<agent>: validation-fix`

- **Meaning**: Fix the failures of the `full-validation` report in the files routed to the agent.
  Not a plan marker: delegated to `coder`, `tester`, or `cleaner` when the `full-validation`
  report shows a failure in a file that agent owns.
- **Skill**: coding-spec for `coder` and `cleaner`, testing-unit for `tester`.
- **Steps**:
  1. Fix only the failures that the brief routes to you, in those files.
  2. `tester` changes only tests and their static data; `cleaner` only refactors, preserving
     behavior; `coder` changes no test or its static data. In the frozen test support code of an
     analysis, fix only lint findings, without changing its behavior.
  3. Run the failing tests or checks again, then the relevant suite.
  4. Lint the changed files with the linting skill and fix findings in them.
- **Evidence**: the changed files, and the commands and results of the tests, checks, and lint.
- **Stops**: the fix needs a change to a file that another agent owns, or to the contract or
  implementation plan; or a failure in the frozen test support code of an analysis needs more
  than a lint fix that preserves behavior.

## `reviewer: contract-validation`

- **Meaning**: Validate the contract read-only. Not a plan marker: delegated for a `Draft`
  contract after the user's authorization and before the approval commit, on the current branch.
- **Skill**: validating-contracts.
- **Steps**:
  1. Validate the contract at the path in the brief with validating-contracts. Change no file.
- **Evidence**: the skill's report, ending with its `Verdict:` line.
- **Stops**: the skill's stops.

## `engineer: planning`

- **Meaning**: Create or update the contract's single implementation plan and advance the
  contract to `Planned`. Not a plan marker: delegated after the approval commit, while the
  contract is at `Approved`.
- **Skill**: planning-specs for a specification, planning-analysis for a methods document.
- **Steps**:
  1. Plan the contract with the skill of its type, in the mode that the skill chooses.
- **Evidence**: the skill's output.
- **Stops**: the skill's stops.

## `engineer: replanning`

- **Meaning**: Update the implementation plan from implementation evidence. Not a plan marker:
  delegated when implementation evidence shows that the scope, dependencies, phase order,
  technical decisions, or acceptance-criterion mapping of the implementation plan must change,
  or that the frozen test support code of an analysis must change or fails functionally.
- **Skill**: planning-specs for a specification, planning-analysis for a methods document.
- **Steps**:
  1. Replan with the skill's replanning rules, from the evidence in the brief.
- **Evidence**: the skill's output, with the markers reset and the Removed entries added.
- **Stops**: the skill's stops.
