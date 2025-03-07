test:
	poetry run pytest --cov src tests

setup:
	poetry install --no-root

format:
	poetry run ruff format .

lint:
	poetry run ruff check