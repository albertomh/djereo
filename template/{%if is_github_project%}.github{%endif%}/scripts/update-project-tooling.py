#!/usr/bin/env python3
"""Update prek hook revisions."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from functools import total_ordering
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PREK_REPO_RE = re.compile(
    r'^(?P<prefix>repo = ")(?P<repo>https://github.com/[^"/]+/[^"/]+)(?P<suffix>")$'
)
PREK_REV_RE = re.compile(r'^(?P<prefix>rev = ")(?P<rev>[^"]+)(?P<suffix>")$')
SEMVER_TAG_RE = re.compile(
    r"^v?(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)$"
)
TAG_CACHE: dict[str, set[str]] = {}


@total_ordering
@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, value: str) -> Version | None:
        match = SEMVER_TAG_RE.fullmatch(value)
        if match is None:
            return None
        return cls(*(int(part) for part in match.groups()))

    def __lt__(self, other: Version) -> bool:
        return (self.major, self.minor, self.patch) < (
            other.major,
            other.minor,
            other.patch,
        )


def project_files() -> list[Path]:
    candidates = [
        REPO_ROOT / "prek.toml",
    ]
    return [path for path in candidates if path.exists()]


def git_ls_remote_tags(repo_url: str) -> set[str]:
    if repo_url in TAG_CACHE:
        return TAG_CACHE[repo_url]

    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git executable is required")  # noqa: TRY003

    result = subprocess.run(  # noqa: S603
        [git, "ls-remote", repo_url, "refs/tags/*"],
        check=True,
        capture_output=True,
        text=True,
    )
    tags: set[str] = set()
    for line in result.stdout.splitlines():
        _, ref = line.split(maxsplit=1)
        tags.add(ref.removeprefix("refs/tags/").removesuffix("^{}"))
    TAG_CACHE[repo_url] = tags
    return tags


def latest_matching_rev(repo_url: str, current_rev: str) -> str:
    if Version.parse(current_rev) is None:
        return current_rev

    candidates: list[tuple[Version, str]] = []
    for tag in git_ls_remote_tags(repo_url):
        version = Version.parse(tag)
        if version is not None:
            candidates.append((version, tag))

    if not candidates:
        return current_rev
    return max(candidates)[1]


def update_prek(path: Path) -> bool:
    changed = False
    current_repo: str | None = None
    updated_lines: list[str] = []

    for line in path.read_text().splitlines(keepends=True):
        stripped = line.rstrip("\n")
        repo_match = PREK_REPO_RE.match(stripped)
        if repo_match is not None:
            current_repo = repo_match.group("repo")
            updated_lines.append(line)
            continue

        rev_match = PREK_REV_RE.match(stripped)
        if rev_match is None or current_repo is None:
            updated_lines.append(line)
            continue

        latest = latest_matching_rev(current_repo, rev_match.group("rev"))
        newline = "\n" if line.endswith("\n") else ""
        updated_line = (
            f"{rev_match.group('prefix')}{latest}{rev_match.group('suffix')}{newline}"
        )
        changed = changed or updated_line != line
        updated_lines.append(updated_line)

    if changed:
        path.write_text("".join(updated_lines))
    return changed


def main() -> None:
    changed_paths = [path for path in project_files() if update_prek(path)]
    for path in changed_paths:
        sys.stdout.write(f"{path.relative_to(REPO_ROOT)}\n")


if __name__ == "__main__":
    main()
