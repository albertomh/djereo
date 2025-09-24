# ruff: noqa: INP001

import nox

# https://endoflife.date/python
py_versions = ["3.12", "3.13"]
OLDEST_PY, *MIDDLE_PY, LATEST_PY = py_versions

nox.options.default_venv_backend = "uv"
nox.options.sessions = [f"tests_with_coverage-{LATEST_PY}"]

RUN_TESTS_ARGS = ["manage.py", "test"]
BASE_FLAGS = ["--failfast", "--shuffle", "--verbosity=3"]


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
    posargs = [*session.posargs]
    conditional_flags = []

    if "--create-db" in posargs:
        posargs = [p for p in posargs if p != "--create-db"]
        # needed to force re-creating old databases left over from runs with `--keepdb`
        conditional_flags.append("--no-input")
    else:
        conditional_flags.append("--keepdb")

    test_processes = 2
    if "--pdb" in posargs:
        test_processes = 1
    conditional_flags.append(f"--parallel={test_processes}")

    return [*BASE_FLAGS, *conditional_flags, *posargs]


@nox.session(python=MIDDLE_PY)
def tests(session: nox.Session) -> None:
    _install_deps(session)

    session.run(
        "python",
        "-Wall",
        *RUN_TESTS_ARGS,
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
        *RUN_TESTS_ARGS,
        *_effective_flags(session),
    )
    session.run("coverage", "report")
    session.run("coverage", "html")
