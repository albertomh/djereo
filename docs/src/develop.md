# Djereo developer documentation

## Develop

`djereo`'s source code can be found at [https://github.com/albertomh/djereo](https://github.com/albertomh/djereo){target=\"_blank"}.

### Development prerequisites

In addition to the prerequisites listed in the [Quickstart](./quickstart.md) you will need
the following to develop `djereo`:

- [pre-commit](https://pre-commit.com/){target=\"_blank"}

### Upgrading the pycliche version

`djereo` is built on top of the [pycliche](https://github.com/albertomh/pycliche){target=\"_blank"} Python
project template. To update `djereo` to a newer version of `pycliche`:

```sh
cd ~/Projects/djereo/
uvx copier update --skip-answered --trust [--vcs-ref=<TAG>]
```

If the `--vcs-ref` flag is not specified, `copier` will use the latest `pycliche` tag.

#### Using the pycliche repo as a git remote

Alternatively, since `djereo` was started by cloning `pycliche` v2.10.0, the latest
changes to `pycliche` may be brought in as follows:

```sh
# ensure pycliche exists as an upstream remote repo

git remote -v
# expected output:
#     origin  git@github.com:albertomh/djereo.git (fetch)
#     origin  git@github.com:albertomh/djereo.git (push)
#     upstream        git@github.com:albertomh/pycliche.git (fetch)
#     upstream        git@github.com:albertomh/pycliche.git (push)

# if not present, add pycliche as a remote
git remote add upstream https://github.com:albertomh/pycliche.git

# fetch the latest changes from pycliche
git fetch upstream

# merge pycliche changes into djereo
# flag necessary since the repos' histories diverged
git merge --allow-unrelated-histories upstream/<branch-or-tag>

# resolve conflicts manually, if any
# stage resolved changes and finish the merge with
git commit
```

### Git principles

This repo follows trunk-based development. This means:

- the `main` branch should always be in a releasable state
- use short-lived feature branches

Please follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/){target=\"_blank"}
guidelines when writing commit messages. `commitlint` is enabled as
pre-commit hook. Valid commit types are defined in `.commitlintrc.ts`.

> **N.B.**  
> The phrase "gen. project" is used frequently in commit messages. It means "generated project",
> i.e. the repository created by invoking `copier` with the `djereo` template as documented
> in the [Quickstart](./quickstart.md).

### Dependency management

Dependencies are defined in the [pyproject.toml](https://github.com/albertomh/djereo/blob/main/pyproject.toml){target=\"_blank"}
file. `uv` is used to manage
dependencies:

```sh
# add a dependency to the project
uv add some-package
```

#### Updating dependencies in the template

There are two places where dependencies are currently declared in the template:

1. [.pre-commit-config.yaml.jinja](https://github.com/albertomh/djereo/blob/main/template/.pre-commit-config.yaml.jinja){target=\"_blank"}
1. [pyproject.toml.jinja](https://github.com/albertomh/djereo/blob/main/template/pyproject.toml.jinja){target=\"_blank"}

Update git hooks in the former via:

```sh
cd template/ && pre-commit autoupdate
```

Update Python packages in the latter manually. Automated option pending on account of
commands like `uv lock --upgrade-package` not taking kindly to Jinja templates.

### Generate project using development version

When developing `djereo` it is useful to observe the outcome of generating new projects
that use in-progress features. To do so:

```sh
# navigate to the parent directory of your local copy of djereo
cd ..
# vcs-ref flag to use the latest local version of djereo instead of a tagged version
uvx copier copy --vcs-ref=HEAD djereo $TEST_PROJECT_NAME
```

### Style

Code style is enforced by pre-commit hooks. Linter rules are configured in the `ruff`
tables in [pyproject.toml](https://github.com/albertomh/djereo/blob/main/pyproject.toml){target=\"_blank"}.

```sh
# before you start developing, install pre-commit hooks
pre-commit install

# update pre-commit hooks
pre-commit autoupdate
```

Docstrings should follow the conventions set out in the [Google styleguide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings){target=\"_blank"}.

### Upgrade checklist

1. Check [Django releases](https://docs.djangoproject.com/en/5.1/releases/){target=\"_blank"}
  and update the `django_version` question in `copier.yaml`.

---

## Test

Run all tests using `pytest` with:

```sh
just test
```

Tests have marks, allowing you to run only a subset:

```sh
just test -m unit
# or
just test -m "not smoke"
```

See the `tool.pytest.ini_options` table in [pyproject.toml](https://github.com/albertomh/djereo/blob/main/pyproject.toml){target=\"_blank"}
for a list of all marks.

---

## Document

`djereo`'s documentation is published as a static site generated using `mkdocs`.

Source markdown and configuration live in the `docs/` directory. The docs are styled using
the [readthedocs](https://www.mkdocs.org/user-guide/choosing-your-theme/#readthedocs){target=\"_blank"}
theme.

A custom GitHub action ([.github/actions/publish-docs](https://github.com/albertomh/djereo/blob/main/.github/actions/publish-docs/action.yaml){target=\"_blank"})
builds the `mkdocs` site and publishes it to the `gh-pages` branch. Changes to this branch
are automatically deployed to [https://albertomh.github.io/djereo/](https://albertomh.github.io/djereo/).

---

## Release

[Release Please](https://github.com/googleapis/release-please) is used to automate:

- Updating the [changelog](https://github.com/albertomh/djereo/blob/main/CHANGELOG.md){target=\"_blank"}.
- Calculating the new SemVer tag based on conventional commit types.
- Creating a new GitHub release.

Release Please is configured as a GitHub action ([release-please.yaml](https://github.com/albertomh/djereo/blob/main/.github/workflows/release-please.yaml){target=\"_blank"}).
It keeps a release pull request open that is refreshed as changes are merged into `main`.
To cut a release, simply merge the release pull request.

### GitHub Personal Access Token

In order for Release Please to automate the above process, a GitHub Actions secret called
`DJEREO_RELEASE_PLEASE_TOKEN` must exist in GitHub ([albertomh/djereo/settings/secrets/actions](https://github.com/albertomh/djereo/settings/secrets/actions){target=\"_blank"}).
The contents of this secret must be a Personal Access Token (PAT) with the following permissions:

```yaml
contents: write
pull-requests: write
```

For more information, consult the [release-please-action project](https://github.com/googleapis/release-please-action){target=\"_blank"}).
