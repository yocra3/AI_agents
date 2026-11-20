# Changelog

This file records the changes to the agent definitions of this repository (agents, skills,
templates and the installer) and the upgrade notes for installed projects. `install.py` copies it
into each project with `.agents/VERSION`. It is not the project's own changelog: projects keep
theirs at `{Root_Folder}/CHANGELOG.md`.

Versions follow semantic versioning. The installed version is in `.agents/VERSION`.

## 0.9.0 - 2026-11-20

First versioned state: the agent definitions of commit `68f6dfc` plus the version marker.

### Added

- `.agents/VERSION`, the version of the agent definitions, and this changelog.
- `install.py` shows the source and installed versions with their commit hashes, records the
  version in `.agents/.install-manifest.json`, warns when the version being installed is lower
  than the installed one, and always overwrites `.agents/VERSION` in the target.

### Upgrade notes

- No action is needed. Projects installed before this version have a manifest without a version,
  so this install shows no downgrade warning; it records the version for the next one.
