#!/bin/sh

echo "Running black"
poetry run black kip tests
echo "Running isort"
poetry run isort kip tests
echo "Running mypy"
poetry run mypy kip
poetry run mypy --ignore-missing-import tests
echo "Running pytest"
poetry run pytest