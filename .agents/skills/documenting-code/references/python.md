# Python code documentation profile

## Scope

- Document modules, public functions, classes, and methods with docstrings.
- Record arguments, return values, raised exceptions, side effects such as files written, and
  examples when useful to callers.

## Conventions

- Follow the repository's existing docstring style. Otherwise, use Google style: its `Args:`,
  `Returns:`, and `Raises:` sections read well in source and are parsed by both Sphinx
  (`sphinx.ext.napoleon`) and mkdocstrings without extra markup.
- Follow PEP 257: a triple-quoted docstring as the first statement, a one-line summary in the
  imperative mood ending with a period, then a blank line before any details or sections.
- Put a module docstring at the top of every script, after any shebang, stating its purpose,
  usage, inputs, and outputs.
- Do not repeat type hints in `Args:`; describe meaning, units, and accepted values instead.
- Keep documentation on the public contract; use `#` comments only for non-obvious
  implementation details.

```python
def count_reads(path: Path, min_quality: int = 20) -> int:
    """Count reads that pass the quality threshold.

    Args:
        path: FASTQ file, optionally gzip-compressed.
        min_quality: Minimum mean Phred quality of a counted read.

    Returns:
        Number of reads at or above `min_quality`.

    Raises:
        ValueError: If the file is not valid FASTQ.
    """
```

## Generation

Use the repository command when defined, such as a Sphinx or mkdocs build. Do not add a
documentation generator to a project that has none; docstrings need no generation step.

## Validation

- Run the repository's docstring lint, or `ruff check --select D` with
  `pydocstyle.convention = "google"` when `ruff` is configured.
- Run the repository's documentation build and tests, including doctests when configured.
