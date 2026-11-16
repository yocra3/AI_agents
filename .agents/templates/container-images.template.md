# Container image registry template

Use this template for `{Analysis_Images_file}`, the project's registry of the container images
that analysis increments run in. An increment names an image by its ID in its `Image` field.

```markdown
# Container images

## <ID, e.g. r-v1.0>

- **Image**: `<image URI or path to the image file>`
- **Digest**: `sha256:<digest>`
- **Recipe**: `<path to the recipe>`
- **Contents**: `<language and version>`; `<key packages with versions>`; tests: `<framework>`;
  lint: `<linter>`; `<rmarkdown and Pandoc versions, if present>`
```

## Rules

- One entry per image, with a unique ID made of a short name and a version, such as `r-v1.0`.
- Add an entry only once the image is built and its digest is known: the manifest digest of a
  registry image, or the sha256 of a local image file.
- Never modify or remove an entry. A rebuilt image gets a new ID and a new entry.
- An image used by an increment provides the tools of every increment that names it and, for
  their language, the test framework and the linter. The image of a report increment also
  provides rmarkdown and Pandoc.
- `data_analyst` maintains this registry. It may compute the sha256 of a local image file, a
  read-only operation, but never modifies recipes or builds images; the user does.
