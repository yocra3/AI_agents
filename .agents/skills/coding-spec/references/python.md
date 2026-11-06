# Python coding guidelines

Apply to Python scripts in any project. Repository conventions take precedence.

## Structure

- Order: header comments, imports, constants, functions, then top-level code.

## Conventions

- Follow PEP 8 as enforced by `ruff`. Use `pathlib.Path` for paths and type hints on functions.
- Fail with an exception and an informative message on invalid input; do not catch broad
  exceptions.
- Write tables with `pandas.DataFrame.to_csv(path, sep="\t", index=False)` or the `csv` module,
  unless another format is required.
- Seed every random step with a fixed seed, for example `numpy.random.default_rng(seed)`.
