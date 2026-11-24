---
name: building-container-images
description: Write the recipe of a tier-4 container image of an analysis implementation plan, build the image, and add its registry entry. Use for coder's `image-build` phase. Never modify tests, image checks, or existing registry entries.
---

# Purpose

Turn the tier-4 image that a `coder: image-build` marker names into a versioned recipe, a built
image, and its entry in the project registry, so that tester's image check for that image passes.

# Inputs

Resolve global placeholders from `{Agents_file}`. Read:

- the image's row in the implementation plan's Images table: its ID, its recipe path in
  `{Analysis_Recipes_Folder}`, and its Contents, with the base image, every package and its
  version, the test framework, the linter, and rmarkdown and Pandoc when listed;
- `{Agents_Folder}/references/templates/container-images.template.md` and `{Analysis_Images_file}`;
- the execution rules in `{Agents_file}`, which declare whether the project runs images with
  Apptainer or Docker.

Stop and report when a placeholder cannot be resolved, when `{Analysis_Images_file}` already has
an entry with the image ID, or when `git check-ignore` shows that `{Analysis_Images_Folder}` is
not ignored by Git.

# Workflow

1. **Recipe.** Write the recipe at the implementation plan's recipe path: an Apptainer definition
   file or a Dockerfile, as the execution rules declare. Start from the base image with its tag
   or digest, and install every package of Contents at its exact version with the package manager
   of its ecosystem. Install nothing else beyond their dependencies, and copy no project file.
2. **Build.** Build the image file `{Analysis_Images_Folder}/<ID>.<ext>`, from an empty build
   context so that no project file reaches the builder:
   - Apptainer: `apptainer build --fakeroot {Analysis_Images_Folder}/<ID>.sif <recipe>`;
   - Docker: `docker build --tag <ID> --file <recipe> <empty folder>`, then
     `docker save --output {Analysis_Images_Folder}/<ID>.tar <ID>`.
3. **Verify.** Before registering the image, check every item of Contents with read-only
   commands in the image, such as `packageVersion("DESeq2")` or `samtools --version`. When an
   item is missing or has another version, fix the recipe and rebuild; never change a version of
   the implementation plan.
4. **Register.** Compute the sha256 of the image file with `sha256sum` and add one entry under
   the image ID, as the registry template defines: the image file path, `sha256:<digest>`,
   source `recipe`, the recipe path, and the Contents.
5. **GREEN.** Run tester's image check for the image and report its result.

# Stops

- **Missing permissions.** When the build fails because the user cannot build images, such as
  `fakeroot` not being enabled for Apptainer or no access to the Docker daemon, stop without
  retrying and state what to ask the administrator for: Apptainer `fakeroot` for the user, with
  its `/etc/subuid` and `/etc/subgid` entries, or access to Docker, such as membership of the
  `docker` group or rootless Docker. Also stop when the build tool is not installed.
- **Unavailable version.** When a package version of Contents cannot be installed, stop and report
  it; the implementation plan owns versions.
- **Failed check.** When tester's image check fails after the entry is added, stop and report it;
  never modify the entry.

# Boundaries

- Never create, modify, or delete tests, image checks, or test support code.
- Never modify or remove a registry entry, an existing image file, or the recipe of another image.
  A rebuild of a registered image needs a new ID from the implementation plan.
- Never send project data to an external service or into an image; the build downloads only the
  base image and packages.
- Never commit; Git commands are limited to read-only checks.

# Output

Return the recipe path, the build command and result, the image file path and its sha256, the
registry entry added, the verification commands and results, and the image check's command and
result, or the stop with what to ask the administrator for.
