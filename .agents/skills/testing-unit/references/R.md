# R and R Markdown testing with testthat

Use the repository's test layout and command when defined; otherwise follow these conventions.
Test R Markdown through the R code it runs or through the effects of rendering it.

- Layout: one `test-<slug>.R` file per component or behavior in the test folder, conventionally
  `tests/testthat/`, with `test_that()` blocks and `expect_*()` assertions.
- Shared setup: put reusable functions, fixtures, and custom skips in `helper-*.R` files in the
  same folder. Do not put tests in them.
- Session-level setup: `testthat::test_dir()` sources the `helper-*.R` and `setup-*.R` files once,
  in alphabetical order, before any test file. Put work that must run once per test session in a
  `setup-*.R` file and register its cleanup with `withr::defer(<cleanup>, testthat::teardown_env())`.
- Temporary files: use `withr::local_tempfile()` or `withr::local_tempdir()`.
- Skip: `testthat::skip_if(<condition>, "<reason>")` or `testthat::skip_if_not()`, always with a
  reason.
- Run: `Rscript -e 'testthat::test_dir("<dir>", stop_on_failure = TRUE)'`, which exits with a
  non-zero status when a test fails.

Official reference: [testthat](https://testthat.r-lib.org/).
