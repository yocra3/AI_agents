---
name: defining-analysis-inputs
description: Write or revise the Input data section of an analysis methods document, by interview or, with explicit authorization for each path, by exploring the structure of the data; authorizing a manifest also covers the header and format of the files it lists. Never creates the methods document.
---

# Purpose

Produce an Input data section that meets `{Agents_Folder}/references/analysis-inputs.md`. Read
that reference first: its fields, formats, vocabulary, and completeness criteria are the target,
and the section records only the shape of what the analysis uses.

# Where the section goes

- Used by `data_analyst`: return the section in the conversation; `data_analyst` writes it into
  the document.
- Invoked by the user: require an existing methods document, the `{Analysis_Methods_file}` the
  user names or the single match in `{Analysis_Methods_Folder}`; ask when several match. Change
  only its Input data section. If the document has an approval commit,
  `docs(<analysis-id>): approve methods vN`, tell the user that the change also needs a row in its
  version control table and `Status` back at `Draft`, which `data_analyst` records.
- With no methods document and no `data_analyst` session: stop, and explain that the analysis
  must first be started with `data_analyst`. Never create the methods document, not even empty.

# Modes

Use the interview unless the user explicitly authorizes exploring a path. An authorization covers
only the paths it names; use the interview for every other input. An authorization to explore a
manifest also covers reading the header and format of each file it lists, and nothing more of
those files; the exploration rules below apply to them. The modes can be mixed.

## Interview

Without accessing the data, go through each field of each input in plain language, offering the
options of the vocabulary: formats, types, constraints, missing-value notations, and relations.
Explain each term with a short example, for example "Is there a column that names each sample,
such as S001?".

## Exploration

Everything that enters your context is sent to the model provider. Commands may read a whole file
to compute a summary, but only summaries may reach the context, in this order of preference:

1. Commands that show no data values, such as `head -1` for a header, `wc -l`, an `awk` check that
   prints only whether it passes, or the number of distinct levels of a column.
2. The levels of the design columns.
3. As a last resort, a few rows with `head -n`, never from a file with data that can identify
   people.

Never load a data file into the context with a file-reading tool or a command that prints it.

Record only the shape: column names, types, levels of the design variables, identifier patterns
as regular expressions, generic constraints, and standard format headers. Check that every level
of a design variable reaches the minimum number of replicates without recording how many it has.
Never record counts, per-record values, measurements, sample or patient identifiers, or free
text. When column names are identifiers, such as the sample columns of a count matrix, record
their pattern, not the names. A variable whose levels identify people is an identifier: record
its pattern and its number of levels. Paths in a manifest are values: record the path column and
the pattern of its paths, never the paths.

Locations and the paths in a manifest may be absolute or relative to the repository root, where
scripts run. Write a location relative to the repository root when you can, and you may tell the
user that relative paths are preferred.

Read binary formats with, in this order:

1. a tool available on the system;
2. an image of `{Analysis_Images_file}`, read-only, under the execution rules in `{Agents_file}`;
3. otherwise, the interview for that input.

Print only the header lines needed, because headers can hold identifiers: for example,
`samtools view -H <file> | grep '^@SQ'` without `@RG` sample names, or
`bcftools view -h <file> | grep '^##'`, which leaves out the `#CHROM` line with sample names.
From the headers, read the version and the assembly of a reference resource when the format
carries them.

Exploration leaves a draft. Always ask the user for:

- the biological meaning of each input and of each used column or field;
- which columns are design variables, their reference level, and the minimum replicates per level;
- what missing values mean;
- whether a mismatch between inputs, such as samples present in one and absent in the other, is
  intended.

## Reference resources

Reference resources are real files that the user provides by path. When the user does not have
one, name the exact file needed and where to download it; downloading and placing it are the
user's.

# Completeness check

Before finishing, apply the completeness criteria of the reference and tell the user in plain
language what is missing and what each missing item is for.

# Output

Return the section, or the path of the updated document; the mode used for each input and the
paths explored; the missing items from the completeness check; and the open questions.

# Prohibited

- Creating the methods document or changing any section other than Input data.
- Exploring a path without the user's explicit authorization for it.
- Writing technical requirements that follow from the methods, such as integer counts for a
  method that needs them.
- Modifying data, installing packages, downloading resources, or sending any project data, such
  as paths, file contents, or identifiers, to an external service.
