# Base images and versions of tier-4 images

How building-container-images chooses the base image of a tier-4 image, resolves the versions of
its packages, and pins both in the recipe, so that a rebuild of the recipe gives the same image.

## Base image by ecosystem

Choose the row that fits the packages of the image's Contents:

| Packages | Base image | Package manager | Pinned by |
| --- | --- | --- | --- |
| R, CRAN only | `rocker/r-ver:<X.Y.Z>` | `install.packages()` from a dated Posit Public Package Manager snapshot | the snapshot date |
| R, with Bioconductor | `bioconductor/bioconductor_docker:RELEASE_<X>_<Y>` | `BiocManager::install()`; CRAN packages from a dated snapshot | the Bioconductor release and the snapshot date |
| Python | `python:<X.Y.Z>-slim` | `pip install` | `==` on every package installed |
| A command-line tool that only Bioconda packages | `mambaorg/micromamba:<X.Y.Z>` | `micromamba install` from conda-forge and bioconda | `=<version>` on every package installed |

- Prefer the native package manager of the language over conda. Use the micromamba base only
  when the image needs a command-line tool that only Bioconda packages, and then install every
  package of the image with micromamba.
- When no row fits the image's packages, stop and report it: the user chooses the base image.

## Versions

- **Base image.** Use the latest stable release whose tag matches the pattern exactly and, when
  the Tech Stack of `{Agents_file}` declares a version of the language, that version, such as the
  latest `4.4.Z` for `R 4.4`. Compare versions numerically, not in the order of the tag list.
  Never use a development or pre-release tag, such as `devel`, `3.16.0a2-slim`, or
  `3.16-rc-slim`, a floating tag, such as `latest` or a tag without the full version (`4.5`,
  `3.15-slim`), or a tag that adds a variant to the pattern, such as `-cuda` or `-R-4.6.1`.
- **Packages.** Install the latest stable release that the pinned source provides and that is
  compatible with the other packages. Never use development versions or channels, pre-releases,
  such as pip's `--pre`, or a package from an untagged commit or branch of a repository.
- **Fixed versions.** Install a version that the methods document fixes exactly, and give every
  other package the latest stable release compatible with it.
- **Resolution.** Resolve the versions with the package manager against the pinned source: from
  a dry run where the manager has one, otherwise from a first build in which only the fixed
  versions are pinned, reading the installed versions in the image. Then pin every resolved
  version in the recipe.
- **Base pin.** Pin the base image by tag and digest: in a Dockerfile,
  `FROM <image>:<tag>@sha256:<digest>`; in an Apptainer definition file, `Bootstrap: docker` and
  `From: <namespace>/<name>:<tag>@sha256:<digest>`.

## R from CRAN

- Rocker builds `rocker/r-ver` on Ubuntu LTS and sets its `CRAN` variable to the Posit Public
  Package Manager binaries of that Ubuntu release: a dated snapshot, such as
  `https://p3m.dev/cran/__linux__/noble/2026-04-23`, for every R release except the latest, and
  the same URL ending in `latest` for the latest.
- Use the image's dated snapshot; when its `CRAN` ends in `latest`, replace `latest` with the build
  date. For a date without a snapshot, Package Manager serves the nearest older one. Pass the URL
  as `repos` to every `install.packages()` call.
- When the document fixes the version of a CRAN package, use the latest snapshot date that still
  serves that version and is compatible with the R release.
- For Pandoc, Rocker images include `/rocker_scripts/install_pandoc.sh <version>`, which installs
  that release of `jgm/pandoc`. Give it the release that
  `https://api.github.com/repos/jgm/pandoc/releases/latest` returns in `tag_name`, the latest
  stable release, never `latest` or `default`.

## R with Bioconductor

- The Bioconductor images build on the Rocker images. `BiocManager::install()` installs the
  packages of the image's Bioconductor release, as binary packages inside the container.
- Use the latest `RELEASE_<X>_<Y>` whose R release meets the Tech Stack, or, when the document
  fixes the version of a Bioconductor package, the latest release that provides it.
- Set the `CRAN` entry of `options(repos)` to a dated snapshot as for `rocker/r-ver`, for the
  Ubuntu release of the image; BiocManager uses `getOption("repos")` in place of its standard
  repositories. Install Pandoc as for `rocker/r-ver`.
- Bioconductor can publish patch versions within a release, so the registry entry's Contents,
  read from the built image, are the record of what it installs.

## Python

- The `slim` variant has only the Debian packages that Python needs; a package that pip must
  compile from source may need build packages, which the recipe then installs with `apt-get`.
- Resolve the versions with pip in the base image:
  `pip install --dry-run --ignore-installed --report - <packages>`. pip selects only stable
  releases unless `--pre` is given. Pin every package of the report with `==`.

## Command-line tools from Bioconda

- `mambaorg/micromamba` tags that do not contain `git` are rolling, so the digest is what fixes
  the image.
- Install with `micromamba install -y -n base`, from the channels `conda-forge` and `bioconda`,
  and end with `micromamba clean --all --yes`.

## Tags and digests

The four base images are on Docker Hub. Query their tags and digests with the registry API, with
an anonymous pull token:

    curl -s 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:<namespace>/<name>:pull'
    curl -s -H 'Authorization: Bearer <token>' 'https://registry-1.docker.io/v2/<namespace>/<name>/tags/list?n=1000'
    curl -sI -H 'Authorization: Bearer <token>' \
      -H 'Accept: application/vnd.oci.image.index.v1+json' \
      -H 'Accept: application/vnd.docker.distribution.manifest.list.v2+json' \
      -H 'Accept: application/vnd.oci.image.manifest.v1+json' \
      -H 'Accept: application/vnd.docker.distribution.manifest.v2+json' \
      'https://registry-1.docker.io/v2/<namespace>/<name>/manifests/<tag>'

- The token is the `token` field of the first response and expires after its `expires_in`
  seconds, 60 by default; request a new one when a query returns HTTP 401.
- Docker official images, such as `python`, have the namespace `library`: `library/python`.
- The tag list is `{"name": ..., "tags": [...]}`. `n` limits its length; `last=<tag>` continues
  after that tag.
- The digest to pin is the `Docker-Content-Digest` header of the manifest response.
- Send only image names and tags; never project data.

## Sources

- Docker, Dockerfile best practices, "Pin base image versions":
  https://docs.docker.com/build/building/best-practices/
- Docker, registry token authentication: https://docs.docker.com/reference/api/registry/auth/
- Docker, registry mirror (`registry-1.docker.io`):
  https://docs.docker.com/docker-hub/image-library/mirror/
- OCI Distribution Specification, listing tags and pulling manifests:
  https://github.com/opencontainers/distribution-spec/blob/main/spec.md
- OCI Image Specification, media types:
  https://github.com/opencontainers/image-spec/blob/main/media-types.md
- Apptainer, definition file bootstrap agents (`From`, default namespace `library`):
  https://apptainer.org/docs/user/latest/appendix.html
- Rocker, `rocker/r-ver`: https://rocker-project.org/images/versioned/r-ver.html, and its
  Dockerfiles and scripts (`CRAN`, `install_pandoc.sh`):
  https://github.com/rocker-org/rocker-versioned2
- Posit Package Manager, snapshot date aliases:
  https://docs.posit.co/rspm/admin/repositories.html
- Bioconductor, Docker images: https://www.bioconductor.org/help/docker/
- BiocManager, `repositories()`: https://bioconductor.github.io/BiocManager/reference/repositories.html
- Docker Hub, `python` official image: https://hub.docker.com/_/python
- pip, `pip install` (`--dry-run`, `--report`, `--pre`): https://pip.pypa.io/en/stable/cli/pip_install/
- micromamba-docker, quick start and tags:
  https://micromamba-docker.readthedocs.io/en/latest/quick_start.html and
  https://micromamba-docker.readthedocs.io/en/latest/tags.html
- GitHub REST API, latest release:
  https://docs.github.com/en/rest/releases/releases#get-the-latest-release
