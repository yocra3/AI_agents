# Analysis inputs reference

Rules for the Input data section of an analysis methods document. The same text feeds the
synthetic data generator, the input checks, and the data section of the manuscript, so it
uses fixed fields and a closed vocabulary. The methods document template refers to this file,
`defining-analysis-inputs` helps write the section, and contract validation checks it against the
completeness criteria below.

## Principles

- Describe only what the analysis uses, with its shape. Do not describe columns, fields, slots, or
  files that no methods step uses; input checks accept them.
- Never record counts, such as rows, variants, genes, or samples. The only count allowed is the
  minimum number of replicates per level of a design variable.
- Never record per-record values, measurements, sample or patient identifiers, or free text taken
  from the data. Describe identifiers by their pattern.
- Record what the user knows about the data, not what the methods require of it. Technical
  requirements derived from the methods, such as integer counts for DESeq2 or a sorted and indexed
  BAM, belong to the implementation plan, where `engineer` turns them into input checks.
- Use only the formats and the vocabulary below. A missing format is added to this reference
  through `craftsman`; never write "other".
- The section may be written by the user, by `data_analyst`, or with `defining-analysis-inputs`,
  at any time before the document is authorized.

## Section layout

One subsection per input, headed by its key, followed by a subsection with the relations between
inputs.

```markdown
### `INPUT_<NAME>`

- **Content**: <one sentence with the biological meaning>
- **Location**: `<path to one file or one folder>`; <for a folder: relative pattern read, and what is ignored>
- **Format**: <format from the list>, <compression, or uncompressed>
- **Structure**: <items of the format's family>
- **Constraints**: <vocabulary below, per used column or field>

### `REF_<NAME>`

- **Content**: ...
- **Location**: ...
- **Format**: ...
- **Structure**: ...
- **Constraints**: ...
- **Version**: <release or version of the resource>
- **Source**: <provider and download URL>
- **Assembly**: <genome assembly, when the resource is tied to one>

### Relations between inputs

- <`INPUT_A` column or field>: <relation> <`INPUT_B` column or field>
```

## Fields

| Field | Rule |
| --- | --- |
| Key | `INPUT_<NAME>` for the user's data, `REF_<NAME>` for a reference resource such as a genome, an annotation, or a public database. `<NAME>` uses upper-case letters, digits, and underscores, and is unique in the document. |
| Content | One sentence that states what the data are, with their biological meaning. |
| Location | The exact path of one file or one folder, never a list. Absolute paths and paths relative to the repository root, where scripts run, are accepted; agents prefer relative paths when they write one. A small fixed set of distinct files is one input per file. For a folder, give the relative pattern of the files read, for example `<sample>/quant.sf`, and what is ignored. |
| Format | One format from the list below, with its compression, for example `TSV, gzip`, `VCF, bgzip`, or `BAM`. |
| Structure | The items of the format's family, below. |
| Constraints | Constraints from the vocabulary below for each used column or field. Missing values are always declared. |
| Version, Source, Assembly | Reference resources only. Reference resources are real files that the user provides by path; only the user's data are replaced by synthetic data in tests. |

## Formats and their structure

| Family | Formats | Structure |
| --- | --- | --- |
| Tables | TSV, CSV | Whether there is a header; what one row represents; the key column; each used column with its type and meaning. |
| Matrices | MTX; TSV or CSV whose cells all hold one kind of value, such as a count matrix | What rows and columns are, each with its identifier pattern; the type of the values. |
| Genomic formats | VCF, BCF, BAM, CRAM, FASTQ, FASTA, GTF, GFF3, BED | Only the specific features the analysis uses, as the user knows them: assembly, `chr` prefix on chromosome names, single-end or paired-end, sorted and indexed, and the INFO or FORMAT fields used. |
| Objects | h5ad, RDS | The class, and the slots, assays, or columns used. |

## Vocabulary

**Types**: `integer`, `float`, `string`, `boolean`, `categorical`, `date`.

**Constraints**:

- **Range**: minimum and maximum with their comparison, for example `>= 0`; only when a method
  requires it.
- **Unique**: no value repeats in the column or field.
- **ID pattern**: a regular expression, for example `^ENSG[0-9]{11}$`; for a path column of a
  manifest, the pattern of its paths.
- **Missing values**: always declared, as `not allowed` or `allowed as <notation>`, where the
  notation is `NA`, empty, or `.`.

**Relations between inputs**:

- **Same set**: both hold the same identifiers.
- **Inclusion**: every identifier of one exists in the other.
- **Same order**: both list the same identifiers in the same order; only when a method requires it.

## Design variables

Mark each column the model uses as a design variable, with its levels, its reference level, and
the minimum number of replicates per level. A variable whose levels identify people, such as a
patient column in a paired design, is an identifier: record its ID pattern and its number of
levels instead of its levels.

## Manifests

A manifest is a table whose column holds paths to other files, such as a samplesheet with paths to
FASTQ files. Describe it as a table. Each path column is a used column of type `string`, with the
format and compression of the files it points to and the structure items of that format's family,
and its ID pattern as a constraint. Paths are values: record the pattern, never the paths. As in
Location, the paths may be absolute or relative to the repository root. The input checks verify
that every listed path exists and that every listed file meets its declared format.

```markdown
### `INPUT_SAMPLESHEET`

- **Content**: Raw RNA-seq reads of each sample.
- **Location**: `data/rnaseq/samplesheet.csv`
- **Format**: CSV, uncompressed
- **Structure**: Table with a header; one row per sample; key column `sample`.
  - `sample`: `string`, sample identifier.
  - `fastq_1`, `fastq_2`: `string`, paths to the read 1 and read 2 files of the sample. Files:
    FASTQ, gzip; paired-end.
- **Constraints**: `sample` unique, ID pattern `^S[0-9]{3}$`, missing values not allowed.
  `fastq_1`, `fastq_2` unique, ID pattern `^data/rnaseq/fastq/S[0-9]{3}_R[12]\.fastq\.gz$`,
  missing values not allowed.
```

## Example

```markdown
### `INPUT_COUNTS`

- **Content**: Gene-level RNA-seq read counts per sample.
- **Location**: `data/rnaseq/counts.tsv.gz`
- **Format**: TSV, gzip
- **Structure**: Matrix with a header. Rows are genes, ID pattern `^ENSG[0-9]{11}$`, in the first
  column `gene_id`; columns are samples, ID pattern `^S[0-9]{3}$`. Values are `integer`.
- **Constraints**: `gene_id` unique. Values: range `>= 0`; missing values not allowed.

### `INPUT_METADATA`

- **Content**: Experimental condition of each sample.
- **Location**: `data/rnaseq/samples.csv`
- **Format**: CSV, uncompressed
- **Structure**: Table with a header; one row per sample; key column `sample_id`.
  - `sample_id`: `string`, sample identifier.
  - `condition`: `categorical`, treatment received. Design variable: levels `control`,
    `treated`; reference level `control`; at least 3 replicates per level.
- **Constraints**: `sample_id` unique, ID pattern `^S[0-9]{3}$`, missing values not allowed.
  `condition` missing values not allowed.

### `REF_ANNOTATION`

- **Content**: Gene annotation used to name genes and keep protein-coding genes.
- **Location**: `refs/gencode.v44.annotation.gtf.gz`
- **Format**: GTF, gzip
- **Structure**: `chr` prefix on chromosome names; attributes `gene_id` and `gene_type` used.
- **Constraints**: `gene_id` ID pattern `^ENSG[0-9]{11}\.[0-9]+$`; missing values not allowed.
- **Version**: GENCODE release 44
- **Source**: https://www.gencodegenes.org/human/release_44.html
- **Assembly**: GRCh38

### Relations between inputs

- `INPUT_COUNTS` sample columns: same set as `INPUT_METADATA` `sample_id`.
- `INPUT_COUNTS` `gene_id`: inclusion in `REF_ANNOTATION` `gene_id` without its version suffix.
```

## Completeness criteria

The section is complete when all of these hold:

1. Every input has a unique `INPUT_<NAME>` or `REF_<NAME>` key and the fields Content, Location,
   Format, Structure, and Constraints.
2. Content states the biological meaning of the input.
3. Location is one file or one folder; a folder states the relative pattern read and what is
   ignored.
4. Format is one from the list and states its compression.
5. Structure has every item of its family, and every used column or field has a type from the
   vocabulary and a meaning.
6. Missing values are declared for every used column, field, or matrix value.
7. Every design variable has its levels, its reference level, and the minimum number of replicates
   per level, or, when its levels identify people, its ID pattern and number of levels.
8. Every reference resource has Version and Source, and Assembly when it is tied to one.
9. Every pair of inputs whose identifiers the analysis matches has a relation from the vocabulary.
10. The section records nothing the principles above forbid and has no pending values, such as
    `TBD`, `?`, or unfilled placeholders.
11. Every path column of a manifest states the format and compression of the files it points to,
    the structure items of that format's family, and its ID pattern.
