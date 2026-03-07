# Usage:
# > nox [-- --pdb | -m "mark"]

import os
import re
import shutil
from pathlib import Path

import nox

PROJECT_ROOT_DIR = Path(__file__).resolve().parent
TESTS_DIR = PROJECT_ROOT_DIR / "tests"
DJEREO_TESTS_SANDBOX_DIR = Path("/", "tmp", "djereo_test")


def _get_copier_choices(key: str) -> list[str]:
    """
    Extract choices for a key from copier.yaml without using PyYAML.
    This avoids needing PyYAML in the environment where nox is initially loaded.
    """
    with (PROJECT_ROOT_DIR / "copier.yaml").open() as f:
        content = f.read()

    # Find the block for the key, then the choices within it.
    # This is a simple parser for the specific format in copier.yaml.
    pattern = rf"^{key}:.*?\n\s+choices:(.*?)(?:\n\w|\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        choices_block = match.group(1)
        return re.findall(r'- "(.*?)"', choices_block)
    return []


py_versions = _get_copier_choices("min_python_version")
dj_versions = _get_copier_choices("django_version")

LATEST_PY = py_versions[-1]
LATEST_DJ = dj_versions[-1]

nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True
# default to latest versions for local runs
nox.options.sessions = [f"tests-{LATEST_PY}(django='{LATEST_DJ}')"]
# in CI all combinations run (via `nox --list` in `.github/workflows/_checks.yaml`)


def clean_up(session: nox.Session):
    cmd = (
        "from tests._utils import clean_up_all_test_databases;"
        "clean_up_all_test_databases()"
    )
    session.run(
        "python",
        "-c",
        cmd,
        env={"PYTHONPATH": "."},
    )

    if DJEREO_TESTS_SANDBOX_DIR.exists():
        shutil.rmtree(DJEREO_TESTS_SANDBOX_DIR, ignore_errors=True)


@nox.session(python=py_versions)
@nox.parametrize("django", dj_versions)
def tests(session: nox.Session, django: str):
    session.run_install(
        "uv",
        "sync",
        "--group=test",
        "--frozen",
        "--quiet",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )

    # Needed for assertions against `importlib.metadata.version`.
    session.install("-e", ".")

    posargs = list(session.posargs)
    use_pdb = "--pdb" in posargs

    pytest_args = [
        "--capture=no",
        "--verbosity=3",
        "--showlocals",
        "--pythonwarnings=always",
    ]

    if not use_pdb:
        pytest_args.extend(
            [
                "--numprocesses=auto",
                # Run grouped tests (`@pytest.mark.xdist_group(name="my_group")`) with the
                # same worker. Ensure serial execution of integration (`runserver`) tests.
                "--dist=loadgroup",
            ]
        )

    try:
        session.env["NOX_SESSION"] = session.name
        session.env["DJANGO_VERSION"] = django
        session.run("pytest", "tests/", *pytest_args, *posargs)
    finally:
        if os.getenv("CI") != "true":
            clean_up(session)
