# Conventional Commits

Commit message rules of the commit-changes skill, following
[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

```txt
<type>[(<scope>)][!]: <description>

[body]

[footers]
```

## Type

The type of what the commit changes:

- `feat`: a new feature or capability.
- `fix`: a bug fix.
- `test`: tests added or fixed, with no change to the code under test.
- `perf`: a performance improvement.
- `refactor`: a code change with no behavior change.
- `style`: formatting only, such as whitespace or layout.
- `docs`: documentation only.
- `build`: the build system, images, or dependencies.
- `ci`: continuous integration configuration.
- `chore`: other maintenance that touches neither code nor tests.
- `revert`: reverts earlier commits, named in a `Refs:` trailer by hash.

## Scope

Optional and lowercase with hyphens; there is no closed list.

- Commits of a contract run by implementation-coordinator: the contract identifier,
  `<spec-slug-id>` or `<analysis-id>`, for every commit of that contract, from approval, plan,
  and replanning through Removed entries, steps, increments, Setup, Finalization, and status.
- Other commits: the area that changes, such as a module, a component, or a top-level folder of
  the project; omit it when the change spans the project or has no clear area.

## Description

English, imperative, lowercase, with no final period. The whole header is at most 72 characters,
ideally about 50.

## Body

What changes and why, not how, wrapped at 72 characters per line.

## Footers

- A breaking change adds `!` before the colon and a
  `BREAKING CHANGE: <what changes and what an upgrader must do>` footer.
- Trailers, such as `Refs: <issue or hash>` and `Co-Authored-By: <name> <email>`, go last, one
  per line.

## Examples

A contract commit:

```txt
feat(analysis-rna-velocity): add spliced read counts

Count spliced and unspliced reads per cell with the pinned image, as
the methods document requires for the velocity model.
```

A commit outside a contract:

```txt
fix(parser)!: reject sheets without a condition column

Sheets without the column produced an empty design and a silent
failure in the model step.

BREAKING CHANGE: every sample sheet needs a condition column; add one
before rerunning.
```
