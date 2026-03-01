import os
import re
import socket
from collections.abc import Callable
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


def set_up_postgres(test_project_dir: Path, project_name: str) -> Callable[[], None]:
    conn_str = get_postgres_connection_string()
    password = "password"

    with psycopg.connect(conn_str, autocommit=True) as conn:
        with conn.cursor() as cur:
            # Create users and databases for the project
            for name in [project_name, f"test_{project_name}"]:
                # Drop existing to ensure a clean slate (including nested test dbs)
                for db_to_drop in [f"test_{name}", name]:
                    cur.execute(
                        """
                        SELECT pg_terminate_backend(pid)
                        FROM pg_stat_activity
                        WHERE datname = %s AND pid <> pg_backend_pid();
                        """,
                        (db_to_drop,),
                    )
                    cur.execute(
                        sql.SQL("DROP DATABASE IF EXISTS {}").format(
                            sql.Identifier(db_to_drop)
                        )
                    )

                cur.execute(
                    sql.SQL("DROP USER IF EXISTS {}").format(sql.Identifier(name))
                )

                cur.execute(
                    sql.SQL("CREATE USER {} WITH PASSWORD {}").format(
                        sql.Identifier(name), sql.Literal(password)
                    )
                )
                cur.execute(
                    sql.SQL("ALTER USER {} CREATEDB").format(sql.Identifier(name))
                )
                cur.execute(
                    sql.SQL("CREATE DATABASE {} OWNER {}").format(
                        sql.Identifier(name), sql.Identifier(name)
                    )
                )


def tear_down_postgres(test_project_dir: Path, project_name: str):
    conn_str = get_postgres_connection_string()

    with psycopg.connect(conn_str, autocommit=True) as conn:
        with conn.cursor() as cur:
            for name in [project_name, f"test_{project_name}"]:
                # Drop databases (including nested test dbs created by Django)
                for db_to_drop in [f"test_{name}", name]:
                    cur.execute(
                        """
                        SELECT pg_terminate_backend(pid)
                        FROM pg_stat_activity
                        WHERE datname = %s AND pid <> pg_backend_pid();
                        """,
                        (db_to_drop,),
                    )
                    cur.execute(
                        sql.SQL("DROP DATABASE IF EXISTS {}").format(
                            sql.Identifier(db_to_drop)
                        )
                    )

                cur.execute(
                    sql.SQL("DROP USER IF EXISTS {}").format(sql.Identifier(name))
                )


def clean_up_all_test_databases():
    """Clean up all databases and roles related to 'djereo_test_'."""
    conn_str = get_postgres_connection_string()
    # Use a broader pattern to catch test_djereo_test_ and test_test_djereo_test_
    pattern = "%djereo_test_%"

    with psycopg.connect(conn_str, autocommit=True) as conn:
        with conn.cursor() as cur:
            # Drop databases
            cur.execute(
                "SELECT datname FROM pg_database WHERE datname LIKE %s", (pattern,)
            )
            databases = [row[0] for row in cur.fetchall()]

            # Drop roles
            cur.execute("SELECT rolname FROM pg_roles WHERE rolname LIKE %s", (pattern,))
            roles = [row[0] for row in cur.fetchall()]

            if not databases and not roles:
                return

            if databases:
                # Terminate sessions
                cur.execute(
                    """
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname LIKE %s
                      AND pid <> pg_backend_pid();
                    """,
                    (pattern,),
                )

                for db in databases:
                    cur.execute(
                        sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db))
                    )

            if roles:
                for role in roles:
                    cur.execute(
                        sql.SQL("DROP ROLE IF EXISTS {}").format(sql.Identifier(role))
                    )


def get_free_port_from_os() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]
