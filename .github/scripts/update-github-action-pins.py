#!/usr/bin/env python3
"""Update GitHub Actions SHA pins and human-readable version comments."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SHA_RE = re.compile(r"^[a-f0-9]{40}$")
MAJOR_TAG_RE = re.compile(r"^v(?P<major>\d+)$")
SEMVER_TAG_RE = re.compile(
    r"^v(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)$"
)
DATE_TAG_RE = re.compile(r"^(?P<year>\d{4})\.(?P<month>\d{2})\.(?P<day>\d{2})$")
USES_RE = re.compile(
    r"(?P<prefix>\buses:\s*)(?P<repo>[\w.-]+/[\w.-]+)@(?P<ref>[^\s#]+)"
    r"(?P<suffix>[^\n#]*)(?P<comment>\s*#\s*(?P<tag>\S+).*)?$"
)
TAG_CACHE: dict[str, set[str]] = {}
SHA_CACHE: dict[tuple[str, str], str] = {}


def sort_key(match: re.Match[str]) -> tuple[int, ...]:
    return tuple(int(part) for part in match.groups())


def github_action_files() -> list[Path]:
    paths: list[Path] = []
    for root in (REPO_ROOT / ".github", REPO_ROOT / "template"):
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.suffix not in {".yaml", ".yml"}:
                continue
            if root.name == "template" and not any(
                ".github" in part for part in path.parts
            ):
                continue
            paths.append(path)
    return sorted(paths)


def git_ls_remote(repo: str, *patterns: str) -> str:
    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git executable is required")  # noqa: TRY003

    url = f"https://github.com/{repo}.git"
    result = subprocess.run(  # noqa: S603
        [git, "ls-remote", url, *patterns],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def list_tags(repo: str) -> set[str]:
    if repo in TAG_CACHE:
        return TAG_CACHE[repo]

    output = git_ls_remote(repo, "refs/tags/*")
    tags: set[str] = set()
    for line in output.splitlines():
        _, ref = line.split(maxsplit=1)
        tags.add(ref.removeprefix("refs/tags/").removesuffix("^{}"))
    TAG_CACHE[repo] = tags
    return tags


def latest_tag(repo: str, current_tag: str) -> str:
    major_match = MAJOR_TAG_RE.fullmatch(current_tag)
    semver_match = SEMVER_TAG_RE.fullmatch(current_tag)
    date_match = DATE_TAG_RE.fullmatch(current_tag)

    if major_match is None and semver_match is None and date_match is None:
        return current_tag

    candidates: list[tuple[tuple[int, ...], str]] = []
    for tag in list_tags(repo):
        candidate_match = None
        if major_match is not None:
            candidate_match = MAJOR_TAG_RE.fullmatch(tag)
        elif semver_match is not None:
            candidate_match = SEMVER_TAG_RE.fullmatch(tag)
        elif date_match is not None:
            candidate_match = DATE_TAG_RE.fullmatch(tag)

        if candidate_match is not None:
            candidates.append((sort_key(candidate_match), tag))

    if not candidates:
        return current_tag
    return max(candidates)[1]


def resolve_tag(repo: str, tag: str) -> str:
    if (repo, tag) in SHA_CACHE:
        return SHA_CACHE[(repo, tag)]

    output = git_ls_remote(repo, f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}")
    refs = {
        ref.removeprefix("refs/tags/").removesuffix("^{}"): sha
        for sha, ref in (line.split(maxsplit=1) for line in output.splitlines())
    }
    if tag not in refs:
        raise RuntimeError(f"Could not resolve {repo}@{tag}")  # noqa: TRY003
    SHA_CACHE[(repo, tag)] = refs[tag]
    return refs[tag]


def update_file(path: Path) -> bool:
    changed = False
    lines = path.read_text().splitlines(keepends=True)
    updated_lines: list[str] = []

    for line in lines:
        match = USES_RE.search(line.rstrip("\n"))
        if match is None:
            updated_lines.append(line)
            continue

        current_ref = match.group("ref")
        tag = match.group("tag") or current_ref

        if SHA_RE.fullmatch(tag):
            updated_lines.append(line)
            continue

        repo = match.group("repo")
        tag = latest_tag(repo, tag)
        sha = resolve_tag(repo, tag)
        suffix = match.group("suffix").rstrip()
        replacement = (
            f"{match.group('prefix')}{match.group('repo')}@{sha}{suffix} # {tag}"
        )
        newline = "\n" if line.endswith("\n") else ""
        updated_line = USES_RE.sub(replacement, line.rstrip("\n")) + newline
        changed = changed or updated_line != line
        updated_lines.append(updated_line)

    if changed:
        path.write_text("".join(updated_lines))
    return changed


def main() -> None:
    changed_paths = [path for path in github_action_files() if update_file(path)]
    for path in changed_paths:
        sys.stdout.write(f"{path.relative_to(REPO_ROOT)}\n")


if __name__ == "__main__":
    main()
