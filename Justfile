@_:
    just --list

# Test typing with mypy (we want this to succeed)
[group('qa')]
mypy:
    uv run --with mypy mypy pyearcal/

# Optionally test with pyright (we don't aim yet)
[group('qa')]
pyright:
    uv run --with pyright pyright

# Run all the pre-commit checks on the whole code-base
pre-commit:
    uvx pre-commit run --all

build:
    rm -rf dist/
    uv build
    rm -rf src/physt.egg-info

publish: build
    uv publish
