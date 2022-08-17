build:
	poetry build

install:
	poetry install

publish:
	poetry publish

test:
	poetry run python -m pytest

coverage:
	poetry run pytest --cov=song2txt tests/ --cov-fail-under=85

lint:
	poetry run flake8
