# Welcome to the Djereo docs

`djereo` - a Django project template with opinionated tooling.

Built on top of the [pycliche](https://github.com/albertomh/pycliche){target=\"_blank"} template.

[![python: 3.10](https://img.shields.io/badge/>=3.10-4584b6?logo=python&logoColor=ffde57)](https://docs.python.org/3.10/whatsnew/3.10.html)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/albertomh/djereo/main/docs/media/copier-badge.json)](https://github.com/copier-org/copier)
[![justfile](https://img.shields.io/badge/🤖_justfile-EFF1F3)](https://github.com/casey/just)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&labelColor=261230&color=de60e9)](https://github.com/astral-sh/uv)
[![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=ffffff)](https://docs.djangoproject.com/en/stable/)
[![Postgres](https://img.shields.io/badge/Postgres-346791?logo=postgresql&logoColor=ffffff)](https://www.postgresql.org/docs/)
[![IPython](https://img.shields.io/badge/IP[y]:-3465a4)](https://ipython.readthedocs.io/en/stable/)
[![structlog](https://img.shields.io/badge/🪵_structlog-b9a198)](https://github.com/hynek/structlog)
[![pre-commit](https://img.shields.io/badge/pre--commit-FAB040?logo=pre-commit&logoColor=1f2d23)](https://github.com/pre-commit/pre-commit)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&labelColor=261230&color=d8ff64)](https://github.com/astral-sh/ruff)
[![biome](https://img.shields.io/badge/Biome-FFFFFF?logo=biome&logoColor=60A5FA)](https://github.com/biomejs/biome)
[![pytest](https://img.shields.io/badge/pytest-0A9EDC?logo=pytest&logoColor=white)](https://github.com/pytest-dev/pytest)
[![coverage](https://img.shields.io/badge/😴_coverage-59aabd)](https://coverage.readthedocs.io/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Release Please](https://img.shields.io/badge/📦_Release_Please-6C97BB)](https://github.com/googleapis/release-please)
[![gunicorn](https://img.shields.io/badge/gunicorn-f7f8f2?logo=gunicorn&logoColor=499848)](https://docs.gunicorn.org/en/latest/index.html)
[![CI](https://github.com/albertomh/djereo/actions/workflows/ci.yaml/badge.svg)](https://github.com/albertomh/djereo/actions/workflows/ci.yaml)

## Features

Projects created using `djereo` include:

- A basic Python package and entrypoint, configured via a `pyproject.toml`.
- Dependencies managed via `uv`, using a `uv.lock` file for reproducible builds.
- IPython as the default shell.
- Simple configuration to enhance your logs with `structlog`.
- Sensible defaults to use a `postgres` database from the start.
- Ready-to-use dev tools: Django Debug Toolbar, `django-browser-reload`, runserver logs
  formatted using `rich`, `structlog` in production.
- Out-of-the-box unit test suite & code coverage reporting.
- Batteries-included `pre-commit` hook configuration to lint & format code, and run SAST.
- A `justfile` to use `just` as a task runner for common jobs.
- Lean containerisation to quickly deploy a project to hosted environments.
- ...and more!

Optionally, for projects intended to be hosted on GitHub, also include:

<!-- markdownlint-disable MD007 ul-indent -->
- GitHub Actions to:
    - Automate cutting releases via `Release Please`.
    - Run `pre-commit` hooks and `pytest` as part of a Continuous Integration pipeline.
- A `dependabot` configuration to keep Python packages & GitHub Actions up to date.
<!-- markdownlint-enable MD007 ul-indent -->

If `djereo` sounds like a good foundation for your next project, explore the [full list of features](./featurelist.md)
or get started with the instructions on the [Quickstart page](./quickstart.md).

---

!!! note ""
    [![Python](https://img.shields.io/badge/Python-4584b6?logo=python&logoColor=ffde57)](https://github.com/albertomh/pycliche)  
    Starting a Python project? Try [pycliche](https://github.com/albertomh/pycliche), the base
    _djereo_ is built on, as your Python project template.

---
