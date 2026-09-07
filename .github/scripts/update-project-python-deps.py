#!/usr/bin/env python3
"""Update Python dependency constraints."""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
from dataclasses import dataclass
from functools import total_ordering
from pathlib import Path
from urllib.request import urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT_DEP_RE = re.compile(
    r'(?P<prefix>["\'](?P<name>[A-Za-z0-9_.-]+)(?:\[[A-Za-z0-9_.-]+])?>=)'
    r'(?P<lower>[^,<"\']+)'
    r"(?P<middle>,<)"
    r'(?P<upper>[^"\']+)'
    r'(?P<suffix>["\'])'
)
SEMVER_TAG_RE = re.compile(
    r"^v?(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)"
    r"(?:\.(?P<patch>0|[1-9]\d*))?$"
)
PYPI_CACHE: dict[tuple[str, str | None], str] = {}
EXCLUDE_NEWER_RE = re.compile(r'^exclude-newer = "(?P<days>\d+) days"$', re.MULTILINE)
UTC = dt.timezone(dt.timedelta(0))


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
        return cls(*(int(part or 0) for part in match.groups()))

    def __lt__(self, other: Version) -> bool:
        return (self.major, self.minor, self.patch) < (
            other.major,
            other.minor,
            other.patch,
        )

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def project_files() -> list[Path]:
    candidates = [
        REPO_ROOT / "pyproject.toml",
        REPO_ROOT / "template" / "pyproject.toml.jinja",
    ]
    return [path for path in candidates if path.exists()]


def exclude_newer_cutoff(path: Path) -> dt.datetime | None:
    match = EXCLUDE_NEWER_RE.search(path.read_text())
    if match is None:
        return None
    return dt.datetime.now(UTC) - dt.timedelta(days=int(match.group("days")))


def upload_time(release_files: list[dict[str, object]]) -> dt.datetime | None:
    upload_times = [
        dt.datetime.fromisoformat(
            str(file["upload_time_iso_8601"]).replace("Z", "+00:00")
        )
        for file in release_files
        if not file.get("yanked") and file.get("upload_time_iso_8601")
    ]
    if not upload_times:
        return None
    return min(upload_times)


def latest_pypi_version(name: str, cutoff: dt.datetime | None) -> str:
    package_name = name.replace("_", "-").lower()
    cache_key = (package_name, cutoff.isoformat() if cutoff is not None else None)
    if cache_key in PYPI_CACHE:
        return PYPI_CACHE[cache_key]

    with urlopen(f"https://pypi.org/pypi/{package_name}/json", timeout=30) as response:
        payload = json.load(response)

    candidates: list[tuple[Version, str]] = []
    for version, release_files in payload["releases"].items():
        parsed = Version.parse(version)
        released_at = upload_time(release_files)
        if parsed is None or released_at is None:
            continue
        if cutoff is not None and released_at > cutoff:
            continue
        candidates.append((parsed, version))

    if not candidates:
        raise RuntimeError(f"Could not find a usable release for {package_name}")  # noqa: TRY003

    latest = max(candidates)[1]
    PYPI_CACHE[cache_key] = latest
    return latest


def upper_bound_for(version: str) -> str:
    parsed = Version.parse(version)
    if parsed is None:
        raise RuntimeError(f"Unsupported version from PyPI: {version}")  # noqa: TRY003
    if parsed.major == 0:
        return f"0.{parsed.minor + 1}.0"
    return f"{parsed.major + 1}.0.0"


def update_pyproject(path: Path) -> bool:
    changed = False
    cutoff = exclude_newer_cutoff(path)

    def replace(match: re.Match[str]) -> str:
        nonlocal changed
        if "{" in match.group(0):
            return match.group(0)

        latest = latest_pypi_version(match.group("name"), cutoff)
        current = Version.parse(match.group("lower"))
        selected = Version.parse(latest)
        if current is not None and selected is not None and selected <= current:
            return match.group(0)

        replacement = (
            f"{match.group('prefix')}{latest}"
            f"{match.group('middle')}{upper_bound_for(latest)}"
            f"{match.group('suffix')}"
        )
        changed = changed or replacement != match.group(0)
        return replacement

    updated = PYPROJECT_DEP_RE.sub(replace, path.read_text())
    if changed:
        path.write_text(updated)
    return changed


def main() -> None:
    changed_paths = [path for path in project_files() if update_pyproject(path)]
    for path in changed_paths:
        sys.stdout.write(f"{path.relative_to(REPO_ROOT)}\n")


if __name__ == "__main__":
    main()
