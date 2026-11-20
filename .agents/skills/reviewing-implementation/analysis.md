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
- Check that each report computes only the simple calculations of its entry in Reports, and that
  its prose only states what each table or figure shows and which file or methods step produced
  it.
- Check that `run-analysis.sh` checks every image it uses and runs the input checks before the
  first script, then runs every increment's computation and render scripts in `NN` order, each in
  its increment's image.
- Do not review result values.

## Classification

Blocking: a deviation from a methods step or from the implementation plan's software or images;
costly, inferential, or unassigned computation inside a report, meaning any computation that its
entry in Reports does not list; interpretive text, such as descriptions of values, conclusions, or
discussion; and a `run-analysis.sh` that does not meet the check above.
