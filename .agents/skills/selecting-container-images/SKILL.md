---
name: selecting-container-images
description: Select the container image of each increment and of the input checks of an analysis implementation plan, in tier order from the project registry, BioContainers, and Seqera Containers, and specify a recipe when none fits. Use from planning-analysis while engineer plans a methods document. Never build images locally or write recipes.
---

# Purpose

Give every increment of the implementation plan, and its input checks, one image that provides
all their tools, following the rules of `{Agents_Folder}/templates/container-images.template.md`.
`engineer` resolves tiers 1 to 3 here and records their registry entries; a tier-4 image becomes
Setup phases of the plan, where `coder` writes its recipe and builds it.

# Requirements

List what each image must provide:

- the packages and tools of the increment's steps, with the version that the methods document
  fixes, if any;
- the test framework and the linter of the increment's language, and rmarkdown and Pandoc for a
  report increment;
- for the input checks, the tools that read each input format, such as `samtools` for BAM
  headers.

An increment runs in one image, so all its requirements must be in that image.

# Tiers

Try the tiers in this order and stop at the first that provides every requirement:

1. **Project registry**: an entry of `{Analysis_Images_file}`.
2. **BioContainers**: a single-package image of a Bioconda package.
3. **Seqera Containers**: an image built on request for a combination of Conda or PyPI packages.
4. **Recipe**: an image that `coder` builds from a recipe.

Versions:

- A registry image that already has the package wins even without its latest version, unless the
  methods document fixes another version.
- A new image, of tiers 2 to 4, uses the latest version available in the package index, or the
  version that the document fixes, compatible with the other packages of the image.
- Resolve each version once, at planning; replanning keeps it unless the document fixes a new one.

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

When no tier provides every requirement, specify the image for the plan: a base image, every
package with its version, and the recipe path in `{Analysis_Recipes_Folder}`. Do not write the
recipe or build the image.

# Registry entries

Give each image an ID made of a short name and a version, such as `r-deseq2-v1`. Add a registry
entry, with its digest, for each new tier-2 and tier-3 image, as the registry template defines.
Never modify or remove an entry. Tier-4 entries are added by `coder` after it builds the image.

# Output

Return one record per image:

```yaml
- id: <image ID>
  tier: <1 | 2 | 3 | 4>
  image: <URI, or recipe path for tier 4>
  digest: <sha256:..., or registry for tier 4>
  contents: <base for tier 4; packages with versions; test framework; linter; rmarkdown and Pandoc>
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
