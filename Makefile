test:
	poetry run pytest -v

setup:
	poetry install --no-root

format:
	poetry run ruff format .