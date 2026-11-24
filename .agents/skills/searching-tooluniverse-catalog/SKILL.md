---
name: searching-tooluniverse-catalog
description: Search the local ToolUniverse catalog for candidate methods. Use once, at the start, before designing the methods of an analysis methods document, when `{Agents_file}` declares `ToolUniverse_CLI`. Read-only catalog queries; never run tools.
---

# Purpose

Find candidate methods for an analysis in the ToolUniverse catalog and translate them to the
original methods a methods document can cite. The catalog is advisory: the methods document never
depends on ToolUniverse and never mentions it.

# Workflow

## 1. Check availability

`ToolUniverse_CLI` in `{Agents_file}` is the path of the `tu` executable. If the key is absent,
or `"<ToolUniverse_CLI>" --version` fails, do not use the catalog: tell the user and continue
without it. Never install or configure anything.

## 2. List the operations

From the scientific question and the inputs, list the main analysis operations, for example
differential expression or colocalization. Do not define methods steps yet. A method the user
explicitly requests is fixed.

## 3. Search the catalog

Run one query at a time, and wait for its result before the next:

    "<ToolUniverse_CLI>" find "<operation in natural language>" --limit 10
    "<ToolUniverse_CLI>" grep <term> --field description
    "<ToolUniverse_CLI>" list --categories
    "<ToolUniverse_CLI>" info <ToolName>

Use `find` and `grep` for each operation, `list` to explore categories, and `info` for promising
candidates; it gives the description, the underlying method and citation, the parameters with
their defaults, and examples. A few searches per operation are enough; do not exhaust synonyms or
justify each rejected candidate.

## 4. Translate candidates to original methods

For each useful candidate, record the original method as `package::function` and its reference.
Some tools reimplement a method, for example a pure-Python port of an R function: cite the
original package, and verify its parameters and defaults in that package's documentation, since
the port may differ. A method available only as a ToolUniverse tool, such as a remote model or a
web API, may be mentioned to the user as an option, but it never enters the methods document.

# Output

Return a short YAML in the conversation; do not save it to a file. `data-analyst` uses it to
propose the methods to the user. The methods document cites only the method and its reference.

```yaml
- operation: <analysis operation>
  candidates:
    - tool: <ToolUniverse name>
      method: <original method: package::function, reference>
      fit: <one line: why it fits or not>
  proposal: <proposed method, or "none from catalog">
```

# Prohibited

- Running any subcommand other than `--version`, `find`, `grep`, `info`, and `list`, such as
  `run`, `test`, `serve`, `connect`, `remote`, `build`, `doctor`, or `status`.
- Installing or configuring ToolUniverse or any other package.
