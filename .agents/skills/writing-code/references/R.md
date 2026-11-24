# R coding guidelines

Apply to R scripts in any project. Repository conventions take precedence.

## Structure

Each script follows this order: header comments, `library()` calls for every attached package,
constants such as seeds, function definitions, then top-level steps in execution order.

- Load shared functions with `source()` and a path relative to the repository root.

## Conventions

- Follow the tidyverse style guide: `snake_case`, `<-` for assignment, two-space indentation, and
  lines of at most 80 characters. `lintr` and `styler` enforce it.
- Do not call `install.packages()`, `BiocManager::install()`, `require()`, `setwd()`, or
  `rm(list = ls())` in scripts.
- Build paths with `file.path()`.
- Use `pkg::fun()` for single uses or masked names, and in every call that could resolve to more
  than one attached package.
- Validate the input structure before computing, and fail with `stop()` and an informative
  message. Do not hide errors or warnings with `try()`, `tryCatch()`, or `suppressWarnings()`
  unless the condition is expected and handled explicitly.
- Keep functions small and free of side effects other than their declared output files. Define
  them before use.

## Outputs

- Write tables as tab-separated text without row names, unless another format is required, for
  example with `utils::write.table(x, path, sep = "\t", quote = FALSE, row.names = FALSE)`.
- Coerce columns to their declared types before writing.
- Write figures with `ggplot2::ggsave()` or an explicit graphics device closed with `dev.off()`.

## Randomness

- Call `set.seed()` with a fixed seed immediately before each random step.
- For parallel work, use `RNGkind("L'Ecuyer-CMRG")` with `set.seed()`, `future.seed = <seed>` in
  `future` or `furrr`, or `RNGseed` in `BiocParallel`, so results do not depend on the number of
  workers.
