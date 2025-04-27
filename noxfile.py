import nox

# https://endoflife.date/python
py_versions = ["3.13", "3.12"]

nox.options.default_venv_backend = "uv"


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

    session.run(
        "pytest",
        "tests/",
        "-s",
        "-vvv",
        "--showlocals",
        "-W",
        "always",
        "--pdb",
        *session.posargs,
    )
