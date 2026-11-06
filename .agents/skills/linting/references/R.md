# R and R Markdown linting with lintr and styler

Use the repository's lint command when defined; otherwise run these checks from the repository
root. Respect `.lintr` when present.

- Lint: `Rscript -e 'quit(status = length(lintr::lint("<file>")) > 0)'`. `lintr::lint()` returns
  its findings without setting an exit status; the wrapper fails when any finding remains.
- Format check: `Rscript -e 'styler::style_file("<file>", dry = "fail")'`.
- Syntax check, `.R` files only: `Rscript -e 'invisible(parse("<file>"))'`.
- Fix: `Rscript -e 'styler::style_file("<file>")'` corrects formatting; resolve remaining lintr
  findings by hand.

Official references: [lintr](https://lintr.r-lib.org/), [styler](https://styler.r-lib.org/).
