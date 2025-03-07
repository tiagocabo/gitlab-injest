test:
	pytest --cov=src --cov-report=term-missing --cov-fail-under=90 tests

setup:
	poetry install --no-root

format:
	ruff format .

lint:
	ruff check

app:
	streamlit run app.py