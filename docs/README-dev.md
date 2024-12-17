# Developer README

## Develop

### Development prerequisites

In addition to the [Prerequisites](../README.md#prerequisites) listed in the README you
will need the following to develop `pycliche`:

- [pre-commit](https://pre-commit.com/)

### Recursive pycliche

The `pycliche` repo has been retrofit to use `pycliche` itself as its template following
[release v2.6.0](https://github.com/albertomh/pycliche/releases/tag/v2.6.0).

To update `pycliche` to a newer version of itself:

```sh
cd ~/Projects/pycliche/
uvx copier update --skip-answered --trust [--vcs-ref=<TAG>]
```

If the `--vcs-ref` flag is not specified, `copier` will use the latest `pycliche` tag.

### Git principles

This repo follows trunk-based development. This means:

- the `main` branch should always be in a releasable state
- use short-lived feature branches

### Dependency management

Dependencies are defined in the `pyproject.toml` file. `uv` is used to manage
dependencies:

```sh
# add a dependency to the project
uv add some-package
```

#### Updating dependencies in the template

There are two places where dependencies are currently declared in the template:

1. `.pre-commit-config.yaml`
1. `pyproject.toml.jinja`

Update git hooks in the former via:

```sh
cd template/ && pre-commit autoupdate
```

Update Python packages in the latter manually. Automated option pending on account of
commands like `uv lock --upgrade-package` not taking kindly to Jinja templates.

### Generate project using development version

When developing `pycliche` it is useful to observe the outcome of generating new projects
that use in-progress features. To do so:

```sh
# navigate to the parent directory of your local copy of pycliche
cd ~/Projects/
# vcs-ref flag to use the latest local version of pycliche instead of a tagged version
uvx copier copy --vcs-ref=HEAD pycliche $TEST_PROJECT_NAME
```

### Style

Code style is enforced by pre-commit hooks. Linter rules are configured in the `ruff`
tables in `pyproject.toml`.

```sh
# before you start developing, install pre-commit hooks
pre-commit install

# update pre-commit hooks
pre-commit autoupdate
```

Docstrings should follow the conventions set out in the [Google styleguide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

Please follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
guidelines when writing commit messages. `commitlint` is enabled as
pre-commit hook. Valid commit types are defined in `.commitlintrc.ts`.

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

See the `tool.pytest.ini_options` table in `pyproject.toml` for a list of all marks.

## Release

[Release Please](https://github.com/googleapis/release-please) is used to automate:

- Updating the [changelog](CHANGELOG.md).
- Calculating the new SemVer tag based on conventional commit types.
- Creating a new GitHub release.

Release Please is configured as a GitHub action ([release-please.yaml](.github/workflows/release-please.yaml)).
It keeps a release pull request open that is refreshed as changes are merged into `main`.
To cut a release, simply merge the release pull request.

### GitHub Personal Access Token

In order for Release Please to automate the above process, a GitHub Actions secret called
`PYCLICHE_RELEASE_PLEASE_TOKEN` must exist in GitHub ([albertomh/pycliche/settings/secrets/actions](albertomh/pycliche/settings/secrets/actions)).
The contents of this secret must be a Personal Access Token (PAT) with the following permissions:

```yaml
contents: write
pull-requests: write
```

For more information, consult the [release-please-action project](https://github.com/googleapis/release-please-action).

## Record demo

The main [README](../README.md) includes a GIF showcasing generating a project using
`pycliche`. To record a new demo, record the output of running `docs/media/auto_pycliche_demo.sh`.

Convert to a gif with:

```sh
# speed up video by 2x (PTS/2)
ffmpeg -i pycliche-M.m.p-demo.mov -filter:v "setpts=PTS/2,fps=60" -an pycliche-M.m.p-demo_fast.mov
# convert to GIF
ffmpeg -i pycliche-M.m.p-demo_fast.mov -vf "fps=15,scale=iw:-1:flags=lanczos" -loop 0 pycliche-M.m.p-demo.gif
```
