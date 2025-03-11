IMAGE_NAME = gitlab-injest

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

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm -p 8501:8501 $(IMAGE_NAME)

start: build run

clean:
	docker rmi $(IMAGE_NAME)
