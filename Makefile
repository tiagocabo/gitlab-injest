test:
	pytest --cov src tests

setup:
	poetry install --no-root

format:
	ruff format .

lint:
	ruff check

app:
	streamlit run app.py