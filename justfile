# djereo - local development tooling

set positional-arguments

default:
  @just --list

_test_setup:
  @test -d .venv/ || uv venv
  @test -x .venv/bin/pip || @uv sync --group test
  @uv pip install -e .

test +args='': _test_setup
  @uv run -m pytest tests/ -s -vvv --showlocals -W always --pdb "$@"

profile_tests: _test_setup
  @source .venv/bin/activate
  @sudo py-spy record --subprocesses --format speedscope -o profile.speedscope.json -- \
    uv run pytest tests/
