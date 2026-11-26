---
name: building-container-images
description: Choose the base image and resolve the package versions of a tier-4 container image of an analysis implementation plan, write its pinned recipe, build the image, and add its registry entry with the installed versions. Use for coder's `image-build` phase. Never modify tests, image checks, or committed registry entries.
---

# Purpose

Turn the tier-4 image that a `coder: image-build` marker names into a versioned recipe that pins
its base image and every package version, a built image, and its entry in the project registry
with the versions installed, so that tester's image check for that image passes.

# Inputs

Resolve global placeholders from `{Agents_file}`. Read:

- the image's row in the implementation plan's Images table: its ID, its recipe path in
  `{Analysis_Recipes_Folder}`, and its Contents: every package, without a version except those
  that the methods document fixes, the test framework, the linter, and rmarkdown and Pandoc when
  listed;
- [references/base-images.md](references/base-images.md), which defines the base images, the
  version rules, and how to pin both;
- `{Agents_Folder}/references/templates/container-images.template.md` and `{Analysis_Images_file}`;
- the Tech Stack of `{Agents_file}`, for the version of the language when it declares one, and
  its execution rules, which declare whether the project runs images with Apptainer or Docker.

Stop and report when a placeholder cannot be resolved, when `{Analysis_Images_file}` already has
a committed entry with the image ID, or when `git check-ignore` shows that
`{Analysis_Images_Folder}` is not ignored by Git.

# Workflow

To resolve versions and to build, run the package manager and the build in the chosen base image
with the container runtime of the execution rules in `{Agents_file}`; send outside only image
names, tags, and package names, and never mount project data, for example with Apptainer's
`--containall`.

On a retry, first remove the uncommitted entry and the image file that the failed attempt added
under the image ID, as the registry rules allow; `git diff` shows the entry as uncommitted.

1. **Base image.** Choose the base image of the image's ecosystem, its latest stable tag, and
   that tag's digest, as the reference defines them.
2. **Versions.** Resolve the version of every package with the package manager of its ecosystem,
   as the reference defines it: each version that the methods document fixes exactly, and the
   latest stable release compatible with them for every other package.
3. **Recipe.** Write the recipe at the implementation plan's recipe path: an Apptainer definition
   file or a Dockerfile, as the execution rules declare. Pin the base image by tag and digest and
   everything resolved, such as the snapshot date, the release, or each exact version, so that a
   rebuild gives the same image. Install every package of Contents and nothing else beyond their
   dependencies, and copy no project file.
4. **Build.** Build the image file `{Analysis_Images_Folder}/<ID>.<ext>`, from an empty build
   context so that no project file reaches the builder:
   - Apptainer: `apptainer build --fakeroot {Analysis_Images_Folder}/<ID>.sif <recipe>`;
   - Docker: `docker build --tag <ID> --file <recipe> <empty folder>`, then
     `docker save --output {Analysis_Images_Folder}/<ID>.tar <ID>`.
5. **Verify.** Before registering the image, read the installed version of the language and of
   every item of Contents with read-only commands in the image, such as
   `packageVersion("DESeq2")` or `samtools --version`. When an item is missing, a version that
   the document fixes differs, or a version differs from the recipe's pin, fix the recipe and
   rebuild; never change a version that the document fixes.
6. **Register.** Compute the sha256 of the image file with `sha256sum` and add one entry under
   the image ID, as the registry template defines: the image file path, `sha256:<digest>`,
   source `recipe`, the recipe path, and the Contents with the versions read in step 5.
7. **GREEN.** Run tester's image check for the image and report its result. When it fails,
   report the failure, leaving the entry and the image file in place; never modify the entry.

# Stops

- **Missing permissions.** When the build fails because the user cannot build images, such as
  `fakeroot` not being enabled for Apptainer or no access to the Docker daemon, stop without
  retrying and state what to ask the administrator for: Apptainer `fakeroot` for the user, with
  its `/etc/subuid` and `/etc/subgid` entries, or access to Docker, such as membership of the
  `docker` group or rootless Docker. Also stop when the build tool is not installed.
- **No base image.** When no base image of the reference fits the image's packages, stop and
  report the packages; the user chooses the base image.
- **Unavailable fixed version.** When a version that the methods document fixes cannot be
  installed, alone or with the other packages, stop and report it; only the user changes it.

# Boundaries

- Never create, modify, or delete tests, image checks, or test support code.
- Never modify or remove a committed registry entry, its image file, or the recipe of another
  image. A rebuild of a registered image needs a new ID from the implementation plan.
- Never modify the implementation plan; `engineer` records the installed versions there from the
  registry entry.
- Never send project data to an external service or into an image; queries and the build
  download only the base image and packages.
- Never commit; Git commands are limited to read-only checks.

# Output

Return the base image with its tag and digest, the resolved versions, the recipe path, the build
command and result, the image file path and its sha256, the registry entry added, the
verification commands and results, and the image check's command and result, or the stop with
what to ask the administrator for or the package that could not be installed.
