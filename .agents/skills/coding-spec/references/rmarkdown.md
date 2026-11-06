# R Markdown coding guidelines

Apply to R Markdown documents in any project. Repository conventions take precedence.

## Source

- Use `output: html_document` with `self_contained: true` unless another format is required.
- Load packages and inputs in the first chunks, and keep chunks short and named by purpose.
- Show tables with `knitr::kable()` or an available display package, and embed existing figure
  files with `knitr::include_graphics()`.
- Draw figures in chunks so the self-contained output embeds them.

## Rendering

Render with a script that calls `rmarkdown::render()` from the repository root into a dedicated
output folder:

```r
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
rmarkdown::render(
  "<path>/<report>.Rmd",
  output_dir = output_dir,
  intermediates_dir = tempdir(),
  knit_root_dir = getwd(),
  envir = new.env()
)
```

- Never write rendered output or intermediates next to the `.Rmd` sources.
- Rendering requires Pandoc.
