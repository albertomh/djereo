# ruff: noqa: S603 S607

# Usage:
# > nox [-- --pdb | -m "mark"]

import os
import shutil
import subprocess
from pathlib import Path

import nox

# https://endoflife.date/python
py_versions = ["3.12", "3.13"]
OLDEST_PY, *MIDDLE_PY, LATEST_PY = py_versions

PROJECT_ROOT_DIR = Path(__file__).resolve().parent
TESTS_DIR = PROJECT_ROOT_DIR / "tests"
DJEREO_TESTS_SANDBOX_DIR = Path("/", "tmp", "djereo_test")

nox.options.default_venv_backend = "uv"
nox.options.sessions = [f"tests-{LATEST_PY}"]


def clean_up():
    user = subprocess.check_output(["whoami"], text=True).strip()
    subprocess.run(
        [
            "psql",
            "--user",
            user,
            "--host",
            "localhost",
            "--dbname",
            "postgres",
            "--file",
            "_clean_up_databases.sql",
        ],
        cwd=TESTS_DIR,
        check=True,
    )

    if DJEREO_TESTS_SANDBOX_DIR.exists():
        shutil.rmtree(DJEREO_TESTS_SANDBOX_DIR, ignore_errors=True)


@nox.session(python=py_versions)
def tests(session: nox.Session):
    session.run_install(
        "uv",
        "sync",
        "--group=test",
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
        session.run("pytest", "tests/", *pytest_args, *posargs)
    finally:
        if os.getenv("CI") != "true":
            clean_up()
