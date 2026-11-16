---
name: selecting-container-images
description: Match the chosen methods of an analysis plan to the project's container image registry and propose images for the gaps. Use after the methods are chosen and before writing the plan. Never build images or change recipes.
---

# Purpose

Give every increment of the plan an image from `{Analysis_Images_file}` that provides its tools,
following the rules of `{Agents_Folder}/templates/container-images.template.md`. The user builds
images and changes recipes; `data_analyst` proposes options and records registry entries.

# Workflow

## 1. Match the registry

Compare each chosen package or tool with the Contents of the registry entries and decide which
image covers each operation. An increment runs in one image, so the tools of one increment, its
test framework, and its linter must all be in that image.

## 2. Verify registry images

When Contents do not settle whether a package or tool is present, check it with a read-only
command in the image under the execution rules in `{Agents_file}`, for example:

    apptainer exec <image> Rscript -e 'packageVersion("coloc")'
    apptainer exec <image> samtools --version

Never execute anything else in an image.

## 3. Search the gaps

For each missing package or tool, query the public indexes below with its name only, never with
project data. Conda names are lower case: Bioconductor packages are `bioconductor-<name>` in
Bioconda, CRAN packages are `r-<name>` in conda-forge and sometimes in Bioconda, and other tools
usually keep their name.

- Bioconda and conda-forge, through the Anaconda.org API used by `anaconda-client`.
  `<channel>` is `bioconda` or `conda-forge`. The first query returns `versions` and
  `latest_version`, or an `error` with HTTP 404 when the package is absent. The second matches
  names containing the term in every channel; keep `bioconda` and `conda-forge` results.

      curl -s https://api.anaconda.org/package/<channel>/<conda-name>
      curl -s 'https://api.anaconda.org/search?name=<term>&type=conda'

- BioContainers: every Bioconda package has an image `quay.io/biocontainers/<conda-name>`. The
  Quay API lists its tags, `<version>--<build>`, with their `manifest_digest`; a repository that
  does not exist returns HTTP 401. The Galaxy depot serves many of the same tags as Singularity
  images for Apptainer; HTTP 200 means present, and the digest is the sha256 of the downloaded
  file. Without a depot image, Apptainer can use
  `docker://quay.io/biocontainers/<conda-name>:<tag>`.

      curl -s 'https://quay.io/api/v1/repository/biocontainers/<conda-name>/tag/?onlyActiveTags=true&filter_tag_name=like:<version>'
      curl -sI https://depot.galaxyproject.org/singularity/<conda-name>:<tag>

An analysis that needs several packages in one image, typical of R, usually needs a custom image.
BioContainers images hold one package and its dependencies; a multi-package "mulled" image exists
only for combinations requested in `BioContainers/multi-package-containers`.

## 4. Propose

Propose one option per gap to the user: use a BioContainers image, add packages to an existing
recipe, or create a new image. Flag a BioContainers image that lacks the test framework, linter,
rmarkdown, or Pandoc that the registry rules require. The user decides and builds the image; then
add its registry entry and use its ID in the plan.

```yaml
- gap: <package or tool>
  needed_by: <operations>
  found: <conda channel and version, BioContainers tag and digest, or not found>
  proposal: <biocontainers | add-to-recipe | new-image>
  detail: <image with tag and digest, recipe and packages to add, or base and packages>
  missing: <test framework, linter, rmarkdown, or Pandoc the registry requires, or none>
```

# Prohibited

- Building images or modifying recipes.
- Running commands other than the package-presence checks on registry images, the read-only
  queries above, and the sha256 of a local image file.
- Sending project data, such as paths, sample names, or file contents, to any external service.
