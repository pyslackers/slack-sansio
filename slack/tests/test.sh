#!/bin/sh

set -e

flake8 .
black --check --diff .
isort --recursive --check-only .
pytest test --verbose --cov
sphinx-build docs/ docs/_build -W
python setup.py sdist
python setup.py bdist_wheel
