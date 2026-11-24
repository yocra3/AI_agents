# Analysis review rules

Use these rules for the implementation review of the implementation plan of an analysis methods
document, `{Plans_Folder}/<analysis-id>.plan.md` for `{Analysis_Methods_file}`. The methods
document is the contract. Take every path and file name from the Analysis layout keys in
`{Agents_file}`, resolved for the analysis.

## Scope

Review every increment of the implementation plan, with its `Files`, `Methods`, `Image`,
`Results`, Expected outputs, and acceptance criteria; its entry in Reports for a report
increment; the shared functions in `{Analysis_Shared_Functions_file}`; and `run-analysis.sh`.

## Checks

- Check point by point that each computation script implements its methods steps as the methods
  document states them: tool, inputs, non-default parameters, filters, model, and multiple-testing
  correction, read with the document's omission rules, using the software of the implementation
  plan's Software and effective parameters and running in its increment's image.
- Check what each report computes against its entry in Reports, and that its prose only states
  what each table or figure shows and which file or methods step produced it.
- Check that each table, file, and figure that a computation script or a report produces is one
  that the implementation plan declares, in Expected outputs or in the report's entry in Reports.
- Check that `run-analysis.sh` checks every image it uses and runs the input checks before the
  first script, then runs every increment's computation and render scripts in `NN` order, each in
  its increment's image.
- Do not review result values.

## Classification

Blocking:

- a deviation from a methods step or from the implementation plan's software or images;
- a statistical test or a model that no methods step states, in a computation script;
- costly, inferential, or model-based computation inside a report that its entry in Reports does
  not list; a simple descriptive calculation that the entry does not list is not blocking;
- interpretive text, such as descriptions of values, conclusions, or discussion;
- a `run-analysis.sh` that does not meet the check above.

Non-blocking: a descriptive table, file, or figure, in a report or a computation script, that the
methods document does not ask for and that changes no required result. Recommend removing it, or
adding it to Results to report, either in a revision of the current `Version` or in a new
`Version`; the user decides.
