---
name: selecting-container-images
description: Select the container image of each increment and of the input checks of an analysis implementation plan, in tier order from the project registry, BioContainers, and Seqera Containers, and specify a recipe when none fits. Use from planning-analysis while engineer plans a methods document. Never build images locally or write recipes.
---

# Purpose

Give every increment of the implementation plan, and its input checks, one image that provides
all their tools, following the rules of
`{Agents_Folder}/references/templates/container-images.template.md`.
`engineer` resolves tiers 1 to 3 here and records their registry entries. A tier-4 image is
specified here only by its requirements and becomes Setup phases of the implementation plan,
where `coder` chooses its base image, resolves its versions, writes its recipe, and builds it.

# Requirements

List what each image must provide:

- the packages and tools of the increment's steps, with the version that the methods document
  fixes, if any;
- the support packages that the implementation plan declares for the increment or the input
  checks;
- the test framework and the linter that the Tech Stack of `{Agents_file}` declares for the
  language of the increment or of the input checks, and rmarkdown and Pandoc for a report
  increment; when it declares none for the language of either, stop and report it;
- for the input checks, the tools that read each input format, such as `samtools` for BAM
  headers.

An increment runs in one image, so all its requirements must be in that image.

# Tiers

Try the tiers in this order and stop at the first that provides every requirement:

1. **Project registry**: an entry of `{Analysis_Images_file}`.
2. **BioContainers**: a single-package image of a Bioconda package.
3. **Seqera Containers**: an image built on request for a combination of Conda or PyPI packages.
4. **Recipe**: an image that `coder` builds from a recipe.

When the Tech Stack of `{Agents_file}` declares a version of the language of the increment or of
the input checks, such as `R 4.4`, an image of tiers 1 to 3 qualifies only when its language
runtime has that version: the same major.minor, such as any `4.4.Z` for `R 4.4`, or the exact
version when the Tech Stack gives one. The registry entry's Contents show it for tier 1, and the
package's language dependency in the index, such as `r-base >=4.4,<4.5.0a0`, for tier 2; a
tier-3 request includes the language at that version, such as `conda-forge::r-base=4.4`. When no
candidate of a tier matches, or its version cannot be shown, go to the next tier as for a missing
package.

Versions:

- A registry image that already has the package wins even without its latest version, unless the
  methods document fixes another version.
- A new image of tiers 2 and 3 uses the latest version available in the package index, or the
  version that the document fixes, compatible with the other packages of the image.
- A tier-4 image gets no version here except those that the document fixes; `coder` resolves the
  others when it builds the image.
- Resolve each version once, at planning or, for tier 4, at the build; replanning keeps it unless
  the document fixes a new one.

## 1. Project registry

Compare the requirements with the Contents of the registry entries. When Contents do not settle
whether a package or tool is present, check it with a read-only command in the image under the
execution rules in `{Agents_file}`, for example:

    apptainer exec <image> Rscript -e 'packageVersion("coloc")'
    apptainer exec <image> samtools --version

Never execute anything else in an image.

## 2. BioContainers

Query the public indexes below with package names only. Conda names are lower case: Bioconductor
packages are `bioconductor-<name>` in Bioconda, CRAN packages are `r-<name>` in conda-forge and
sometimes in Bioconda, and other tools usually keep their name.

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

A BioContainers image holds one package and its dependencies, so it fits only when that package
covers every requirement, including the test framework and the linter.

## 3. Seqera Containers

Request one image with every requirement as Conda or PyPI packages, each with its channel and
version, through the Wave CLI. Add `--singularity` for an Apptainer image:

    wave --freeze --await --conda-package bioconda::<conda-name>=<version> --conda-package conda-forge::<conda-name>=<version>

A request triggers a build in the Seqera service that may take several minutes; wait for it with
`--await`. The images are public, at `community.wave.seqera.io`, and the same packages always
return the same image. Record the URI that the request returns and its manifest digest from the
registry. When the build fails, for example because the packages conflict, use tier 4. When the
Wave CLI is not available, report it and use tier 4; the user can install it or request the image
at `https://seqera.io/containers/`. A missing Wave CLI is never a stop condition.

## 4. Recipe

When no tier provides every requirement, specify the image for the implementation plan by its
requirements only: every package, without a version except those that the methods document
fixes, the test framework and the linter, rmarkdown and Pandoc for a report increment, and the
recipe path in `{Analysis_Recipes_Folder}`. Do not choose a base image, resolve versions, write
the recipe, or build the image.

# Registry entries

A registry image keeps its ID; give each new image an ID as the registry template defines. Add a
registry entry, with its digest, for each new tier-2 and tier-3 image. Tier-4 entries are added by
`coder` after it builds the image.

# Output

Return one record per image:

```yaml
- id: <image ID>
  tier: <1 | 2 | 3 | 4>
  image: <URI, or recipe path for tier 4>
  digest: <sha256:..., or registry for tier 4>
  contents: <packages with versions, or for tier 4 without versions except those that the document fixes; test framework; linter; rmarkdown and Pandoc>
  used_by: <increments and input checks>
  entry_added: <true | false>
```

When the Wave CLI was not available, also report it with the images it sent to tier 4, so that the
implementation plan or `engineer`'s output records it.

# Prohibited

- Building images locally, writing or modifying recipes, or modifying registry entries.
- Running commands other than the package-presence checks on registry images, the read-only
  queries above, Seqera Containers requests, and the sha256 of a local image file.
- Sending project data, such as paths, sample names, or file contents, to any external service;
  queries and requests carry package names and versions only.
