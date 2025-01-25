# djereo documentation site

This directory holds the source to a `mkdocs` microsite containing the documentation for `djereo`.

## Prerequisites

To work on `djereo`'s docs the following must be available locally:

- [Python 3.10](https://docs.python.org/3.10/) or above
- [uv](https://docs.astral.sh/uv/)

## Quickstart: run locally

A `justfile` defines common development tasks. Run `just` to show all available recipes.

```sh
# make sure to run commands from the `djereo/docs/` directory

# install dependencies in a virtual environment and run the mkdocs development server
just serve
```

## Develop djereo's docs

See [develop.md#document](./src/develop.md#document) for more on how `mkdocs` is used and
configured to publish documentation on [https://albertomh.github.io/djereo/](https://albertomh.github.io/djereo/).
