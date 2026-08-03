#!/usr/bin/env python3
"""Prune stale SNAPSHOT/RC chart packages from the snapshot/ Helm repository.

Retention policy (union of two rules, a package survives if EITHER holds):
  1. it is among the N newest builds of its chart, per pre-release kind
     (SNAPSHOT and RC are ranked independently);
  2. it was added to git less than MAX_AGE_DAYS ago.

Packages under stable/ are release artifacts and are never touched.

The index.yaml is edited surgically -- entry blocks for pruned versions are
removed and every surviving byte is preserved -- rather than regenerated with
`helm repo index`, so that digests, creation timestamps and annotations of
charts that remain published stay exactly as they were first served.

Usage:
    python3 scripts/prune-snapshots.py [--apply] [--keep N] [--max-age-days D]

Without --apply the script only reports what it would delete.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date, timedelta

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGES_DIR = os.path.join(REPO_ROOT, "snapshot", "packages")
INDEX_FILE = os.path.join(REPO_ROOT, "snapshot", "index.yaml")

DEFAULT_KEEP = 5
DEFAULT_MAX_AGE_DAYS = 183

# <chart>-<major>.<minor>.<patch>-<KIND>.<build>.tgz, where KIND may itself
# carry a branch qualifier (e.g. 2.11.0-MDTU-DDM-SNAPSHOT.2).
PACKAGE_RE = re.compile(
    r"^(?P<chart>.+?)-(?P<version>\d+\.\d+\.\d+)-(?P<qualifier>.*?)"
    r"(?P<kind>SNAPSHOT|RC)\.(?P<build>\d+)\.tgz$"
)


def parse_package(filename: str):
    """Return a sort key for a package filename, or None if it is not a pre-release."""
    m = PACKAGE_RE.match(filename)
    if not m:
        return None
    return {
        "chart": m.group("chart"),
        # The branch qualifier makes e.g. MDTU-DDM builds a separate release
        # line from mainline ones, so they are ranked in their own bucket.
        "group": (m.group("chart"), m.group("qualifier"), m.group("kind")),
        "order": (
            tuple(int(p) for p in m.group("version").split(".")),
            int(m.group("build")),
        ),
        "version": f"{m.group('version')}-{m.group('qualifier')}{m.group('kind')}.{m.group('build')}",
    }


def git_add_dates(path_prefix: str) -> dict[str, str]:
    """Map repo-relative path -> ISO date of the commit that first added it.

    Falls back to an empty map on a repository without history (e.g. a freshly
    squashed branch), in which case the age rule simply never fires and
    retention is decided by the keep-newest-N rule alone.
    """
    out = subprocess.run(
        [
            "git", "-C", REPO_ROOT, "log", "--diff-filter=A",
            "--name-only", "--format=%H %ad", "--date=short", "--", path_prefix,
        ],
        capture_output=True, text=True, check=True,
    ).stdout

    dates: dict[str, str] = {}
    current: str | None = None
    for line in out.splitlines():
        if re.match(r"^[0-9a-f]{40} ", line):
            current = line.split()[1]
        elif line.strip() and current:
            # git log walks newest-first, so later assignments are older commits.
            dates[line.strip()] = current
    return dates


def select(files: list[str], keep: int, max_age_days: int, add_dates: dict[str, str]):
    """Split package filenames into (keep, delete, skipped-not-a-prerelease)."""
    cutoff = (date.today() - timedelta(days=max_age_days)).isoformat()

    groups = defaultdict(list)
    unparsed = []
    for f in files:
        info = parse_package(f)
        if info is None:
            unparsed.append(f)
            continue
        groups[info["group"]].append((info["order"], f))

    keep_set: set[str] = set()
    for members in groups.values():
        members.sort()
        keep_set.update(f for _, f in members[-keep:])

    for f in files:
        if f in unparsed:
            continue
        added = add_dates.get(f"snapshot/packages/{f}")
        if added is None or added >= cutoff:
            keep_set.add(f)

    delete = sorted(f for f in files if f not in keep_set and f not in unparsed)
    return sorted(keep_set), delete, sorted(unparsed)


def prune_index(index_text: str, deleted_versions: set[str]) -> tuple[str, int]:
    """Drop chart entry blocks whose version is in deleted_versions.

    A Helm index entry is a `  - key: value` list item under a chart name; the
    block extends until the next list item or the next chart key.
    """
    lines = index_text.splitlines(keepends=True)
    result: list[str] = []
    i = 0
    removed = 0
    while i < len(lines):
        if lines[i].startswith("  - "):
            j = i + 1
            while j < len(lines) and not (
                lines[j].startswith("  - ") or re.match(r"^[ ]{0,2}\S", lines[j])
            ):
                j += 1
            block = lines[i:j]
            # Anchored at the entry's own indent level: chart annotations embed
            # CRD manifests that contain their own `version:` keys, deeper in.
            version = next(
                (
                    m.group(1)
                    for line in block
                    if (m := re.match(r'^ {4}version:\s*"?([^"\s]+)"?\s*$', line))
                ),
                None,
            )
            if version in deleted_versions:
                removed += 1
            else:
                result.extend(block)
            i = j
        else:
            result.append(lines[i])
            i += 1
    return "".join(result), removed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="perform deletions (default: dry run)")
    ap.add_argument("--keep", type=int, default=DEFAULT_KEEP, help=f"builds to keep per chart per kind (default: {DEFAULT_KEEP})")
    ap.add_argument("--max-age-days", type=int, default=DEFAULT_MAX_AGE_DAYS, help=f"always keep packages newer than this (default: {DEFAULT_MAX_AGE_DAYS})")
    args = ap.parse_args()

    if not os.path.isdir(PACKAGES_DIR):
        print(f"error: {PACKAGES_DIR} not found", file=sys.stderr)
        return 1

    files = sorted(f for f in os.listdir(PACKAGES_DIR) if f.endswith(".tgz"))
    keep, delete, unparsed = select(files, args.keep, args.max_age_days, git_add_dates("snapshot/packages"))

    def mb(names):
        return sum(os.path.getsize(os.path.join(PACKAGES_DIR, n)) for n in names) / 1048576

    print(f"packages:   {len(files)} ({mb(files):.1f} MB)")
    print(f"keep:       {len(keep)} ({mb(keep):.1f} MB)")
    print(f"delete:     {len(delete)} ({mb(delete):.1f} MB)")
    if unparsed:
        print(f"unrecognised (kept): {len(unparsed)} -> {', '.join(unparsed)}")

    if not args.apply:
        print("\ndry run; re-run with --apply to delete. Would remove:")
        for f in delete:
            print(f"  {f}")
        return 0

    deleted_versions = {parse_package(f)["version"] for f in delete}
    with open(INDEX_FILE, encoding="utf-8") as fh:
        new_index, removed = prune_index(fh.read(), deleted_versions)

    if removed != len(delete):
        print(
            f"warning: removed {removed} index entries for {len(delete)} deleted packages "
            "(some packages may not have been indexed)",
            file=sys.stderr,
        )

    with open(INDEX_FILE, "w", encoding="utf-8") as fh:
        fh.write(new_index)
    for f in delete:
        os.remove(os.path.join(PACKAGES_DIR, f))

    print(f"\ndeleted {len(delete)} packages and {removed} index entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
