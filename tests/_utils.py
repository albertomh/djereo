import os
import re
import socket
import time
from pathlib import Path

import psycopg
from psycopg import sql
from sh import ErrorReturnCode, git, whoami


def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r"\x1b[^m]*m")
    return ansi_escape.sub("", text)


def is_git_repo(path: Path) -> bool:
    """Check if the given path is a Git repository."""
    try:
        git("-C", str(path), "status")
    except ErrorReturnCode:
        return False
    else:
        return True


def count_dirs_and_files(path: Path) -> tuple[int, int]:
    """Count the number of directories and files in a given path.

    Args:
        path (Path): The directory path to inspect.

    Returns:
        tuple[int, int]: A tuple of the number of directories and the number of files.
    """
    num_dirs, num_files = 0, 0
    for entry in path.iterdir():
        if entry.is_file():
            num_files += 1
        elif entry.is_dir():
            num_dirs += 1
    return num_dirs, num_files


def in_ci() -> bool:
    return os.getenv("CI") == "true"


def get_current_os_user() -> str:
    current_user = whoami()
    return current_user.strip()


def get_postgres_user() -> str:
    if in_ci():
        return "postgres"
    return get_current_os_user()


def get_postgres_connection_string(dbname: str = "postgres") -> str:
    user = get_postgres_user()
    password = "password" if in_ci() else None
    conn_str = f"host=localhost user={user} dbname={dbname}"
    if password:
        conn_str += f" password={password}"
    return conn_str


def set_up_postgres(project_name: str) -> None:
    conn_str = get_postgres_connection_string()
    password = "password"
    user_name = project_name
    prod_db = project_name
    test_db = f"test_{project_name}"

    with psycopg.connect(conn_str, autocommit=True) as conn:
        with conn.cursor() as cur:
            # terminate any old connections to both DBs
            for db in [prod_db, test_db]:
                cur.execute(
                    """
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = %s AND pid <> pg_backend_pid();
                    """,
                    (db,),
                )

            # create user if it doesn't exist
            cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (user_name,))
            if not cur.fetchone():
                cur.execute(
                    sql.SQL("CREATE USER {} WITH PASSWORD {}").format(
                        sql.Identifier(user_name), sql.Literal(password)
                    )
                )
                cur.execute(
                    sql.SQL("ALTER USER {} CREATEDB").format(sql.Identifier(user_name))
                )

            # create both DBs if they don't exist
            for db in [prod_db, test_db]:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db,))
                if not cur.fetchone():
                    cur.execute(
                        sql.SQL("CREATE DATABASE {} OWNER {}").format(
                            sql.Identifier(db), sql.Identifier(user_name)
                        )
                    )


def tear_down_postgres(project_name: str):
    conn_str = get_postgres_connection_string()
    user_name = project_name
    prod_db = project_name
    test_db = f"test_{project_name}"

    with psycopg.connect(conn_str, autocommit=True) as conn:
        with conn.cursor() as cur:
            for db in [prod_db, test_db]:
                cur.execute(
                    """
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = %s AND pid <> pg_backend_pid();
                    """,
                    (db,),
                )
                cur.execute(
                    sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db))
                )

            cur.execute(
                sql.SQL("DROP USER IF EXISTS {}").format(sql.Identifier(user_name))
            )


def get_free_port_from_os() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def wait_for_server(host: str, port: int, timeout: float = 10.0) -> None:
    """Block until a TCP server starts accepting connections."""
    start = time.monotonic()

    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                return
        except OSError:
            pass

        if time.monotonic() - start > timeout:
            raise TimeoutError(f"Server {host}:{port} did not start within {timeout}s")  # noqa: TRY003

        time.sleep(0.05)
