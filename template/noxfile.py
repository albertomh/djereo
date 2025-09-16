# ruff: noqa: INP001

import nox

# https://endoflife.date/python
py_versions = ["3.12", "3.13"]
OLDEST_PY, *MIDDLE_PY, LATEST_PY = py_versions

nox.options.default_venv_backend = "uv"
nox.options.sessions = [f"tests_with_coverage-{LATEST_PY}"]

run_tests_args = ["manage.py", "test"]
base_flags = ["--failfast", "--shuffle", "--verbosity=3"]


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


def _effective_flags(session: nox.Session) -> list[str]:
    """Manipulate Django test runner flags to avoid incompatibilities.

    Parallel execution must be disabled (force DJANGO_TEST_PROCESSES to 1) if using `pdb`.
    <https://docs.djangoproject.com/en/stable/ref/django-admin/#cmdoption-test-parallel>
    """
    test_processes = 2
    if "--pdb" in session.posargs:
        test_processes = 1

    return [*base_flags, f"--parallel={test_processes}", *session.posargs]


@nox.session(python=MIDDLE_PY)
def tests(session: nox.Session) -> None:
    _install_deps(session)

    session.run(
        "python",
        "-Wall",
        *run_tests_args,
        *_effective_flags(session),
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
        *_effective_flags(session),
    )
    session.run("coverage", "report")
    session.run("coverage", "html")
