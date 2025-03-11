IMAGE_NAME = gitlab-injest

local-test:
	poetry run 	pytest --cov=src --cov-report=term-missing --cov-report=xml --cov-fail-under=90 tests

setup:
	poetry install --no-root

format:
	ruff format .

lint:
	ruff check

app:
	poetry run streamlit run app.py

clean:
	docker rmi $(IMAGE_NAME)

build:
	docker compose build

test:
	docker compose up test --abort-on-container-exit

start:
	docker compose up app --abort-on-container-exit