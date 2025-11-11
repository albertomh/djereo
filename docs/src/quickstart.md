# Quickstart

This section covers how to create a Django project using `djereo` as a template.

## Prerequisites

The following must be available locally:

- [Python 3.13](https://docs.python.org/3.13/){target=\"_blank"} or above
- [Postgres](https://www.postgresql.org/download/)
- [uv](https://docs.astral.sh/uv/){target=\"_blank"}
- [just](https://github.com/casey/just)

## Bootstrap a new Django project

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

## Update existing projects

To update a project created using an older version of `djereo` to a newer version of the
template:

```sh
cd ~/Projects/existing_project/
uvx copier update --skip-answered --trust [--vcs-ref=<TAG>]
```

If the `--vcs-ref` flag is not specified `copier` will use the latest `djereo` tag.
