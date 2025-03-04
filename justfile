# djereo - local development tooling

set positional-arguments

default:
  @just --list

test +args='':
  @test -d .venv/ || uv venv
  @test -x .venv/bin/pip || @uv sync --group test
  @uv pip install -e .
  @uv run -m pytest tests/ -s -vvv --showlocals -W always --pdb "$@"
