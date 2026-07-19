.PHONY: install test lint format type-check docs clean build publish

install:
	pip install -e ".[dev]"

test:
	pytest -v --cov=prompt_bonsai --cov-report=term-missing

test-ci:
	pytest --cov=prompt_bonsai --cov-report=xml

lint:
	ruff check src tests
	mypy src

format:
	black src tests
	ruff check --fix src tests

type-check:
	mypy src

docs:
	mkdocs serve

build:
	python -m build

publish-test:
	twine upload --repository testpypi dist/*

publish:
	twine upload dist/*

clean:
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

all: format lint type-check test
