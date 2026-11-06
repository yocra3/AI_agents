#!/usr/bin/env python3
"""Install or update the agent definitions in a target Git repository.

The script copies the committed `.agents`, `.claude` and `.codex` files into the target and
records each one with its SHA-256 in `.agents/.install-manifest.json`. On the next run it compares
three versions of each file (this repository, the manifest, and the target) to decide whether to
add, update, delete or keep it. Files that are not in the manifest belong to the target project
and are never touched.

Both repositories must have no uncommitted changes in those folders, so every change the script
makes in the target can be reviewed with `git diff` and reverted with `git checkout`.

Usage: python3 install.py [--dry-run] [--yes] TARGET
Compatible with Python 3.6.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

MANAGED_DIRS = (".agents", ".claude", ".codex")
SKILLS_LINK = ".claude/skills"
SKILLS_LINK_TARGET = "../.agents/skills"
LOCAL_CONFIG = (".claude/settings.json", ".codex/config.toml")  # installed only when absent
MANIFEST = ".agents/.install-manifest.json"
# Folders listed as unmanaged leftovers when a target has no manifest yet.
LEGACY_SCAN_DIRS = (".agents/skills", ".agents/templates", ".codex/agents", ".claude/agents",
                    ".claude/scripts")

SOURCE = os.path.dirname(os.path.abspath(__file__))

LABELS = [
    ("add", "New files to add"),
    ("update", "Files to update"),
    ("delete", "Files removed upstream, to delete"),
    ("conflict", "Changed here and in the target, to overwrite (review with git diff)"),
    ("modified-locally", "Changed only in the target, kept"),
    ("deleted-locally", "Deleted in the target, kept deleted"),
    ("kept-removed", "Removed upstream but changed in the target, kept as project files"),
    ("config-differs", "Local configuration that differs, review by hand (never overwritten)"),
    ("unmanaged", "Not installed by this script (project files or leftovers of an older "
                  "install), not touched"),
]
CHANGES = ("add", "update", "delete", "conflict")


def git(repo, *args):
    """Run git in repo and return its stripped output, or None when git fails."""
    try:
        result = subprocess.run(["git", "-C", repo] + list(args), stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, universal_newlines=True)
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def require_clean(repo, name, allow_changes=False):
    """Stop unless repo is a Git work tree with no uncommitted changes in the managed folders."""
    if git(repo, "rev-parse", "--is-inside-work-tree") != "true":
        sys.exit("install: %s is not a Git repository" % repo)
    pending = git(repo, "status", "--porcelain", "--", *MANAGED_DIRS)
    if pending and not allow_changes:
        sys.exit("install: uncommitted changes in %s; commit or stash them first:\n%s"
                 % (name, pending))


def file_hash(path):
    """Return the SHA-256 of a regular file, or None when it is absent or a link."""
    if not os.path.isfile(path) or os.path.islink(path):
        return None
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def tracked_files(repo, dirs):
    """Return {relative path: hash} for the files Git tracks below dirs, without links."""
    files = {}
    # Not stripped by git(): -z output keeps file names that begin or end with spaces intact.
    listing = subprocess.run(["git", "-C", repo, "ls-files", "-z", "--"] + list(dirs),
                             stdout=subprocess.PIPE, universal_newlines=True).stdout
    for rel in listing.split("\0"):
        if rel and rel != MANIFEST:
            digest = file_hash(os.path.join(repo, rel))
            if digest is not None:
                files[rel] = digest
    return files


def plan(target, source_files, old_files, legacy):
    """Classify every file and return a list of (action, rel) tuples."""
    actions = []
    for rel in sorted(set(source_files) | set(old_files)):
        src = source_files.get(rel)
        old = old_files.get(rel)
        local = file_hash(os.path.join(target, rel))
        if rel in LOCAL_CONFIG:
            action = "add" if local is None else "config-differs" if local != src else None
        elif src is None:
            action = None if local is None else "delete" if local == old else "kept-removed"
        elif local is None:
            action = "add" if old is None else "deleted-locally"
        elif local == src:
            action = None
        elif local == old:
            action = "update"
        elif src == old:
            action = "modified-locally"
        else:
            action = "conflict"
        if action:
            actions.append((action, rel))
    if legacy:
        leftovers = set(tracked_files(target, LEGACY_SCAN_DIRS)) - set(source_files)
        actions.extend(("unmanaged", rel) for rel in sorted(leftovers))
    return actions


def summarize(actions, old_version, new_version):
    """Print the planned actions and return the number of files that will change."""
    print("Source version: %s" % new_version)
    print("Installed version: %s" % (old_version or "none (no manifest)"))
    for key, label in LABELS:
        rels = [rel for action, rel in actions if action == key]
        if rels:
            print("\n%s (%d):" % (label, len(rels)))
            print("\n".join("  " + rel for rel in rels))
    return sum(1 for action, _ in actions if action in CHANGES)


def remove_empty_parents(target, rel):
    parent = os.path.dirname(os.path.join(target, rel))
    while os.path.relpath(parent, target) not in MANAGED_DIRS and not os.listdir(parent):
        os.rmdir(parent)
        parent = os.path.dirname(parent)


def apply(target, actions):
    for action, rel in actions:
        path = os.path.join(target, rel)
        if action in ("add", "update", "conflict"):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            shutil.copy2(os.path.join(SOURCE, rel), path)
        elif action == "delete":
            os.remove(path)
            remove_empty_parents(target, rel)


def link_skills(target):
    """Make the skills in `.agents/skills` visible to Claude Code in `.claude/skills`.

    Link the whole folder when `.claude/skills` does not exist. When the project already has it as
    a real folder, link each missing skill inside it instead and remove the links of skills that
    no longer exist; the project's own skills there are left alone.
    """
    link = os.path.join(target, SKILLS_LINK)
    if not os.path.lexists(link):
        os.symlink(SKILLS_LINK_TARGET, link)
        return
    if os.path.islink(link) or not os.path.isdir(link):
        if not os.path.islink(link) or os.readlink(link) != SKILLS_LINK_TARGET:
            print("warning: %s is not a folder or a link to %s; Claude Code may not see the "
                  "skills" % (SKILLS_LINK, SKILLS_LINK_TARGET))
        return
    skills = os.path.join(target, ".agents", "skills")
    for name in sorted(os.listdir(skills)):
        entry = os.path.join(link, name)
        if os.path.isdir(os.path.join(skills, name)) and not os.path.lexists(entry):
            os.symlink("../" + SKILLS_LINK_TARGET + "/" + name, entry)
            print("Linked %s/%s" % (SKILLS_LINK, name))
        elif os.path.lexists(entry) and not os.path.islink(entry):
            print("warning: %s/%s is a project folder; the skill of the same name in "
                  ".agents/skills is not linked" % (SKILLS_LINK, name))
    for name in sorted(os.listdir(link)):
        entry = os.path.join(link, name)
        if (os.path.islink(entry) and os.readlink(entry).startswith("../" + SKILLS_LINK_TARGET)
                and not os.path.exists(entry)):
            os.remove(entry)
            print("Removed the link %s/%s of a skill that no longer exists" % (SKILLS_LINK, name))


def main():
    parser = argparse.ArgumentParser(description="Install or update the agent definitions.")
    parser.add_argument("target", help="path to the target Git repository")
    parser.add_argument("--dry-run", action="store_true", help="show the changes and exit")
    parser.add_argument("--yes", action="store_true", help="apply without confirmation")
    args = parser.parse_args()

    target = os.path.abspath(args.target)
    if not os.path.isdir(target):
        sys.exit("install: %s is not a directory" % target)
    if os.path.realpath(target) == os.path.realpath(SOURCE):
        sys.exit("install: the target is this repository")
    require_clean(SOURCE, "this repository")
    require_clean(target, "the target", allow_changes=args.dry_run)

    manifest_path = os.path.join(target, MANIFEST)
    manifest = None
    if os.path.isfile(manifest_path):
        with open(manifest_path) as fh:
            manifest = json.load(fh)

    old_files = manifest["files"] if manifest else {}
    new_version = git(SOURCE, "rev-parse", "--short", "HEAD")
    source_files = tracked_files(SOURCE, MANAGED_DIRS)
    actions = plan(target, source_files, old_files, manifest is None)
    changes = summarize(actions, manifest and manifest["source_version"], new_version)

    if args.dry_run:
        return
    if changes == 0 and manifest is not None and os.path.lexists(os.path.join(target, SKILLS_LINK)):
        print("\nNothing to update.")
        return
    if not args.yes:
        try:
            answer = input("\nApply these changes? [y/N] ").strip().lower()
        except EOFError:
            answer = ""
        if answer != "y":
            sys.exit("install: cancelled, nothing changed")

    apply(target, actions)
    link_skills(target)
    with open(manifest_path, "w") as fh:
        json.dump({"source_version": new_version,
                   "files": {rel: digest for rel, digest in source_files.items()
                             if rel not in LOCAL_CONFIG}},
                  fh, indent=2, sort_keys=True)
        fh.write("\n")

    print("\nInstalled %s." % new_version)
    if any(action == "conflict" for action, _ in actions):
        print("Overwritten files changed in the target: review them with `git diff` and restore "
              "your version with `git checkout -- <file>`.")
    if manifest is None:
        print("Next: generate AGENTS.md with the project-bootstrap skill and add a CLAUDE.md "
              "(see README.md).")


if __name__ == "__main__":
    main()
