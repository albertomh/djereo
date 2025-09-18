# Usage:
# > nox [-- --pdb | -m "mark"]

import nox

# https://endoflife.date/python
py_versions = ["3.12", "3.13"]
OLDEST_PY, *MIDDLE_PY, LATEST_PY = py_versions

nox.options.default_venv_backend = "uv"
nox.options.sessions = [f"tests-{LATEST_PY}"]


@nox.session(python=py_versions)
def tests(session: nox.Session) -> None:
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

    session.run("pytest", "tests/", *pytest_args, *posargs)
