test:
	poetry run python -m pytest

coverage:
	poetry run pytest --cov=song2txt tests/ --cov-fail-under=70

lint:
	poetry run flake8
