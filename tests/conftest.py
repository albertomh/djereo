import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import copier
import pytest

from tests._utils import set_up_postgres, tear_down_postgres

TESTS_DIR = Path(__file__).resolve().parent
DJEREO_TESTS_SANDBOX_DIR = Path("/", "tmp", "djereo_test")
IS_CI = os.getenv("CI") == "true"
DJEREO_TEST_PROJECT_NAME = "djereo_test_project"


def pytest_sessionstart(session):
    if not DJEREO_TESTS_SANDBOX_DIR.exists():
        DJEREO_TESTS_SANDBOX_DIR.mkdir(exist_ok=True)


def pytest_sessionfinish(session):
    # cleanup implemented in `noxfile.py` to ensure all xdist workers have finished
    pass


@pytest.fixture(scope="session", autouse=True)
def set_up_postgres_for_tests():
    tear_down_postgres(DJEREO_TEST_PROJECT_NAME)
    set_up_postgres(DJEREO_TEST_PROJECT_NAME)

    yield

    tear_down_postgres(DJEREO_TEST_PROJECT_NAME)


@pytest.fixture(scope="session")
def djereo_root_dir() -> Path:
    """Provides the path to the djereo project directory for consumption by copier."""
    project_root = Path(__file__).resolve().parent.parent
    if not project_root.exists():
        pytest.fail(f"djereo project root does not exist at {project_root}")
    return project_root


@pytest.fixture(scope="session")
def copier_input_data() -> dict:
    """Answers to core djereo template questions (see `copier.yaml`)."""
    input_data = {
        "_is_test": True,
        "project_name": DJEREO_TEST_PROJECT_NAME,
        "author_name": "Miguel de Cervantes",
        "author_email": "mike@alcala.net",
    }

    nox_session = os.getenv("NOX_SESSION", "")
    nox_match = re.search(r"(\d+\.\d+)", nox_session)
    if nox_match:
        input_data["min_python_version"] = nox_match.group(1)

    django_version = os.getenv("DJANGO_VERSION")
    if django_version:
        input_data["django_version"] = django_version
    return input_data


@pytest.fixture
def test_project_dir(tmp_path: Path) -> Path:
    """Provides a temporary directory for a test project."""
    return tmp_path


@pytest.fixture
def copier_copy(djereo_root_dir: Path, test_project_dir: Path) -> Path:
    """Fixture to run copier with given data, aligned with current project standards."""

    def _copy(data: dict, generate_dotenv: bool = True, copier_quiet: bool = True):
        import copier

        copier.run_copy(
            str(djereo_root_dir),
            str(test_project_dir),
            data=data,
            vcs_ref="HEAD",
            defaults=True,
            quiet=copier_quiet,
            unsafe=True,
        )
        if generate_dotenv:
            dotenv_path = test_project_dir / ".env"
            if not dotenv_path.exists():
                dotenv_path.touch()

    return _copy


@pytest.fixture(scope="session")
def generated_project(
    djereo_root_dir: Path,
    copier_input_data: dict,
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    """Generate a project using djereo to use as a template across integration tests.
    Generate only once per pytest session."""
    project_dir = tmp_path_factory.mktemp("djereo_project")

    copier.run_copy(
        str(djereo_root_dir),
        str(project_dir),
        data=copier_input_data,
        vcs_ref="HEAD",
        defaults=True,
        quiet=True,
        unsafe=True,
    )

    test_env_path = project_dir / ".env.test"
    with test_env_path.open("r+") as file:
        env_content = file.read()
        env_content = (
            env_content + "EMAIL_BACKEND=django.core.mail.backends.locmem.EmailBackend\n"
        )
        file.seek(0)
        file.write(env_content)
        file.truncate()

    subprocess.run(["uv", "sync", "--quiet"], cwd=project_dir, check=True)

    subprocess.run(
        ["uv", "run", "manage.py", "collectstatic", "--noinput"],
        cwd=project_dir,
        check=True,
    )

    return project_dir


@pytest.fixture(scope="function")
def _pytest_function_name(request: pytest.FixtureRequest) -> str:
    return request.function.__name__


@pytest.fixture(scope="function")
def djereo_project_dir_for_test(
    _pytest_function_name: str, generated_project: Path
) -> Path:
    destination = DJEREO_TESTS_SANDBOX_DIR / _pytest_function_name
    if destination.exists():
        shutil.rmtree(destination, ignore_errors=True)
    shutil.copytree(
        generated_project,
        destination,
        ignore=shutil.ignore_patterns(".venv"),
    )
    (destination / ".venv").symlink_to(generated_project / ".venv")
    return destination


@pytest.fixture
def django_debug() -> bool:
    """Return whether Django should run with DEBUG enabled for the current test.

    Usage:
    ```py
    @pytest.mark.parametrize("django_debug", [True])
    def test_when_debug_enabled(set_up_generated_project, django_debug):
        ...
    ```
    """
    return False


@pytest.fixture
def set_up_generated_project(
    request: pytest.FixtureRequest, django_debug: bool, djereo_project_dir_for_test: Path
) -> Path:
    env_test = djereo_project_dir_for_test / ".env.test"
    content = env_test.read_text()
    debug_line = f"DEBUG={'true' if django_debug else 'false'}"
    content = re.sub(r"^DEBUG=.*", debug_line, content, flags=re.MULTILINE)
    env_test.write_text(content)

    venv = djereo_project_dir_for_test / ".venv"
    site_packages = next((venv / "lib").glob("python*/site-packages"))
    sys.path.insert(0, str(site_packages))
    sys.path.insert(0, str(djereo_project_dir_for_test))

    os.environ["USE_ENV_TEST"] = "True"
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", f"{DJEREO_TEST_PROJECT_NAME}.settings"
    )

    import django

    django.setup()

    # run migrations only if they are not up to date and skip_migrate is not requested
    if not request.node.get_closest_marker("skip_migrate"):
        import subprocess

        result = subprocess.run(
            ["uv", "run", "manage.py", "migrate", "--check"],
            cwd=djereo_project_dir_for_test,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            subprocess.run(
                ["uv", "run", "manage.py", "migrate"],
                cwd=djereo_project_dir_for_test,
                check=True,
            )

    return djereo_project_dir_for_test


@pytest.fixture
def django_test_client(set_up_generated_project, django_debug):
    from django.conf import settings
    from django.test import Client

    if not django_debug:
        settings.DEBUG = False

    settings.ALLOWED_HOSTS.append("testserver")

    return Client()
