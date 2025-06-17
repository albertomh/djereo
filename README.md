<!-- markdownlint-disable MD041 first-line-heading/first-line-h1 -->

<!-- markdownlint-disable MD033 no-inline-html -->
<p align="center">
  <!-- markdownlint-disable MD013 line-length -->
  <img src="docs/media/djereo_wordmark-logo.webp" alt="djereo logo - a printing plate embossed with a pony (the Django mascot) and the word 'djereo'"/>
  <!-- markdownlint-enable MD013 line-length -->
</p>

`djereo` - a Django project template with opinionated tooling.

Embracing [Boring Technology](https://boringtechnology.club/), fighting bloat, striving for
simplicity.

Built on top of the [pycliche](https://github.com/albertomh/pycliche) template.

[![python >= 3.12](https://img.shields.io/badge/>=3.12-4584b6?logo=python&logoColor=ffde57)](https://docs.python.org/3.12/whatsnew/3.12.html)
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
[![nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Release Please](https://img.shields.io/badge/📦_Release_Please-6C97BB)](https://github.com/googleapis/release-please)
[![gunicorn](https://img.shields.io/badge/gunicorn-f7f8f2?logo=gunicorn&logoColor=499848)](https://docs.gunicorn.org/en/latest/index.html)
[![CI](https://github.com/albertomh/djereo/actions/workflows/ci.yaml/badge.svg)](https://github.com/albertomh/djereo/actions/workflows/ci.yaml)

## Features

Projects created using `djereo` include:

- A Django web application, configured via a `pyproject.toml`.
- Dependencies managed via `uv`, using a `uv.lock` file for reproducible builds.
- An implementation of the 'custom User + UserProfile' pattern, tied together with a
  `django-allauth` integration.
- Optional vendorised `htmx` with sensible defaults for the frontend.
- Simple configuration to enhance your logs with `structlog`.
- Ready-to-use dev tools: Django Debug Toolbar, `django-browser-reload`, runserver logs
  formatted using `rich`, `structlog` in production.
- IPython as the default shell.
- Out-of-the-box code coverage reporting with `coverage.py`.
- `pre-commit` hooks to lint & format code, and run SAST.
- A `justfile` to use `just` as a task runner for common jobs.
- Lean containerisation to quickly deploy a project to hosted environments.
- Settings to score A+ on securityheaders.com, for peace of mind.
- ...and more!

Optionally, for projects intended to be hosted on GitHub, also include:

- GitHub Actions to:
  - Automate cutting releases via `Release Please`.
  - Run `pre-commit` hooks and `pytest` as part of a Continuous Integration pipeline.
- A `dependabot` configuration to keep Python packages & GitHub Actions up to date.

> [![docs](https://img.shields.io/badge/📖_Docs-FFFFFF)](https://albertomh.github.io/djereo/)  
> Read about all of `djereo`'s features: [https://albertomh.github.io/djereo/featurelist/](https://albertomh.github.io/djereo/featurelist/)

<!-- break up blockquotes to avoid triggering markdownlint's MD028/no-blanks-blockquote -->

> [![Python](https://img.shields.io/badge/Python-4584b6?logo=python&logoColor=ffde57)](https://github.com/albertomh/pycliche)  
> Starting a Python project? Try [pycliche](https://github.com/albertomh/pycliche), the base
> `djereo` is built on, as your Python project template.

## Quickstart

This section covers how to create a Django project using `djereo` as a template.

### Prerequisites

The following must be available locally:

- [Python 3.12](https://docs.python.org/3.12/) or above
- [Postgres](https://www.postgresql.org/download/)
- [uv](https://docs.astral.sh/uv/)
- [just](https://github.com/casey/just)

### Bootstrap a new Django project

Bootstrap a new Django project using `djereo`:

1. Navigate to the directory under which you wish to create a new project.
1. Run `uvx copier copy --trust gh:albertomh/djereo <project_name>` and follow the wizard.

This creates a directory under your current location. Follow the README in the new
`<project_name>/` directory to get started with your project.

Please note:

- it is not necessary to clone `djereo`. The `gh:albertomh/djereo` argument will pull
  the latest tag from GitHub.
- the `--trust` flag is necessary to allow a post-creation task to initialise the new directory
  as a git repository and generate a `uv` lockfile.

---

## Documentation

`djereo`'s documentation is available at [https://albertomh.github.io/djereo/](https://albertomh.github.io/djereo/).

---

## Develop

The developer documentation ([https://albertomh.github.io/djereo/develop/](https://albertomh.github.io/djereo/develop/))
covers how to work on `djereo` itself:

- [Develop](https://albertomh.github.io/djereo/develop/#develop)
  - [Development prerequisites](https://albertomh.github.io/djereo/develop/#development-prerequisites)
  - [Upgrading the pycliche version](https://albertomh.github.io/djereo/develop/#upgrading-the-pycliche-version)
  - [Git principles](https://albertomh.github.io/djereo/develop/#git-principles)
  - [Dependency management](https://albertomh.github.io/djereo/develop/#dependency-management)
    - [Updating dependencies in the template](https://albertomh.github.io/djereo/develop/#updating-dependencies-in-the-template)
  - [Generate project using development version](https://albertomh.github.io/djereo/develop/#generate-project-using-development-version)
  - [Style](https://albertomh.github.io/djereo/develop/#style)
  - [Upgrade checklist](https://albertomh.github.io/djereo/develop/#upgrade-checklist)

- [Test](https://albertomh.github.io/djereo/develop/#test)

- [Document](https://albertomh.github.io/djereo/develop/#document)

- [Release](https://albertomh.github.io/djereo/develop/#release)
  - [GitHub Personal Access Token](https://albertomh.github.io/djereo/develop/#github-personal-access-token)

---

## Acknowledgements

Several tooling choices have been guided by the work of [Adam Johnson](https://adamj.eu/tech/)
&amp; [Carlton Gibson](https://github.com/carltongibson).

The `djereo` logo is typeset in [Black Ops One](https://fonts.google.com/specimen/Black+Ops+One).
Horse head icon generated using DALL·E.

## What's in a name?

"Stereotype" or "stereo" refers to the metal plates used to quickly mass-produce printed media.
