# Container image registry template

Use this template for `{Analysis_Images_file}`, the project's registry of the container images
that analysis increments and input checks run in. An implementation plan names an image by its
ID.

```markdown
# Container images

## <ID, e.g. r-deseq2-v1>

- **Image**: `<image URI, or path to the image file in {Analysis_Images_Folder}>`
- **Digest**: `sha256:<digest>`
- **Source**: `<BioContainers | Seqera Containers | recipe>`
- **Recipe**: `<path to the recipe in {Analysis_Recipes_Folder}, or not-applicable>`
- **Contents**: `<language and version>`; `<key packages with versions>`; tests: `<framework>`;
  lint: `<linter>`; `<rmarkdown and Pandoc versions, if present>`
```

## Rules

- One entry per image, with a unique ID made of a short name and a version, such as
  `r-deseq2-v1`.
- Add an entry only once the image exists and its digest is known: the manifest digest of a
  registry image, or the sha256 of a local image file.
- `engineer` adds the entries of the images it selects from BioContainers and Seqera Containers
  while planning, tiers 2 and 3; tier-1 images already have their entry.
- `coder` adds the entry of a tier-4 image after building it in `coder: image-build`, with the
  image ID of the implementation plan and the sha256 of the image file.
- Never modify or remove an entry. A rebuilt image gets a new ID and a new entry.
- Recipes are versioned in `{Analysis_Recipes_Folder}`. Built image files are kept in
  `{Analysis_Images_Folder}`, which Git ignores.
- An image provides the tools of every increment that names it and, for their language, the test
  framework and the linter. The image of a report increment also provides rmarkdown and Pandoc,
  and the image of the input checks provides the tools that read each input format.
