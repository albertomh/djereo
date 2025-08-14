# ruff: noqa: INP001

import nox

# https://endoflife.date/python
py_versions = ["3.12", "3.13"]
OLDEST_PY, *MIDDLE_PY, LATEST_PY = py_versions

nox.options.default_venv_backend = "uv"
nox.options.sessions = [f"tests_with_coverage-{LATEST_PY}"]

run_tests_args = ["manage.py", "test"]
run_tests_flags = ["--failfast", "--pdb", "--shuffle", "--verbosity=3"]


def _install_deps(session: nox.Session) -> None:
    session.run_install(
        "uv",
        "sync",
        "--group=test",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )

    # Needed for assertions against `importlib.metadata.version`.
    session.install("-e", ".")


@nox.session(python=MIDDLE_PY)
def tests(session: nox.Session) -> None:
    _install_deps(session)

    session.run(
        "python",
        "-Wall",
        *run_tests_args,
        *session.posargs,
        *run_tests_flags,
    )


@nox.session(python=[OLDEST_PY, LATEST_PY])
def tests_with_coverage(session: nox.Session) -> None:
    _install_deps(session)

    session.run("coverage", "erase")
    session.run(
        "coverage",
        "run",
        "--source",
        ".",
        *run_tests_args,
        *session.posargs,
        *run_tests_flags,
    )
    session.run("coverage", "report")
    session.run("coverage", "html")
