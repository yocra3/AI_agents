# Bash code documentation profile

## Scope

- Document every script with a header comment block and every non-trivial function with a
  function comment block.
- Record arguments, environment variables read, files written, standard output, and exit status
  when useful to callers.

## Conventions

- Follow the repository's existing comment style. Otherwise, use the
  [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html#comments).
- Place the script header after the shebang, with its purpose, usage, inputs, and outputs.
- Place the function block immediately above the function, with a summary line and only the
  sections that apply: `Globals:`, `Arguments:`, `Outputs:`, and `Returns:`.
- Keep documentation on the interface; do not narrate each command.

```bash
#!/usr/bin/env bash
#
# Purpose: Align paired-end reads and index the sorted BAM.
# Usage: align.sh <sample-sheet>
# Inputs: sample sheet with columns sample, fastq_1, fastq_2; REFERENCE environment variable.
# Outputs: <sample>.sorted.bam and <sample>.sorted.bam.bai in OUTPUT_DIR.

#######################################
# Align one sample and write a sorted BAM.
# Globals:
#   REFERENCE
# Arguments:
#   Sample name, first FASTQ path, second FASTQ path.
# Outputs:
#   Writes <sample>.sorted.bam to OUTPUT_DIR.
# Returns:
#   0 on success, non-zero if alignment fails.
#######################################
align_sample() {
  ...
}
```

## Generation

Bash comments need no generation step.

## Validation

- Run `bash -n` and the repository's lint, such as `shellcheck`, on changed scripts.
- Confirm that each documented argument, variable, and output matches the code.
