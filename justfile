# djereo - local development tooling

set positional-arguments

default:
  @just --list

test +args='':
  @uv sync --group test
  @uv pip install -e .
  @uv run -m pytest tests/ -s -vvv -W always --pdb "$@"
